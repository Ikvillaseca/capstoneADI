import requests
import json
from django.conf import settings
from decimal import ROUND_HALF_UP, Decimal
from math import radians, sin, cos, sqrt, asin
from sklearn.cluster import KMeans
import numpy as np
from collections import defaultdict
import datetime
import traceback
from .models import Viaje, Pasajero_Viaje, Parada_Viaje, Chofer, Vehiculo
import google.auth
from google.auth.transport.requests import Request
from django.utils import timezone
from django.utils.timezone import make_aware, localtime

# Verificar si la api funciona correctamente
def verificar_api_key():
    try:
        api_key = settings.GOOGLE_MAPS_API_KEY
        return api_key is not None and len(str(api_key).strip()) > 0
    except Exception:
        return False

API_EXISTE = verificar_api_key()

def obtener_access_token():
    """
    Obtiene el token OAuth2 usando las credenciales del service account
    """
    try:
        # Cargar credenciales desde el archivo JSON configurado
        credentials, project = google.auth.default(
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        # Refrescar el token si es necesario
        auth_req = Request()
        credentials.refresh(auth_req)
        
        print(f"✓ Token OAuth2 obtenido exitosamente")
        print(f"  Proyecto: {project}")
        
        return credentials.token
        
    except Exception as e:
        print(f"✗ Error obteniendo token OAuth2: {str(e)}")
        traceback.print_exc()
        return None

#Diccionario de prioridades para el geocoding
TIPO_PRIORIDAD = [
    "airport",
    "bus_station",
    "subway_station",
    "train_station",
    "transit_station",
    "establishment",
    "point_of_interest",
    "premise",
    "street_address",
]

TIPO_PARADERO_MAP = {
    "airport": "A",
    "bus_station": "P",
    "subway_station": "M",
    "train_station": "M",
    "transit_station": "M",
    "establishment": "E",
    "point_of_interest": "O",
    "premise": "E",
    "street_address": "O",
}


def determinar_tipo_paradero(tipo):
    for tipo_prio in TIPO_PRIORIDAD:
        if tipo_prio in tipo:
            return TIPO_PARADERO_MAP.get(tipo_prio, "O")
    return "O"


def geocoding_desde_direccion(direccion):
    api_key = settings.GOOGLE_MAPS_API_KEY
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": direccion,
        "key": api_key,
        "components": "country:CL",
        "language": "es-419",
        "region": "cl",
    }

    try:
        response = requests.get(url, params=params)
        # Caso en el que tenemos respuesta con exito
        if response.status_code == 200:
            data = response.json()
            # Guardar los datos de la respuesta en una variable para que no sean tan grandes las consultas
            datos_lugar = data["results"][0]
            # Obtener los datos que quiero de la response
            lat = datos_lugar["geometry"]["location"]["lat"]
            lon = datos_lugar["geometry"]["location"]["lng"]
            direccion = datos_lugar["formatted_address"]
            tipos = datos_lugar["types"]
            # Se puede obtener la comuna/region en el caso de ser necesario
            # Arreglar los distintos datos para que tengan el formato correcto
            lat = Decimal(str(lat)).quantize(
                Decimal("0.000001"), rounding=ROUND_HALF_UP
            )
            lon = Decimal(str(lon)).quantize(
                Decimal("0.000001"), rounding=ROUND_HALF_UP
            )
            direccion = str(direccion)
            tipo = determinar_tipo_paradero(tipos)
            return lat, lon, direccion, tipo
        # Caso en el que hay una respuesta sin exito
        else:
            return None, None, None, None
    # Caso en el que ocurre un error
    except Exception as e:
        print(f"ERROR:\n{str(e)}")
        return None, None, None, None
    


# El plan es agrupar pasajeros por paraderos, y luego intentar agrupar los paraderos mas cercanos
# Luego de eso intentar asignar los pasajeros a los vehiculos tomando en consideracion la capacidad
# Probablemente caiga en un problema matematico de optimizacion.
# O a lo mejor tenga que hacer algo como clustering???
# por ejemplo, que hacer cuando tengo capacidades de vehiculos como 11 y 12
# y 8 pasajeros para un lado A, 4 para otro lado B
# A y B son cercanos y lo ideal seria asignarlos al vehiculo de 12.
# Pero por ejemplo puede ocurrir que ahora sean 8 y 6
# En ese caso debo asignar el grupo B al vehiculo de 11
# Seria buena idea intentar primero hacer viajes con un chofer y considerar, luego la implementacion de varios al mismo tiempo y asignar los viajes.
# A este punto para que funcione todo, se deben tener Pasajeros con paraderos asignados, Choferes con vehiculo asignado, y ahora seleccionar el paradero de destino u origen???

# Esta es probablemente la parte mas compleja de todo el proyecto

def calcular_distancias_haversine(lat1, lon1, lat2, lon2):
    # PROBABLEMENTE BORRAR, IDEA SIN CONCRETAR
    print("=== Calculando distancias ===")
    # Redondeo radio tierra en KM.
    R = 6371.2
    # Convertir a radianes
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Esta es la formula creo, se calcula la distancia de latitudes y longitudes
    # Y se aplica "Formula Haversine"
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return c * R

def agrupar_pasajeros_mismo_paradero(grupo):
    lista_pasajeros_grupo = grupo.pasajero.select_related('paradero_deseado').all()

    paraderos_deseados = defaultdict(list)
    pasajeros_sin_paradero = []
    for pasajero in lista_pasajeros_grupo:
        # Para poder identificar pasajeros que no tienen paradero deseado sin causar problemas en el flujo 
        if not pasajero.paradero_deseado:
            print(f"!!!!!! Pasajero {pasajero.id_pasajero} ({pasajero.nombre}) sin paradero asignado")
            pasajeros_sin_paradero.append(pasajero)
            continue
        paradero_id = pasajero.paradero_deseado.id_ubicacion
        paraderos_deseados[paradero_id].append(pasajero)

    # Si es que permitimos que existan pasajeros sin un paradero deseado, puede existir un problema ya que no serian considerados.
    # Asumiremos que todos los pasajeros tienen un paradero_deseado de recogida/destino
    if pasajeros_sin_paradero:
        print("EXISTEN PASAJEROS QUE NO TIENEN PARADERO ASIGNADO")
        print(pasajeros_sin_paradero)
    
    # Esto es para poder acceder a cada item
    for paradero_id, pasajeros in paraderos_deseados.items():
        # print(paradero_id, pasajeros)
        continue

    return paraderos_deseados

def obtener_detalles_vehiculos(grupo):
    """
    Obtiene los detalles de los vehiculos y simplifica las consultas
    Retorna una lista de diccionarios de vehiculos
    """
    lista_vehiculos_grupo = grupo.chofer.select_related('id_vehiculo').all()
    # Necesito tener en cuenta siempre al chofer.id_chofer-datos_vehiculo
    detalles_vehiculos = []

    for chofer in lista_vehiculos_grupo:
        # Para poder identificar pasajeros que no tienen paradero deseado sin causar problemas en el flujo
        diccionario_vehiculo = {
        "id_vehiculo": chofer.id_vehiculo.id_vehiculo,
        "id_chofer": chofer.id_chofer,
        "capacidad": chofer.id_vehiculo.capacidad
        }
        detalles_vehiculos.append(diccionario_vehiculo)
    return detalles_vehiculos

def agrupar_paraderos_cercanos(paraderos_con_pasajeros, num_clusters=None):
    """
    Agrupa paraderos cercanos usando KMeans
    Retorna una lista de clusters con paraderos y pasajeros, agrupados
    """
    # Para evitar errores
    if not paraderos_con_pasajeros:
        return []
    
    # Extraer coordenadas de paraderos
    coordenadas = []
    paraderos_info = []
    
    for paradero_id, pasajeros in paraderos_con_pasajeros.items():
        paradero = pasajeros[0].paradero_deseado
        coordenadas.append([float(paradero.latitud), float(paradero.longitud)])
        paraderos_info.append({
            'paradero_id': paradero_id,
            'paradero': paradero,
            'pasajeros': pasajeros,
            'cantidad': len(pasajeros)
        })
    
    # Siempre le envio la cantidad de vehiculos, pero si no, 
    # usar el numero de ubicaciones como clusteres
    if num_clusters is None or num_clusters > len(coordenadas):
        num_clusters = len(coordenadas)
    
    # Aplicar KMeans
    coordenadas_array = np.array(coordenadas)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(coordenadas_array)
    
    # Organizar por cluster
    clusters_agrupados = defaultdict(list)
    for idx, cluster_id in enumerate(clusters):
        clusters_agrupados[cluster_id].append(paraderos_info[idx])
    
    return clusters_agrupados

def asignar_vehiculos_a_clusters(clusters, vehiculos):
    """
    Asigna vehículos a clusters basándose en capacidad
    Retorna: lista de asignaciones {vehiculo, cluster, pasajeros}
    """
    asignaciones = []
    vehiculos_disponibles = sorted(vehiculos, key=lambda v: v['capacidad'], reverse=True)
    
    # Ordenar clusters por cantidad de pasajeros (descendente)
    clusters_ordenados = sorted(
        clusters.items(),
        key=lambda x: sum(p['cantidad'] for p in x[1]),
        reverse=True
    )
    
    for cluster_id, paraderos_cluster in clusters_ordenados:
        total_pasajeros = sum(p['cantidad'] for p in paraderos_cluster)
        pasajeros_lista = []
        
        # Recolectar todos los pasajeros del cluster
        for paradero_info in paraderos_cluster:
            pasajeros_lista.extend(paradero_info['pasajeros'])
        
        # Buscar vehículo con capacidad suficiente
        vehiculo_asignado = None
        for idx, vehiculo in enumerate(vehiculos_disponibles):
            if vehiculo['capacidad'] >= total_pasajeros:
                vehiculo_asignado = vehiculo
                vehiculos_disponibles.pop(idx)
                break
        
        # Si no hay vehículo con capacidad suficiente, dividir cluster
        if not vehiculo_asignado and vehiculos_disponibles:
            # Tomar el vehículo más grande disponible
            vehiculo_asignado = vehiculos_disponibles.pop(0)
            capacidad = vehiculo_asignado['capacidad']
            
            # Asignar pasajeros hasta llenar capacidad
            pasajeros_asignados = pasajeros_lista[:capacidad]
            pasajeros_restantes = pasajeros_lista[capacidad:]
            
            asignaciones.append({
                'vehiculo': vehiculo_asignado,
                'cluster_id': cluster_id,
                'paraderos': paraderos_cluster,
                'pasajeros': pasajeros_asignados,
                'capacidad_usada': len(pasajeros_asignados)
            })
            
            # Crear nueva asignación para pasajeros restantes
            if pasajeros_restantes and vehiculos_disponibles:
                vehiculo_extra = vehiculos_disponibles.pop(0)
                asignaciones.append({
                    'vehiculo': vehiculo_extra,
                    'cluster_id': f"{cluster_id}_overflow",
                    'paraderos': paraderos_cluster,
                    'pasajeros': pasajeros_restantes,
                    'capacidad_usada': len(pasajeros_restantes)
                })
        else:
            if vehiculo_asignado:
                asignaciones.append({
                    'vehiculo': vehiculo_asignado,
                    'cluster_id': cluster_id,
                    'paraderos': paraderos_cluster,
                    'pasajeros': pasajeros_lista,
                    'capacidad_usada': len(pasajeros_lista)
                })
    
    return asignaciones


def calcular_ruta_optima(paraderos_cluster, origen, destino):
    """
    Calcula la ruta óptima para visitar todos los paraderos
    Retorna: lista ordenada de paraderos con información de pasajeros
    """
    if not paraderos_cluster:
        return []
    
    # Extraer coordenadas
    coordenadas = []
    paraderos_info = []
    
    for paradero_info in paraderos_cluster:
        paradero = paradero_info['paradero']
        coordenadas.append([float(paradero.latitud), float(paradero.longitud)])
        paraderos_info.append(paradero_info)
    
    # Si solo hay un paradero, retornar directamente
    if len(coordenadas) == 1:
        return [paraderos_info[0]]
    
    # Algoritmo del vecino más cercano (Nearest Neighbor)
    coord_origen = [float(origen.latitud), float(origen.longitud)]
    ruta_ordenada = []
    indices_visitados = set()
    coord_actual = coord_origen
    
    while len(indices_visitados) < len(coordenadas):
        distancia_min = float('inf')
        idx_mas_cercano = None
        
        for idx, coord in enumerate(coordenadas):
            if idx in indices_visitados:
                continue
            
            distancia = calcular_distancias_haversine(
                coord_actual[0], coord_actual[1],
                coord[0], coord[1]
            )
            
            if distancia < distancia_min:
                distancia_min = distancia
                idx_mas_cercano = idx
        
        if idx_mas_cercano is not None:
            indices_visitados.add(idx_mas_cercano)
            ruta_ordenada.append(paraderos_info[idx_mas_cercano])
            coord_actual = coordenadas[idx_mas_cercano]
    
    return ruta_ordenada

def estimar_tiempo_viaje(distancia_km, velocidad_promedio=30):
    """
    Estima el tiempo de viaje en minutos
    distancia_km: distancia en kilómetros
    velocidad_promedio: km/h (default 30 para ciudad)
    """
    tiempo_horas = distancia_km / velocidad_promedio
    tiempo_minutos = tiempo_horas * 60
    # Agregar 5 minutos por parada (tiempo de espera)
    return int(tiempo_minutos) + 5

def crear_viajes_desde_asignaciones(asignaciones, punto_encuentro, tipo_viaje="IDA", fecha_hora_deseada=None, tipo_hora_deseada='LLEGADA', grupo=None):
    """
    Crea objetos Viaje con sus paradas ordenadas
    tipo_viaje: 'IDA' (recoger) o 'VUELTA' (dejar)
    grupo: Grupo_Pasajeros al que pertenece este viaje
    #Punto encuentro: Destino si es IDA, Origen si es VUELTA

    """
    hora_salida_base = fecha_hora_deseada
    # Definir un campo para definir la hora de inicio del viaje (Probablemente tambien el dia)
    if hora_salida_base is None:
        hora_salida_base = datetime.time(7, 0)
    
    viajes_creados = []
    
    # Crear viaje por asignacion
    for asignacion in asignaciones:
        #Obtener los datos necesarios para crear los viajes
        vehiculo = asignacion['vehiculo']
        pasajeros = asignacion['pasajeros']
        paraderos_cluster = asignacion['paraderos']
        chofer = Chofer.objects.get(id_chofer=vehiculo['id_chofer'])
        
        # Determinar primer paradero del recorrido
        primer_paradero = pasajeros[0].paradero_deseado
        
        if tipo_viaje == 'IDA':
            origen_viaje = primer_paradero
            destino_viaje = punto_encuentro
        else:
            origen_viaje = punto_encuentro
            destino_viaje = primer_paradero

        # Calcular el orden de los paraderos
        ruta_ordenada = calcular_ruta_optima(paraderos_cluster, origen_viaje, destino_viaje)
        
        # Calcular distancia total
        distancia_total = 0
        if tipo_viaje == 'IDA':
            coord_actual = [float(primer_paradero.latitud), float(primer_paradero.longitud)]
        else:
            coord_actual = [float(punto_encuentro.latitud), float(punto_encuentro.longitud)]
        
        for paradero_info in ruta_ordenada:
            paradero = paradero_info['paradero']
            coord_paradero = [float(paradero.latitud), float(paradero.longitud)]
            distancia = calcular_distancias_haversine(
                coord_actual[0], coord_actual[1],
                coord_paradero[0], coord_paradero[1]
            )
            distancia_total += distancia
            coord_actual = coord_paradero
        
        if tipo_viaje == 'IDA':
            distancia_total += calcular_distancias_haversine(coord_actual[0], coord_actual[1],
                float(punto_encuentro.latitud), float(punto_encuentro.longitud))
        
        tiempo_total_minutos = estimar_tiempo_viaje(distancia_total)
        hora_llegada = (datetime.datetime.combine(datetime.date.today(), hora_salida_base) + 
                       datetime.timedelta(minutes=tiempo_total_minutos)).time()
        
        # Crear viaje
        viaje = Viaje.objects.create(
            tipo_viaje=tipo_viaje,
            hora_Salida=hora_salida_base,
            hora_Llegada=hora_llegada,
            id_vehiculo_id=vehiculo['id_vehiculo'],
            id_chofer=chofer,
            punto_encuentro=punto_encuentro,
            id_grupo=grupo
        )
                
        hora_actual = hora_salida_base
        coord_anterior = [float(origen_viaje.latitud), float(origen_viaje.longitud)]
        #Crear los paraderos
        
        #Viaje de IDA (primero los paraderos luego el final definido)
        if tipo_viaje == 'IDA':
            for orden, paradero_info in enumerate(ruta_ordenada, start=1):
                paradero = paradero_info['paradero']
                cantidad_pasajeros = paradero_info['cantidad']
                
                coord_paradero = [float(paradero.latitud), float(paradero.longitud)]
                distancia_tramo = calcular_distancias_haversine(
                    coord_anterior[0], coord_anterior[1],
                    coord_paradero[0], coord_paradero[1]
                )
                
                tiempo_tramo = estimar_tiempo_viaje(distancia_tramo)
                hora_actual = (datetime.datetime.combine(datetime.date.today(), hora_actual) + 
                              datetime.timedelta(minutes=tiempo_tramo)).time()
                
                Parada_Viaje.objects.create(
                    id_viaje=viaje,
                    id_parada=paradero,
                    orden=orden,
                    pasajeros_suben=cantidad_pasajeros,
                    pasajeros_bajan=0,
                    hora_estimada_llegada=hora_actual
                )
                
                coord_anterior = coord_paradero
            
            distancia_final = calcular_distancias_haversine(
                coord_anterior[0], coord_anterior[1],
                float(punto_encuentro.latitud), float(punto_encuentro.longitud)
            )
            tiempo_final = estimar_tiempo_viaje(distancia_final)
            hora_actual = (datetime.datetime.combine(datetime.date.today(), hora_actual) + 
                          datetime.timedelta(minutes=tiempo_final)).time()
            
            Parada_Viaje.objects.create(
                id_viaje=viaje,
                id_parada=punto_encuentro,
                orden=len(ruta_ordenada) + 1,
                pasajeros_suben=0,
                pasajeros_bajan=len(pasajeros),
                hora_estimada_llegada=hora_actual
            )
        
        #Viaje de VUELTA (Origen definido, luego se dejan pasajeros en los paraderos)
        else:
            Parada_Viaje.objects.create(
                id_viaje=viaje,
                id_parada=punto_encuentro,
                orden=1,
                pasajeros_suben=len(pasajeros),
                pasajeros_bajan=0,
                hora_estimada_llegada=hora_salida_base
            )
            
            for orden, paradero_info in enumerate(ruta_ordenada, start=2):
                paradero = paradero_info['paradero']
                cantidad_pasajeros = paradero_info['cantidad']
                
                coord_paradero = [float(paradero.latitud), float(paradero.longitud)]
                distancia_tramo = calcular_distancias_haversine(
                    coord_anterior[0], coord_anterior[1],
                    coord_paradero[0], coord_paradero[1]
                )
                
                tiempo_tramo = estimar_tiempo_viaje(distancia_tramo)
                hora_actual = (datetime.datetime.combine(datetime.date.today(), hora_actual) + 
                              datetime.timedelta(minutes=tiempo_tramo)).time()
                
                Parada_Viaje.objects.create(
                    id_viaje=viaje,
                    id_parada=paradero,
                    orden=orden,
                    pasajeros_suben=0,
                    pasajeros_bajan=cantidad_pasajeros,
                    hora_estimada_llegada=hora_actual
                )
                
                coord_anterior = coord_paradero
        
        for pasajero in pasajeros:
            Pasajero_Viaje.objects.create(
                id_viaje=viaje,
                id_pasajero=pasajero
            )
        
        viajes_creados.append({
            'viaje': viaje,
            'tipo': tipo_viaje,
            'pasajeros_count': len(pasajeros),
            'capacidad_usada': asignacion['capacidad_usada'],
            'paradas_count': len(ruta_ordenada) + 1,
            'distancia_km': round(distancia_total, 2)
        })
        
        print(f"=== Viaje {tipo_viaje} creado: {viaje.id_viaje} ===")
        print(f"  Grupo: {grupo if grupo else 'Sin grupo'}")
        print(f"  Chofer: {chofer.nombre} {chofer.apellido}")
        print(f"  Pasajeros: {len(pasajeros)}/{vehiculo['capacidad']}")
        print(f"  Paradas: {len(ruta_ordenada) + 1}")
    
    return viajes_creados

def procesar_respuesta_api(resultado_api, asignacion, punto_encuentro, tipo_viaje, hora_deseada, tipo_hora_deseada, chofer, grupo):
    """
    Procesa la respuesta de la API y crea los objetos Viaje y Parada_Viaje
    """
    try:
        routes = resultado_api.get('routes', [])
        if not routes:
            print("No se encontraron rutas en la respuesta")
            return None
        
        route = routes[0]
        vehiculo = asignacion['vehiculo']
        pasajeros = asignacion['pasajeros']
        
        visits = route.get('visits', [])
        metrics = route.get('metrics', {})
        transitions = route.get('transitions', [])
        
        # Extraer horas reales de la respuesta de la API
        primera_visita = visits[0]
        ultima_visita = visits[-1]
        
        hora_salida_str = primera_visita.get('startTime', '')
        hora_llegada_str = ultima_visita.get('startTime', '')
        
        # Convertir strings UTC a datetime aware
        hora_salida_utc = datetime.datetime.fromisoformat(hora_salida_str.replace('Z', '+00:00'))
        hora_llegada_utc = datetime.datetime.fromisoformat(hora_llegada_str.replace('Z', '+00:00'))
        
        # Convertir a hora local de Chile automáticamente
        hora_salida_local = localtime(hora_salida_utc)
        hora_llegada_local = localtime(hora_llegada_utc)
        
        # Extraer solo el time para guardar en BD
        hora_salida = hora_salida_local.time()
        hora_llegada = hora_llegada_local.time()
        
        # Crear el viaje con las horas reales de la API
        viaje = Viaje.objects.create(
            tipo_viaje=tipo_viaje,
            hora_Salida=hora_salida,
            hora_Llegada=hora_llegada,
            id_vehiculo_id=vehiculo['id_vehiculo'],
            id_chofer=chofer,
            punto_encuentro=punto_encuentro,
            id_grupo=grupo
        )
        
        print(f"\n=== Creando paradas del viaje ===")
        print(f"Hora salida real: {hora_salida}")
        print(f"Hora llegada real: {hora_llegada}")
        print(f"Total paradas: {len(visits)}")
        
        # Crear las paradas según las visitas optimizadas
        for orden, visit in enumerate(visits, start=1):
            start_time_str = visit.get('startTime', '')
            start_datetime_utc = datetime.datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            start_datetime_local = localtime(start_datetime_utc)
            hora_parada = start_datetime_local.time()
            
            is_pickup = visit.get('isPickup', False)
            shipment_label = visit.get('shipmentLabel', '')
            
            # Extraer cantidad de pasajeros del label
            cantidad_pasajeros = 0
            if 'Pasajeros_' in shipment_label:
                try:
                    cantidad_pasajeros = int(shipment_label.split('Pasajeros_')[1])
                except:
                    cantidad_pasajeros = 1
            
            if tipo_viaje == "IDA":
                if is_pickup:
                    # Buscar paradero correspondiente
                    paradero = None
                    for paradero_info in asignacion['paraderos']:
                        if str(paradero_info['paradero'].id_ubicacion) in shipment_label:
                            paradero = paradero_info['paradero']
                            cantidad_pasajeros = paradero_info['cantidad']
                            break
                    
                    if paradero:
                        Parada_Viaje.objects.create(
                            id_viaje=viaje,
                            id_parada=paradero,
                            orden=orden,
                            pasajeros_suben=cantidad_pasajeros,
                            pasajeros_bajan=0,
                            hora_estimada_llegada=hora_parada
                        )
                        print(f"  Parada {orden}: Paradero {paradero.id_ubicacion} - Suben {cantidad_pasajeros} - {hora_parada}")
                else:
                    # Punto de encuentro (destino)
                    Parada_Viaje.objects.create(
                        id_viaje=viaje,
                        id_parada=punto_encuentro,
                        orden=orden,
                        pasajeros_suben=0,
                        pasajeros_bajan=len(pasajeros),
                        hora_estimada_llegada=hora_parada
                    )
                    print(f"  Parada {orden}: Punto Encuentro - Bajan {len(pasajeros)} - {hora_parada}")
            
            else:  # VUELTA
                if is_pickup:
                    # Punto de encuentro (origen)
                    Parada_Viaje.objects.create(
                        id_viaje=viaje,
                        id_parada=punto_encuentro,
                        orden=orden,
                        pasajeros_suben=len(pasajeros),
                        pasajeros_bajan=0,
                        hora_estimada_llegada=hora_parada
                    )
                    print(f"  Parada {orden}: Punto Encuentro - Suben {len(pasajeros)} - {hora_parada}")
                else:
                    # Buscar paradero correspondiente
                    paradero = None
                    for paradero_info in asignacion['paraderos']:
                        if str(paradero_info['paradero'].id_ubicacion) in shipment_label:
                            paradero = paradero_info['paradero']
                            cantidad_pasajeros = paradero_info['cantidad']
                            break
                    
                    if paradero:
                        Parada_Viaje.objects.create(
                            id_viaje=viaje,
                            id_parada=paradero,
                            orden=orden,
                            pasajeros_suben=0,
                            pasajeros_bajan=cantidad_pasajeros,
                            hora_estimada_llegada=hora_parada
                        )
                        print(f"  Parada {orden}: Paradero {paradero.id_ubicacion} - Bajan {cantidad_pasajeros} - {hora_parada}")
        
        # Asociar pasajeros al viaje
        for pasajero in pasajeros:
            Pasajero_Viaje.objects.create(
                id_viaje=viaje,
                id_pasajero=pasajero
            )
        
        print(f"Viaje creado exitosamente: {viaje.id_viaje}")
        
        return {
            'viaje': viaje,
            'tipo': tipo_viaje,
            'pasajeros_count': len(pasajeros),
            'capacidad_usada': asignacion['capacidad_usada'],
            'paradas_count': len(visits),
            'distancia_km': round(float(metrics.get('travelDistanceMeters', 0)) / 1000, 2)
        }
        
    except Exception as e:
        print(f"Error procesando respuesta API: {str(e)}")
        traceback.print_exc()
        return None
    

def crear_viajes_desde_asignaciones_api(asignaciones, punto_encuentro, tipo_viaje="IDA", fecha_hora_deseada=None, tipo_hora_deseada='LLEGADA', grupo=None):
    # Optimizar el orden y la ruta
    # Route optimization API (Testear la viabilidad de esto)
    print("Creando viajes usando API")
    
    # Configurar acceso a la API
    project_id = settings.GOOGLE_CLOUD_PROJECT_ID
    base_url_optimization = f"https://routeoptimization.googleapis.com/v1/projects/{project_id}:optimizeTours"
    
    # Obtener token OAuth2
    access_token = obtener_access_token()
    if not access_token:
        print("No se pudo obtener token OAuth2")
        print("Usando método fallback sin API...")
        return crear_viajes_desde_asignaciones(
            asignaciones, 
            punto_encuentro, 
            tipo_viaje, 
            fecha_hora_deseada, 
            tipo_hora_deseada, 
            grupo
        )
    
    # Headers con Bearer token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    
    
    viajes_creados = []
    
    # Configurar hora base
    if fecha_hora_deseada is None:
        fecha_hora_deseada = timezone.now()
    
    if isinstance(fecha_hora_deseada, datetime.time):
        fecha_hora_deseada = datetime.datetime.combine(datetime.date.today(), fecha_hora_deseada)
    
    # Hacer aware si es naive (Django lo convierte automáticamente a TIME_ZONE)
    if timezone.is_naive(fecha_hora_deseada):
        fecha_hora_deseada = make_aware(fecha_hora_deseada)
    
    # Guardar hora local para prints
    hora_base_local = localtime(fecha_hora_deseada)
    
    # Convertir a UTC para la API
    hora_base_utc = fecha_hora_deseada.astimezone(datetime.timezone.utc)

    # Crear un viaje por cada asignación
    for idx, asignacion in enumerate(asignaciones, start=1):
        try:
            print(f"\n=== Procesando asignación {idx}/{len(asignaciones)} ===")
            
            vehiculo = asignacion['vehiculo']
            pasajeros = asignacion['pasajeros']
            paraderos_cluster = asignacion['paraderos']
            chofer = Chofer.objects.get(id_chofer=vehiculo['id_chofer'])
            
            # Construir shipments
            shipments = []
            
            for paradero_info in paraderos_cluster:
                paradero = paradero_info['paradero']
                cantidad_pasajeros = paradero_info['cantidad']
                
                print(f"Creando ventanas basando en la hora de {tipo_hora_deseada} ESPERADA")
                
                # Configurar ventanas de tiempo según tipo de hora deseada
                if tipo_hora_deseada == 'LLEGADA':
                    if tipo_viaje == "IDA":
                        pickup_start = (hora_base_utc - datetime.timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        pickup_end = (hora_base_utc - datetime.timedelta(minutes=15)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        delivery_start = (hora_base_utc - datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        delivery_end = (hora_base_utc + datetime.timedelta(minutes=2)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                    else:  # VUELTA
                        pickup_start = (hora_base_utc - datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        pickup_end = (hora_base_utc + datetime.timedelta(minutes=2)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        delivery_start = (hora_base_utc + datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        delivery_end = (hora_base_utc + datetime.timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                else:  # INICIO
                    if tipo_viaje == "IDA":
                        pickup_start = hora_base_utc.strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        pickup_end = (hora_base_utc + datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        delivery_start = (hora_base_utc + datetime.timedelta(minutes=15)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        delivery_end = (hora_base_utc + datetime.timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                    else:  # VUELTA
                        pickup_start = hora_base_utc.strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        pickup_end = (hora_base_utc + datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        delivery_start = (hora_base_utc + datetime.timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                        delivery_end = (hora_base_utc + datetime.timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                
                if tipo_viaje == "IDA":
                    shipment = {
                        "pickups": [{
                            "arrivalWaypoint": {
                                "location": {
                                    "latLng": {
                                        "latitude": float(paradero.latitud),
                                        "longitude": float(paradero.longitud)
                                    }
                                }
                            },
                            "timeWindows": [{
                                "startTime": pickup_start,
                                "endTime": pickup_end
                            }],
                            "duration": "300s"
                        }],
                        "deliveries": [{
                            "arrivalWaypoint": {
                                "location": {
                                    "latLng": {
                                        "latitude": float(punto_encuentro.latitud),
                                        "longitude": float(punto_encuentro.longitud)
                                    }
                                }
                            },
                            "timeWindows": [{
                                "startTime": delivery_start,
                                "endTime": delivery_end
                            }],
                            "duration": "180s"
                        }],
                        "label": f"Paradero_{paradero.id_ubicacion}_Pasajeros_{cantidad_pasajeros}",
                        "loadDemands": {
                            "pasajeros": {"amount": str(cantidad_pasajeros)}
                        }
                    }
                else:  # VUELTA
                    shipment = {
                        "pickups": [{
                            "arrivalWaypoint": {
                                "location": {
                                    "latLng": {
                                        "latitude": float(punto_encuentro.latitud),
                                        "longitude": float(punto_encuentro.longitud)
                                    }
                                }
                            },
                            "timeWindows": [{
                                "startTime": pickup_start,
                                "endTime": pickup_end
                            }],
                            "duration": "180s"
                        }],
                        "deliveries": [{
                            "arrivalWaypoint": {
                                "location": {
                                    "latLng": {
                                        "latitude": float(paradero.latitud),
                                        "longitude": float(paradero.longitud)
                                    }
                                }
                            },
                            "timeWindows": [{
                                "startTime": delivery_start,
                                "endTime": delivery_end
                            }],
                            "duration": "180s"
                        }],
                        "label": f"Paradero_{paradero.id_ubicacion}_Pasajeros_{cantidad_pasajeros}",
                        "loadDemands": {
                            "pasajeros": {"amount": str(cantidad_pasajeros)}
                        }
                    }
                
                shipments.append(shipment)
            
            # Configurar vehículo
            if tipo_hora_deseada == 'LLEGADA':
                vehiculo_start = (hora_base_utc - datetime.timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                vehiculo_start_end = (hora_base_utc - datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                vehiculo_end_start = (hora_base_utc - datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                vehiculo_end_end = (hora_base_utc + datetime.timedelta(minutes=2)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
            else:  # INICIO
                vehiculo_start = hora_base_utc.strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                vehiculo_start_end = (hora_base_utc + datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                vehiculo_end_start = hora_base_utc.strftime('%Y-%m-%dT%H:%M:%S') + "Z"
                vehiculo_end_end = (hora_base_utc + datetime.timedelta(hours=4)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"  
            
            vehicle_config = {
                "loadLimits": {
                    "pasajeros": {
                        "maxLoad": vehiculo['capacidad']
                    }
                },
                "costPerHour": 30,
                "costPerKilometer": 1,
                "startTimeWindows": [{
                    "startTime": vehiculo_start,
                    "endTime": vehiculo_start_end
                }],
                "endTimeWindows": [{
                    "startTime": vehiculo_end_start,
                    "endTime": vehiculo_end_end
                }],
                "label": f"Vehiculo_{vehiculo['id_vehiculo']}_Chofer_{chofer.id_chofer}"
            }
            
            global_start = (hora_base_utc - datetime.timedelta(hours=5)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
            global_end = (hora_base_utc + datetime.timedelta(hours=5)).strftime('%Y-%m-%dT%H:%M:%S') + "Z"
            
            data = {
                "timeout": "30s",
                "model": {
                    "shipments": shipments,
                    "vehicles": [vehicle_config],
                    "globalStartTime": global_start,
                    "globalEndTime": global_end
                },
                "considerRoadTraffic": True,
                "populatePolylines": True,
            }
            
            print(f"\n=== Enviando request a Route Optimization API ===")
            print(f"Tipo viaje: {tipo_viaje}")
            print(f"Tipo hora: {tipo_hora_deseada} - {hora_base_local}")
            if tipo_hora_deseada == 'LLEGADA':
                print(f"  Ventana llegada: {hora_base_local} (+2 min máximo)")
            else:
                print(f"  Ventana salida: {hora_base_local} (+5 min máximo)")
            print(f"Shipments: {len(shipments)}")
            print(f"Vehículo capacidad: {vehiculo['capacidad']}")
            
            response = requests.post(base_url_optimization, headers=headers, json=data)
            
            if response.status_code == 200:
                resultado = response.json()
                print("Respuesta exitosa de la API")
                
                # Procesar la respuesta y crear el viaje
                viaje_creado = procesar_respuesta_api(
                    resultado, 
                    asignacion, 
                    punto_encuentro, 
                    tipo_viaje, 
                    hora_base_local.time(),
                    tipo_hora_deseada,
                    chofer, 
                    grupo
                )
                
                if viaje_creado:
                    viajes_creados.append(viaje_creado)
                    print(f"Viaje {idx} creado exitosamente")
                else:
                    print(f"No se pudo crear el viaje {idx}")
                
            else:
                print(f"=!= Error en API: {response.status_code}")
                print(f"Respuesta: {response.text}")
                print(f"Saltando asignación {idx}")
                
        except Exception as e:
            print(f"Error procesando asignación {idx}: {str(e)}")
            traceback.print_exc()
            print(f"Continuando con siguiente asignación...")
            continue
    
    # Si no se creó ningún viaje con API, usar fallback
    if not viajes_creados:
        print("\nNo se pudo crear ningún viaje con API")
        print("Usando método fallback sin API...")
        return crear_viajes_desde_asignaciones(
            asignaciones, 
            punto_encuentro, 
            tipo_viaje, 
            hora_base_local.time(), 
            tipo_hora_deseada, 
            grupo
        )
    
    print(f"\nTotal de viajes creados con API: {len(viajes_creados)}")
    return viajes_creados

def asignar_viajes(grupo, punto_encuentro, tipo_viaje="IDA", fecha_hora_deseada=None, tipo_hora_deseada='LLEGADA'):
    """
    Función principal que orquesta toda la asignación de viajes
    """
    print("===!=== INICIANDO ASIGNACION DE VIAJES ===!===")
    print(f"Tipo de viaje: {tipo_viaje}")
    print(f"Punto de encuentro: {punto_encuentro}")

    paraderos_deseados = agrupar_pasajeros_mismo_paradero(grupo)
    print(f"Paraderos únicos: {len(paraderos_deseados)}")

    detalles_vehiculos = obtener_detalles_vehiculos(grupo)
    print(f"Vehículos disponibles: {len(detalles_vehiculos)}")

    num_clusters = len(detalles_vehiculos)
    clusters = agrupar_paraderos_cercanos(paraderos_deseados, num_clusters)
    print(f"Clusters creados: {len(clusters)}")

    asignaciones = asignar_vehiculos_a_clusters(clusters, detalles_vehiculos)
    print(f"Asignaciones realizadas: {len(asignaciones)}")

    # AQUI CREO QUE SE DESVÍA TODA LA RUTA, Y DEBO HACER EL METODO ANTIGUO SI ES QUE LA API NO ESTA DISPONIBLE
    # y EL METODO CON API SI ESQUE ESTE ES 
    if API_EXISTE: # Metodo que utiliza api de Google Maps
        viajes = crear_viajes_desde_asignaciones_api(asignaciones, punto_encuentro, tipo_viaje, fecha_hora_deseada, tipo_hora_deseada, grupo)
    else: # Metodo fallback para crear viajes sin depender de la API (Contiene imperfecciones en las estimaciones ya que no considera calles y usa aproximaciones)
        viajes = crear_viajes_desde_asignaciones(asignaciones, punto_encuentro, tipo_viaje, fecha_hora_deseada, tipo_hora_deseada, grupo)


    print(f"Total viajes creados: {len(viajes)}")
    print("===!=== ASIGNACION COMPLETADA ===!===")

    ids_viajes = [v["viaje"].id_viaje for v in viajes]
    return ids_viajes

# Funcion para generar la imagen del mapa para visualizar
def generar_imagen_clusters(grupo, punto_encuentro, guardar_como="clusters_visualization.png"):
    """
    Genera una imagen estática de los clusters para presentación
    Guarda el archivo en la carpeta del proyecto
    """

    # Obtener datos
    paraderos_deseados = agrupar_pasajeros_mismo_paradero(grupo)
    detalles_vehiculos = obtener_detalles_vehiculos(grupo)
    num_clusters = len(detalles_vehiculos)
    clusters = agrupar_paraderos_cercanos(paraderos_deseados, num_clusters)

    # Construir URL
    api_key = settings.GOOGLE_MAPS_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/staticmap"

    # Parametros
    markers = []

    colores_clusters = [
        "blue",
        "green",
        "purple",
        "yellow",
        "orange",
        "brown",
        "gray",
        "black",
    ]
    # Agregar clusters (simplificado)
    for cluster_id, paraderos_cluster in clusters.items():
        color = colores_clusters[cluster_id % len(colores_clusters)]
        for p in paraderos_cluster:
            lat = float(p["paradero"].latitud)
            lng = float(p["paradero"].longitud)
            cantidad = p["cantidad"]
            label = str(cantidad) if cantidad < 10 else "9"
            markers.append(f"color:{color}|label:{label}|{lat},{lng}")

    # Punto de encuentro
    pe_lat = float(punto_encuentro.latitud)
    pe_lng = float(punto_encuentro.longitud)
    markers.append(f"color:red|size:large|{pe_lat},{pe_lng}")

    params = [
        ("size", "1400x900"),
        ("scale", "2"),
        ("maptype", "roadmap"),
        ("format", "png"),
        ("markers", markers),
        ("style", "feature:poi.business|visibility:off"),
        ("style", "feature:transit.station|visibility:off"),
        ("style", "feature:road|element:labels.icon|visibility:off"),
        ("style", "feature:all|saturation:-50|lightness:20"),
        ("key", api_key),
    ]

    response = requests.get(base_url, params=params)

    with open(guardar_como, "wb") as f:
        f.write(response.content)

    print(f"Imagen guardada: {guardar_como}")
    return guardar_como
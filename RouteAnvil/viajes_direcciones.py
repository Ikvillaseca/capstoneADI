import requests
import json
from django.conf import settings
from decimal import ROUND_HALF_UP, Decimal
from math import radians, sin, cos, sqrt, asin
from sklearn.cluster import KMeans
import numpy as np
from collections import defaultdict
import datetime
from .models import Viaje, Pasajero_Viaje, Parada_Viaje, Chofer, Vehiculo

#Verificar si la api funciona correctamente
def verificar_api_key():
    try:
        api_key = settings.GOOGLE_MAPS_API_KEY
        return api_key is not None and len(str(api_key).strip()) > 0
    except Exception:
        return False

API_EXISTE = verificar_api_key()



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

def crear_viajes_desde_asignaciones(asignaciones, punto_encuentro, tipo_viaje='IDA', hora_salida_base=None, grupo=None):
    """
    Crea objetos Viaje con sus paradas ordenadas
    tipo_viaje: 'IDA' (recoger) o 'VUELTA' (dejar)
    grupo: Grupo_Pasajeros al que pertenece este viaje
    #Punto encuentro: Destino si es IDA, Origen si es VUELTA

    """
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

def crear_viajes_desde_asignaciones_api(asignaciones, punto_encuentro, tipo_viaje='IDA', hora_salida_base=None, grupo=None):
    print("Trabajando con la api de google maps para crear viajes")



def asignar_viajes(grupo, punto_encuentro, tipo_viaje="IDA", hora_salida=None):
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
        viajes = crear_viajes_desde_asignaciones_api(asignaciones, punto_encuentro, tipo_viaje, hora_salida, grupo)
    else: # Metodo fallback para crear viajes sin depender de la API (Contiene imperfecciones en las estimaciones ya que no considera calles y usa aproximaciones)
        viajes = crear_viajes_desde_asignaciones(asignaciones, punto_encuentro, tipo_viaje, hora_salida, grupo)


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
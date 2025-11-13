import requests
import json
from django.conf import settings
from decimal import ROUND_HALF_UP, Decimal
from math import radians, sin, cos, sqrt, asin
from sklearn.cluster import KMeans
import numpy as np
from collections import defaultdict
import datetime
from .models import Vehiculo

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
    lista_vehiculos_grupo = grupo.chofer.select_related('id_vehiculo').all()
    #Necesito tener en cuenta siempre al chofer.id_chofer-datos_vehiculo
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



def asignar_viajes(grupo):
    print("===!=== INICIANDO ASIGNACION DE VIAJES ===!===")
    print(datetime.datetime.now())
    print(f"{grupo}")
    # Separar el problema en partes, primero necesito obtener los pasajeros del grupo

    # Mandar el grupo a la funcion que los agrupa cuando tienen el mismo paradero, asi reduzco los calculos
    paraderos_deseados = agrupar_pasajeros_mismo_paradero(grupo)

    # Obtengo un diccionario con id de paradero Y pasajeros que desean ese paradero

    # Probablemente me gustaria saber la capacidad de los vehiculos
    detalles_vehiculos = obtener_detalles_vehiculos(grupo)

    # Experimento con KMeans


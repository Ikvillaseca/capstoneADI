import requests
import json
from django.conf import settings
from decimal import ROUND_HALF_UP, Decimal
from math import radians, sin, cos, sqrt, asin
from collections import defaultdict

TIPO_PRIORIDAD= [
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

def agrupar_pasajeros_por_ruta(pasajeros, destino):
    """
    Agrupa pasajeros que tienen el mismo origen (o destino)
    Retorna: {(origen_id, destino_id): [lista_pasajeros]}
    """
    grupos = defaultdict(list)
    
    for pasajero in pasajeros:
        if pasajero.paradero_deseado and destino:
            clave = (
                str(pasajero.paradero_deseado.id_ubicacion),
                str(destino.id_ubicacion)
            )
            grupos[clave].append(pasajero)
    return dict(grupos)

def agrupar_pasajeros(grupos_rutas):
    print("=== Agrupando pasajeros ===")

    rutas = list(grupos_rutas.keys())


    calcular_distancias_haversine()

    pass


def asignar_viajes(grupo):
    print("===!=== Agrupando pasajeros ===!===")
    print(grupo)
    agrupar_pasajeros()
    print(grupo)


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
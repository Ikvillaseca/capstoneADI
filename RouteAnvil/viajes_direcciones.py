import requests
import json
from django.conf import settings
from decimal import ROUND_HALF_UP, Decimal

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
            return TIPO_PARADERO_MAP.get(tipo_prio, 'O')
    return 'O'



def calcular_distancia():
    pass

def agrupar_pasajeros():
    pass

def asignar_viajes():
    print("asignando")

def geocoding_desde_direccion(direccion):
    api_key = settings.GOOGLE_MAPS_API_KEY
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    params = {
        'address': direccion,
        'key': api_key,
        'language': 'es-419',
        'region': 'cl'
    }
    
    try:
        response = requests.get(url, params=params)
        #Caso en el que tenemos respuesta con exito
        if response.status_code == 200:
            data = response.json()
            #Guardar los datos de la respuesta para que no sean tan grandes las consultas
            datos_lugar = data['results'][0]
            #Obtener los datos que quiero de la response
            lat = datos_lugar['geometry']['location']['lat']
            lon = datos_lugar['geometry']['location']['lng']
            direccion = datos_lugar['formatted_address']
            tipos = datos_lugar['types']
            #Arreglar los distintos datos para que tengan el formato correcto
            lat = Decimal(str(lat)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
            lon = Decimal(str(lon)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
            direccion  = str(direccion)
            tipo = determinar_tipo_paradero(tipos)
            return lat, lon, direccion, tipo
        #Caso en el que hay una respuesta sin exito
        else:
            return None, None, None, None
    #Caso en el que ocurre un error
    except Exception as e:
        print(f"ERROR:\n{str(e)}")
        return None, None, None, None
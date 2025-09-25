from behave import given, when, then
from behave.api.pending_step import StepNotImplementedError

from features.environment import get_url

@given('Navegue a la pagina de {nombre_pagina}')
def step_impl(context, nombre_pagina):

    #Diccionario de urls para poder implementar urls que sean distintas al nombre de la pagina
    urls = {
        'inicio' : '/'
    }

    #Intenta buscar url usando el diccionario, o sino usa el nombre como path
    url = urls.get(nombre_pagina.lower(), f'/{nombre_pagina}/')
    full_url = get_url(context, url) #Utiliza la funcion get_url de environment.py
    print(f"Navegando a URL: {full_url}")
    context.browser.get(full_url)
    url_actual = context.browser.current_url
    assert url_actual == full_url

@given('Ingrese los datos de prueba de pasajero')
def step_impl(context):
    raise StepNotImplementedError(u'Given Ingrese los datos de prueba de pasajero')

@when('Agregue los datos de un pasajero')
def step_impl(context):
    raise StepNotImplementedError(u'When Ingrese los datos de prueba de pasajero')

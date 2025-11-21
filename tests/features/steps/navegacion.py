from behave import given, when, then
from features.environment import get_url
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

RUTAS = {
    "inicio": "/",
    "pasajeros": "/pasajeros/",
    "choferes": "/choferes/",
    "vehiculos": "/vehiculos/",
    "paraderos": "/paraderos/",
}

@given('El navegador esta abierto')
def step_impl(context):
    assert True

@when('Navegue a la pagina de {nombre_pagina}')
def step_impl(context, nombre_pagina):

    #Intenta buscar url usando el diccionario, o sino usa el nombre como path
    url = RUTAS.get(nombre_pagina.lower(), f'/{nombre_pagina}/')
    full_url = get_url(context, url) #Utiliza la funcion get_url de environment.py
    print(f"Navegando a URL: {full_url}")
    context.browser.get(full_url)
    url_actual = context.browser.current_url
    assert url_actual == full_url

@then('Observare que accedi a la pagina con titulo "{titulo}"')
def step_ver_titulo(context, titulo):
    real = context.browser.title.strip()
    assert real == titulo.strip(), f"Título esperado '{titulo}' pero real '{real}'"
from behave import given, when, then
from behave.api.pending_step import StepNotImplementedError
from selenium.webdriver.common.by import By

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


@when('Agregue los datos de un pasajero')
def step_impl(context):
    for fila in context.table:
        context.browser.find_element(By.CSS_SELECTOR, "a:nth-child(2) > button").click()
        context.browser.find_element(By.ID, "id_rut").click()
        context.browser.find_element(By.ID, "id_rut").send_keys("19083514-6")
        context.browser.find_element(By.ID, "id_nombre").click()
        context.browser.find_element(By.ID, "id_nombre").send_keys("Juanito")
        context.browser.find_element(By.ID, "id_apellido").click()
        context.browser.find_element(By.ID, "id_apellido").send_keys("Perez")
        context.browser.find_element(By.ID, "id_telefono").click()
        context.browser.find_element(By.ID, "id_telefono").send_keys("+56909021679")
        context.browser.find_element(By.ID, "id_empresa_trabajo").click()
        context.browser.find_element(By.ID, "id_empresa_trabajo").send_keys("Fontabella")
        context.browser.find_element(By.CSS_SELECTOR, "button").click()

@then('Observare que los pasajeros se agregaron a la lista')
def step_impl(context):
            raise StepNotImplementedError(u'Then Observare que los pasajeros se agregaron a la lista')

from behave import given, when, then
from behave.api.pending_step import StepNotImplementedError
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
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
    #Guardar los datos de prueba de la persona en el contexto
    context.datos_prueba_pasajero = []
    for fila in context.table:
        input_prueba_rut = fila['rut']
        input_prueba_nombre = fila['nombre']
        input_prueba_apellido = fila['apellido']
        input_prueba_telefono = fila['telefono']
        input_prueba_empresa_trabajo = fila['empresa_trabajo']

        persona_prueba = {
            'rut' : input_prueba_rut,
            'nombre' : input_prueba_nombre,
            'apellido' : input_prueba_apellido,
            'telefono' : input_prueba_telefono,
            'empresa_trabajo' : input_prueba_empresa_trabajo
        }

        wait = WebDriverWait(context.browser, 10) # Esperará hasta 10 segundos
        #Script para realizar las acciones - extraido de Selenium IDE
        try:
            context.browser.find_element(By.CSS_SELECTOR, "a:nth-child(2) > button").click()
            wait.until(EC.presence_of_element_located((By.ID, "id_rut")))
            context.browser.find_element(By.ID, "id_rut").click()
            context.browser.find_element(By.ID, "id_rut").send_keys(input_prueba_rut)
            context.browser.find_element(By.ID, "id_nombre").click()
            context.browser.find_element(By.ID, "id_nombre").send_keys(input_prueba_nombre)
            context.browser.find_element(By.ID, "id_apellido").click()
            context.browser.find_element(By.ID, "id_apellido").send_keys(input_prueba_apellido)
            context.browser.find_element(By.ID, "id_telefono").click()
            context.browser.find_element(By.ID, "id_telefono").send_keys(input_prueba_telefono)
            context.browser.find_element(By.ID, "id_empresa_trabajo").click()
            context.browser.find_element(By.ID, "id_empresa_trabajo").send_keys(input_prueba_empresa_trabajo)
            context.browser.find_element(By.CSS_SELECTOR, "button").click()

            context.datos_prueba_pasajero.append(persona_prueba)

            

        except TimeoutException:
            print("Timeout occurred while adding passenger data.")



@then('Observare que los pasajeros se agregaron a la lista')
def step_impl(context):
    print(context.datos_prueba_pasajero)
    raise StepNotImplementedError(u'Then Observare que los pasajeros se agregaron a la lista')

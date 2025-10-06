from behave import given, when, then
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
        #Extraigo los datos de la tabla en .feature
        input_prueba_rut = fila['rut']
        input_prueba_nombre = fila['nombre']
        input_prueba_apellido = fila['apellido']
        input_prueba_telefono = fila['telefono']
        input_prueba_empresa_trabajo = fila['empresa_trabajo']

        #Genero una persona de prueba con los datos de prueba para despues agregarlo a una lista y mandarlo al context de behave
        persona_prueba = {
            'rut' : input_prueba_rut,
            'nombre' : input_prueba_nombre,
            'apellido' : input_prueba_apellido,
            'telefono' : input_prueba_telefono,
            'empresa_trabajo' : input_prueba_empresa_trabajo
        }

        #Funcion para poder hacer que el enavegador espere hasta qeu ciertos elementos aparezcan
        wait = WebDriverWait(context.browser, 3) #Esperará hasta 3 segundos
        #Script para realizar las acciones - extraido de Selenium IDE
        try:
            #Ubicamos el boton para agregar pasajero
            #Utilizar element_to_be_clickable con cuidado
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/pasajero/crear/']")))
            context.browser.find_element(By.CSS_SELECTOR, "a[href='/pasajero/crear/']").click()
            #Verificamos que estamos en la pagina de crear pasajero
            wait.until(EC.presence_of_element_located((By.ID, "id_rut")))
            #Llenamos los datos del pasajero
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
            context.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            #Luego de clickear enviar, abre la pagina detalles, por lo tanto queremos volver a la pagina de lista
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn-secondary[href='/pasajeros/']")))
            context.browser.find_element(By.CSS_SELECTOR, "a.btn-secondary[href='/pasajeros/']").click()
            #Verificamos que llegamos a la pagina con la lista
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/pasajero/crear/']")))
            context.datos_prueba_pasajero.append(persona_prueba)
        except TimeoutException:
            print(f"Timeout mientras se intentó agregar pasajero {input_prueba_rut}")



@then('Observare que los pasajeros se agregaron a la lista')
def step_impl(context):
    
    tabla = context.browser.find_element(By.TAG_NAME, "table")
    texto_de_la_tabla = tabla.find_element(By.TAG_NAME, "tbody").text

    pasajeros_encontrados = 0
    for pasajero in context.datos_prueba_pasajero:
        rut = pasajero['rut']
        nombre = pasajero['nombre']
        print(f"## Buscando a '{nombre}' (RUT: {rut}) ##")
        # Comprobar si el RUT y el nombre están en el texto de la tabla
        if rut in texto_de_la_tabla and nombre in texto_de_la_tabla:
            pasajeros_encontrados += 1
    assert len(context.datos_prueba_pasajero) == pasajeros_encontrados
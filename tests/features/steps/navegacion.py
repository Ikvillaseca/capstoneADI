from behave import given, when, then
from features.environment import get_url
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@given('El navegador esta abierto')
def step_impl(context):
    assert True

@when('Navegue a la pagina de {nombre_pagina}')
def step_impl(context, nombre_pagina):

    #Diccionario de urls para poder implementar urls que sean distintas al nombre de la pagina
    urls = {
        "inicio": "/",
        "pasajeros": "/pasajeros/",
        "choferes": "/choferes/",
        "vehiculos": "/vehiculos/",
    }

    #Intenta buscar url usando el diccionario, o sino usa el nombre como path
    url = urls.get(nombre_pagina.lower(), f'/{nombre_pagina}/')
    full_url = get_url(context, url) #Utiliza la funcion get_url de environment.py
    print(f"Navegando a URL: {full_url}")
    context.browser.get(full_url)
    url_actual = context.browser.current_url
    assert url_actual == full_url

@then('Observare que accedi a la pagina con titulo "{titulo}"')
def step_impl(context, titulo):
    # Esperar a que la página cargue verificando que existe el titulo
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "title"))
    )
    
    title = context.browser.title #Obtiene el titulo del browser
    print(f"Titulo de la página: {title}")
    assert f"{titulo}" in title, f"El título '{title}' no contiene '{titulo}'" #Valida que el titulo sea igual
    print("Título verificado correctamente")
from behave import given, when, then
from features.environment import get_url
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@given('El navegador esta abierto')
def step_open_browser(context):
    assert True

@when('Navegue a la pagina de {nombre_pagina}')
def step_go_to_url(context, nombre_pagina):

    urls = {
        'inicio' : '/'
    }

    url = urls.get(nombre_pagina.lower(), f'/{nombre_pagina}/')

    full_url = get_url(context, url)
    print(f"Navegando a URL: {full_url}")
    context.browser.get(full_url)

@then('Observare que accedi a la pagina con titulo "{titulo}"')
def step_check_title(context, titulo):
    # Esperar a que la página cargue
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "title"))
    )
    
    title = context.browser.title
    print(f"Titulo de la página: {title}")
    assert f"{titulo}" in title, f"El título '{title}' no contiene '{titulo}'"
    print("Título verificado correctamente")
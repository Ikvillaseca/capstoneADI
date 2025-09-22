from behave import fixture, use_fixture
from selenium.webdriver import Firefox,Chrome
from os import getenv

@fixture
def browser_chrome(context):
    context.browser = Chrome()
    yield context.browser
    context.browser.quit()

def before_all(context):
    use_fixture(browser_chrome, context)

def get_url(context, path=""):
    #Intento obtener la url desde el entorno, 
    #O valor de la url al ejecutar "behave -D base_url="
    #O sino desde context
    #O sino la url por defecto de django
    base_url = (
        context.config.userdata.get('base_url') or 
        getenv('BASE_URL') or 
        getattr(context, 'base_url', None) or
        'http://127.0.0.1:8000'
    )
    #Helper para construir URLs completas
    if path.startswith('/'):
        url = f"{base_url}{path}"
    else:
        url = f"{base_url}/{path}"
    return url

#== Pruebas en Firefox
# def browser_firefox(context):
#     context.browser = Firefox()
#     yield context.browser
#     context.browser.quit()

# def before_all(context):
#     use_fixture(browser_firefox, context)
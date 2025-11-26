import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STEPS_DIR = os.path.join(BASE_DIR, "steps")
if STEPS_DIR not in sys.path:
    sys.path.append(STEPS_DIR)

from behave import fixture, use_fixture
from selenium.webdriver import Chrome #Firefox
from selenium.webdriver.chrome.options import Options
from os import getenv
import webbrowser
import os
import time
@fixture
def browser_chrome(context):
    chrome_options = Options()
    chrome_options.add_argument('--log-level=3')
    context.browser = Chrome(options=chrome_options)
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
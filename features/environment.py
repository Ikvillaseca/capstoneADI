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

    base_url = (
        context.config.userdata.get('base_url') or 
        getenv('BASE_URL') or 
        getattr(context, 'base_url', None) or
        'http://127.0.0.1:8000'
    )
    """Helper para construir URLs completas"""
    if path.startswith('/'):
        return f"{base_url}{path}"
    return f"{base_url}/{path}"


#== Pruebas en Firefox
# def browser_firefox(context):
#     context.browser = Firefox()
#     yield context.browser
#     context.browser.quit()

# def before_all(context):
#     use_fixture(browser_firefox, context)
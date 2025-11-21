from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from utils import safe_click, fill

@when('Agregue los datos de un vehiculo')
def step_agregar_vehiculo(context):
    context.datos_prueba_vehiculo = []
    wait = WebDriverWait(context.browser, 6)
    for fila in context.table:
        v = {h: fila[h].strip() for h in fila.headings}
        try:
            safe_click(context.browser, (By.CSS_SELECTOR, "a[href='/vehiculo/crear/']"))
            wait.until(EC.presence_of_element_located((By.ID, "id_patente")))
            fill(context.browser, (By.ID, "id_patente"), v['patente'])
            fill(context.browser, (By.ID, "id_marca"), v['marca'])
            fill(context.browser, (By.ID, "id_modelo"), v['modelo'])
            fill(context.browser, (By.ID, "id_anio"), v['anio'])
            fill(context.browser, (By.ID, "id_capacidad"), v['capacidad'])
            rev = context.browser.find_element(By.ID, "id_revision_tecnica")
            rev.send_keys(v['fecha_revision_tecnica']); rev.send_keys(Keys.TAB)
            prox = context.browser.find_element(By.ID, "id_proxima_revision")
            prox.send_keys(v['fecha_proximo_revision']); prox.send_keys(Keys.TAB)
            safe_click(context.browser, (By.CSS_SELECTOR, "button[type='submit']"))
            wait.until(EC.url_contains('/vehiculo/detalle/'))
            safe_click(context.browser, (By.CSS_SELECTOR, "a.btn-secondary[href='/vehiculos/']"))
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/vehiculo/crear/']")))
            context.datos_prueba_vehiculo.append(v)
        except TimeoutException as e:
            print(f"Timeout vehiculo {v['patente']}: {e}")
            raise

@then('Observare que los vehiculos se agregaron a la lista')
def step_verificar_vehiculos(context):
    WebDriverWait(context.browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    tbody = context.browser.find_element(By.TAG_NAME, "tbody").text
    encontrados = sum(1 for v in context.datos_prueba_vehiculo if v['patente'] in tbody and v['marca'] in tbody)
    assert encontrados == len(context.datos_prueba_vehiculo), f"Esperados {len(context.datos_prueba_vehiculo)}, encontrados {encontrados}"
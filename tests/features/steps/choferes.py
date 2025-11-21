from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from utils import safe_click, fill # ¡IMPORTANTE! Importa las funciones de ayuda

@when('Agregue los datos de un chofer')
def step_agregar_chofer(context):
    context.datos_prueba_chofer = []
    wait = WebDriverWait(context.browser, 6)

    for fila in context.table:
        c = {key.strip(): value.strip() for key, value in fila.items()}
        
        try:
            # 1. Click en "Registrar Chofer" de forma segura
            safe_click(context.browser, (By.CSS_SELECTOR, "a[href='/chofer/crear/']"))
            
            # 2. Espera a que el formulario cargue
            wait.until(EC.presence_of_element_located((By.ID, "id_rut")))

            # 3. Llena los campos
            fill(context.browser, (By.ID, "id_rut"), c['rut'])
            fill(context.browser, (By.ID, "id_nombre"), c['nombre'])
            fill(context.browser, (By.ID, "id_apellido"), c['apellido'])
            
            # 4. Selecciona la licencia
            sel = Select(context.browser.find_element(By.ID, "id_tipo_licencia"))
            sel.select_by_visible_text(c['tipo_licencia'])

            fill(context.browser, (By.ID, "id_direccion"), c['direccion'])
            
            # 5. Llena las fechas y cierra el datepicker
            fuc = context.browser.find_element(By.ID, "id_fecha_ultimo_control")
            fuc.send_keys(c['fecha_ultimo_control'])
            fuc.send_keys(Keys.TAB)

            fpc = context.browser.find_element(By.ID, "id_fecha_proximo_control")
            fpc.send_keys(c['fecha_proximo_control'])
            fpc.send_keys(Keys.TAB)

            # 6. Click en "Guardar" de forma segura
            safe_click(context.browser, (By.CSS_SELECTOR, "button[type='submit']"))
            
            # 7. Espera a que la página de detalle cargue
            wait.until(EC.url_contains('/chofer/detalle/'))

            # 8. Click en "Volver a la Lista" de forma segura
            safe_click(context.browser, (By.CSS_SELECTOR, "a.btn-secondary[href='/choferes/']"))
            
            # 9. Espera a estar de vuelta en la lista
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/chofer/crear/']")))
            
            context.datos_prueba_chofer.append(c)
        except TimeoutException as e:
            print(f"Timeout creando chofer {c['rut']}. Error: {e}")
            raise

@then('Observare que los choferes se agregaron a la lista')
def step_verificar_choferes(context):
    WebDriverWait(context.browser, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "tbody"))
    )
    tbody_text = context.browser.find_element(By.TAG_NAME, "tbody").text
    
    encontrados = sum(
        1 for c in context.datos_prueba_chofer
        if c['rut'] in tbody_text and c['nombre'] in tbody_text
    )
    
    assert encontrados == len(context.datos_prueba_chofer)
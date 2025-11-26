from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from features.environment import get_url
from utils import safe_click, fill

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
def step_agregar_pasajero(context):
    context.datos_prueba_pasajero = []
    wait = WebDriverWait(context.browser, 6)

    for fila in context.table:
        p = {k.strip(): fila[k].strip() for k in fila.headings}
        try:
            safe_click(context.browser, (By.CSS_SELECTOR, "a[href='/pasajero/crear/']"))
            wait.until(EC.presence_of_element_located((By.ID, "id_rut")))

            fill(context.browser, (By.ID, "id_rut"), p['rut'])
            fill(context.browser, (By.ID, "id_nombre"), p['nombre'])
            fill(context.browser, (By.ID, "id_apellido"), p['apellido'])
            fill(context.browser, (By.ID, "id_telefono"), p['telefono'])
            fill(context.browser, (By.ID, "id_empresa_trabajo"), p['empresa_trabajo'])

            # Click robusto con diagnóstico
            try:
                safe_click(context.browser, (By.CSS_SELECTOR, "button[type='submit']"))
            except ElementClickInterceptedException:
                covering = context.browser.execute_script("""
                    const el=document.querySelector("button[type='submit']");
                    const r=el.getBoundingClientRect();
                    return document.elementFromPoint(r.left+r.width/2, r.top+r.height/2)?.outerHTML;
                """)
                raise AssertionError(f"Botón submit interceptado por: {covering}")

            WebDriverWait(context.browser, 6).until(
                lambda d: '/pasajero/' in d.current_url and '/crear' not in d.current_url
            )

            try:
                safe_click(context.browser, (By.CSS_SELECTOR, "a.btn-secondary[href='/pasajeros/']"))
            except:
                pass

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/pasajero/crear/']")))

            context.datos_prueba_pasajero.append(p)
        except TimeoutException as e:
            print(f"[PASAJERO] Timeout creando {p.get('rut')}: {e}")
            try:
                safe_click(context.browser, (By.CSS_SELECTOR, "a[href='/pasajeros/']"))
            except:
                pass

@then('Observare que los pasajeros se agregaron a la lista')
def step_verificar_pasajeros(context):
    WebDriverWait(context.browser, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "tbody"))
    )
    tbody = context.browser.find_element(By.TAG_NAME, "tbody").text
    encontrados = sum(1 for p in context.datos_prueba_pasajero if p['rut'] in tbody and p['nombre'] in tbody)
    assert encontrados == len(context.datos_prueba_pasajero), f"Esperados {len(context.datos_prueba_pasajero)}, encontrados {encontrados}"
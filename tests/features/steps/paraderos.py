from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unicodedata

try:
    from utils import safe_click, fill
except ModuleNotFoundError:
    from steps.utils import safe_click, fill

def _normalizar(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s.lower())
        if unicodedata.category(c) != 'Mn'
    )

@when('Agregue los datos de un paradero')
def step_agregar_paradero(context):
    context.datos_prueba_paradero = []
    context.creados_paraderos = []  # nombres realmente creados
    wait = WebDriverWait(context.browser, 6)
    for fila in context.table:
        p = {
            'nombre': fila['nombre'].strip(),
            'direccion': fila['direccion'].strip(),
        }
        try:
            safe_click(context.browser, (By.CSS_SELECTOR, "a[href='/paradero/crear/']"))
            wait.until(EC.presence_of_element_located((By.ID, "id_nombre")))
            fill(context.browser, (By.ID, "id_nombre"), p['nombre'])
            fill(context.browser, (By.ID, "id_direccion"), p['direccion'])
            safe_click(context.browser, (By.CSS_SELECTOR, "button[type='submit']"))

            # Verificar si hubo errores en el formulario
            form_errors = context.browser.find_elements(By.CSS_SELECTOR, ".errorlist li")
            if form_errors:
                textos = [e.text for e in form_errors]
                print(f"[PARADERO] No creado '{p['nombre']}' por errores: {textos}")
                # Volver manualmente si quedó en crear
                if '/paradero/crear' in context.browser.current_url:
                    safe_click(context.browser, (By.CSS_SELECTOR, "a[href='/paraderos/']"))
                continue  # No agregar a creados

            # Esperar estar en detalle o lista (éxito)
            def _exito(d):
                u = d.current_url
                if '/paraderos/' in u and '/crear' not in u:
                    return True
                if '/paradero/' in u and '/crear' not in u:
                    return True
                try:
                    d.find_element(By.CSS_SELECTOR, "a.btn-secondary[href='/paraderos/']")
                    return True
                except:
                    return False

            try:
                WebDriverWait(context.browser, 6).until(_exito)
            except TimeoutException:
                current_url = context.browser.current_url
                print(f"[PARADERO] Timeout tras guardar '{p['nombre']}'. URL={current_url}")
                # Intentar volver y continuar
                try:
                    safe_click(context.browser, (By.CSS_SELECTOR, "a.btn-secondary[href='/paraderos/']"))
                except:
                    pass
                continue

            # Ir a la lista (si estamos en detalle)
            try:
                safe_click(context.browser, (By.CSS_SELECTOR, "a.btn-secondary[href='/paraderos/']"))
            except:
                pass

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/paradero/crear/']")))
            context.datos_prueba_paradero.append(p)        # esperados
            context.creados_paraderos.append(p['nombre'])  # realmente creados
        except TimeoutException as e:
            print(f"[PARADERO] Timeout creando '{p['nombre']}': {e}")
            # Intento volver para no romper siguiente ciclo
            try:
                safe_click(context.browser, (By.CSS_SELECTOR, "a[href='/paraderos/']"))
            except:
                pass
            # No agregar a listas
            continue

@then('Observare que los paraderos se agregaron a la lista')
def step_verificar_paraderos(context):
    WebDriverWait(context.browser, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "tbody"))
    )
    tbody_el = context.browser.find_element(By.TAG_NAME, "tbody")
    tbody_text = tbody_el.text
    print("[PARADERO] Contenido tbody:\n", tbody_text)

    norm_tbody = _normalizar(tbody_text)
    encontrados = []
    faltantes = []
    for p in context.datos_prueba_paradero:
        nombre_norm = _normalizar(p['nombre'])
        if nombre_norm in norm_tbody:
            encontrados.append(p['nombre'])
        else:
            faltantes.append(p['nombre'])

    print(f"[PARADERO] Esperados: {context.datos_prueba_paradero}")
    print(f"[PARADERO] Realmente creados: {context.creados_paraderos}")
    print(f"[PARADERO] Encontrados en lista: {encontrados}")
    print(f"[PARADERO] Faltantes en lista: {faltantes}")

    assert len(encontrados) == len(context.datos_prueba_paradero), (
        f"Esperados {len(context.datos_prueba_paradero)}, encontrados {len(encontrados)}. "
        f"Faltantes: {faltantes}. Ver consola para detalles."
    )
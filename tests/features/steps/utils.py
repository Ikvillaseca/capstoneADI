from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException

def safe_click(driver, locator, timeout=6):
    wait = WebDriverWait(driver, timeout)
    el = wait.until(EC.element_to_be_clickable(locator))
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        el.click()
    except ElementClickInterceptedException:
        el = driver.find_element(*locator)
        driver.execute_script("arguments[0].click();", el)
    except StaleElementReferenceException:
        el = driver.find_element(*locator)
        driver.execute_script("arguments[0].click();", el)

def fill(driver, locator, value):
    el = driver.find_element(*locator)
    el.clear()
    el.send_keys(value)
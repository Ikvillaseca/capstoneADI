import time
import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
SELENIUM_OK = True

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_OK = True
except Exception:
    SELENIUM_OK = False

@unittest.skipUnless(SELENIUM_OK, "Selenium/webdriver-manager no instalados (solo necesarios para tests)")
class PanelControlTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = Service(ChromeDriverManager().install())
        cls.browser = webdriver.Chrome(service=service, options=options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_panel_muestra_tarjetas(self):
        self.browser.get(self.live_server_url + "/")
        cards = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".stat-card"))
        )
        self.assertEqual(len(cards), 4)  # por si cambia el número de tarjetas

    def test_carrusel_visible(self):
        self.browser.get(self.live_server_url + "/")
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "transportCarousel"))
        )
        slides = self.browser.find_elements(By.CSS_SELECTOR, "#transportCarousel .carousel-item")
        self.assertGreaterEqual(len(slides), 1)

    def test_carrusel_avanza_automatico(self):
        self.browser.get(self.live_server_url + "/")
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "transportCarousel"))
        )
        slides = self.browser.find_elements(By.CSS_SELECTOR, "#transportCarousel .carousel-item")
        if len(slides) < 2:
            self.skipTest("Solo hay un slide en el carrusel")

        def active_index():
            items = self.browser.find_elements(By.CSS_SELECTOR, "#transportCarousel .carousel-item")
            for i, el in enumerate(items):
                if "active" in el.get_attribute("class").split():
                    return i
            return -1

        inicio = active_index()
        WebDriverWait(self.browser, 8).until(lambda d: active_index() != inicio)
        self.assertNotEqual(inicio, active_index())
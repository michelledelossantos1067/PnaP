from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class BasePage:
    """Clase base para todas las páginas - Page Object Model"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.url = ""
    
    def open(self):
        """Abre la URL de la página"""
        self.driver.get(self.url)
        time.sleep(0.5)  # Pequeña pausa para estabilidad
    
    def find_element(self, locator):
        """Encuentra un elemento con espera explícita"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Encuentra múltiples elementos"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click(self, locator):
        """Click en un elemento con espera"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        time.sleep(0.3)
    
    def enter_text(self, locator, text):
        """Ingresa texto en un campo"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        time.sleep(0.2)
    
    def get_text(self, locator):
        """Obtiene el texto de un elemento"""
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator, timeout=5):
        """Verifica si un elemento es visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """Verifica si un elemento está presente en el DOM"""
        try:
            self.find_element(locator)
            return True
        except:
            return False
    
    def get_current_url(self):
        """Retorna la URL actual"""
        return self.driver.current_url
    
    def take_screenshot(self, filename):
        """Toma captura de pantalla"""
        self.driver.save_screenshot(f"screenshots/{filename}")
    
    def scroll_to_element(self, locator):
        """Hace scroll hasta un elemento"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)
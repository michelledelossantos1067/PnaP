from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object para la página de Login"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-btn")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    ALERT_DANGER = (By.CLASS_NAME, "alert-danger")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:5000/login"
    
    def login(self, username, password):
        """Realiza login con usuario y contraseña"""
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def get_error_message(self):
        """Obtiene el mensaje de error"""
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except:
            return ""
    
    def click_login_button(self):
        """Click en botón de login sin llenar campos"""
        self.click(self.LOGIN_BUTTON)
    
    def enter_username(self, username):
        """Ingresa solo el usuario"""
        self.enter_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Ingresa solo la contraseña"""
        self.enter_text(self.PASSWORD_INPUT, password)
    
    def is_on_login_page(self):
        """Verifica si está en la página de login"""
        return "login" in self.driver.current_url
    
    def has_error_alert(self):
        """Verifica si hay alerta de error visible"""
        return self.is_element_visible(self.ALERT_DANGER, timeout=3)
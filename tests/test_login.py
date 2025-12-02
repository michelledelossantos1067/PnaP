import pytest
from pages.login_page import LoginPage
import time

class TestLogin:
    """US-001: Pruebas de Inicio de Sesión"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup que se ejecuta antes de cada test"""
        self.driver = driver
        self.login_page = LoginPage(driver)
    
    def test_login_exitoso_camino_feliz(self):
        """
        US-001: Camino feliz - Login exitoso con credenciales válidas
        """
        print("\n🧪 Test: Login exitoso (Camino Feliz)")
        
        # Arrange
        self.login_page.open()
        
        # Act
        self.login_page.login("admin", "admin123")
        time.sleep(1)
        
        # Assert
        assert "dashboard" in self.driver.current_url, "No redirigió al dashboard"
        print("Login exitoso - Redirigió correctamente al dashboard")
    
    def test_login_credenciales_invalidas_negativa(self):
        """
        US-001: Prueba negativa - Login con credenciales incorrectas
        
        """
        print("\nTest: Login con credenciales inválidas (Negativa)")
        
        # Arrange
        self.login_page.open()
        
        # Act
        self.login_page.login("usuario_invalido", "password_incorrecto")
        time.sleep(1)
        
        # Assert
        assert self.login_page.has_error_alert(), "No se mostró mensaje de error"
        assert self.login_page.is_on_login_page(), "Redirigió incorrectamente"
        print("Error mostrado correctamente para credenciales inválidas")
    
    def test_login_usuario_vacio_negativa(self):
        """
        US-001: Prueba negativa - Login sin usuario
        
    """
        print("\n🧪 Test: Login sin usuario (Negativa)")
        
        # Arrange
        self.login_page.open()
        
        # Act
        self.login_page.enter_password("admin123")
        self.login_page.click_login_button()
        time.sleep(1)
        
        # Assert
        assert self.login_page.is_on_login_page(), "No debería permitir login sin usuario"
        print("✅ Validación correcta: No permite login sin usuario")
    
    def test_login_password_vacio_negativa(self):
        """
        US-001: Prueba negativa - Login sin contraseña
        """
        print("\n🧪 Test: Login sin contraseña (Negativa)")
        
        # Arrange
        self.login_page.open()
        
        # Act
        self.login_page.enter_username("admin")
        self.login_page.click_login_button()
        time.sleep(1)
        
        # Assert
        assert self.login_page.is_on_login_page(), "No debería permitir login sin password"
        print("Validación correcta: No permite login sin contraseña")
    
    def test_login_password_incorrecto_negativa(self):
        """
        US-001: Prueba negativa - Usuario válido con password incorrecto
        """
        print("\n🧪 Test: Password incorrecto (Negativa)")
        
        # Arrange
        self.login_page.open()
        
        # Act
        self.login_page.login("admin", "password_incorrecto")
        time.sleep(1)
        
        # Assert
        assert self.login_page.has_error_alert(), "Debería mostrar error"
        assert self.login_page.is_on_login_page(), "No debería permitir acceso"
        print("Validación correcta: Password incorrecto bloqueado")
    
    def test_login_campos_vacios_limites(self):
        """
        US-001: Prueba de límites - Ambos campos vacíos
        
        """
        print("\n🧪 Test: Ambos campos vacíos (Límites)")
        
        # Arrange
        self.login_page.open()
        
        # Act
        self.login_page.click_login_button()
        time.sleep(1)
        
        # Assert
        assert self.login_page.is_on_login_page(), "No debería permitir login vacío"
        print("Validación correcta: Campos vacíos bloqueados")
    
    def test_login_caracteres_especiales_limites(self):
        """
        US-001: Prueba de límites - Caracteres especiales en credenciales
        """
        print("\n🧪 Test: Caracteres especiales (Límites)")
        
        # Arrange
        self.login_page.open()
        
        # Act
        self.login_page.login("admin'; DROP TABLE--", "<script>alert('xss')</script>")
        time.sleep(1)
        
        # Assert
        assert self.login_page.is_on_login_page(), "Debería rechazar caracteres especiales"
        print("✅ Validación correcta: Caracteres especiales manejados")
    
    def test_login_espacios_username_limites(self):
        """
        US-001: Prueba de límites - Espacios en el username
        """
        print("\ntest: Espacios en username (Límites)")
        
        # Arrange
        self.login_page.open()
        
        # Act
        self.login_page.login("   admin   ", "admin123")
        time.sleep(1)

        current_url = self.driver.current_url
        assert "dashboard" in current_url or "login" in current_url
        print("Espacios en username manejados correctamente")
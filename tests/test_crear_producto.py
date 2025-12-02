import pytest
from pages.login_page import LoginPage
from pages.productos_page import ProductosPage
import time

class TestCrearProducto:
    """US-002: Pruebas de Creación de Productos"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup: Login antes de cada test"""
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.productos_page = ProductosPage(driver)
        
        # Login automático
        self.login_page.open()
        self.login_page.login("admin", "admin123")
        time.sleep(1)
    
    def test_crear_producto_exitoso_camino_feliz(self):
        """
        US-002: Camino feliz """
        print("\nTest: Crear producto exitoso (Camino Feliz)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_producto = f"Producto Test {int(time.time())}"
        
        # Act
        self.productos_page.crear_producto(nombre_producto, 99.99, 10)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_exito(), "No se mostró mensaje de éxito"
        assert "productos" in self.driver.current_url, "No redirigió a lista"
        
        producto_encontrado = self.productos_page.buscar_producto_por_nombre(nombre_producto)
        assert producto_encontrado is not None, "Producto no aparece en la lista"
        print(f"Producto '{nombre_producto}' creado exitosamente")
    
    def test_crear_producto_campos_vacios_negativa(self):
        """
        US-002: Prueba negativa """
        print("\nTest: Crear producto con campos vacíos (Negativa)")
        
        # Arrange
        self.productos_page.open_crear()
        
        # Act 
        self.productos_page.crear_producto("", "", "")
        time.sleep(1)
        
        # Assert
        assert "crear" in self.driver.current_url, "No debería permitir crear sin datos"
        print("validación correcta: Campos vacíos bloqueados")
    
    def test_crear_producto_precio_negativo_negativa(self):
        """
        US-002: Prueba negativa """
        print("\n🧪 Test: Precio negativo rechazado (Negativa)")
        
        # Arrange
        self.productos_page.open_crear()
        
        # Act
        self.productos_page.crear_producto("Producto Precio Negativo", -50.00, 10)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_error(), "Debería mostrar error para precio negativo"
        print("Validación correcta: Precio negativo rechazado")
    
    def test_crear_producto_cantidad_negativa_negativa(self):
        """
        US-002: Prueba negativa """
        print("\n🧪 Test: Cantidad negativa rechazada (Negativa)")
        
        # Arrange
        self.productos_page.open_crear()
        
        # Act
        self.productos_page.crear_producto("Producto Cantidad Negativa", 50.00, -5)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_error(), "Debería mostrar error para cantidad negativa"
        print("Validación correcta: Cantidad negativa rechazada")
    
    def test_crear_producto_nombre_duplicado_negativa(self):
        """
        US-002: Prueba negativa """
        print("\nTest: Nombre duplicado rechazado (Negativa)")
        
        # Arrange 
        self.productos_page.open_crear()
        nombre_duplicado = f"Producto Duplicado {int(time.time())}"
        self.productos_page.crear_producto(nombre_duplicado, 100.00, 5)
        time.sleep(1)
        
        # Act 
        self.productos_page.open_crear()
        self.productos_page.crear_producto(nombre_duplicado, 200.00, 10)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_error(), "Debería mostrar error por nombre duplicado"
        print("Validación correcta: Nombre duplicado rechazado")
    
    def test_crear_producto_precio_cero_limites(self):
        """
        US-002: Prueba de límites
        """
        print("\nTest: Precio en cero (Límites)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_producto = f"Producto Gratis {int(time.time())}"
        
        # Act
        self.productos_page.crear_producto(nombre_producto, 0, 5)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_exito(), "Precio 0 debería ser válido"
        print("Producto con precio 0 creado correctamente")
    
    def test_crear_producto_cantidad_cero_limites(self):
        """
        US-002: Prueba de límites
        """
        print("\nTest: Cantidad en cero (Límites)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_producto = f"Producto Sin Stock {int(time.time())}"
        
        # Act
        self.productos_page.crear_producto(nombre_producto, 50.00, 0)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_exito(), "Cantidad 0 debería ser válida"
        print("Producto con cantidad 0 creado correctamente")
    
    def test_crear_producto_precio_muy_alto_limites(self):
        """
        US-002: Prueba de límites
        """
        print("\nTest: Precio muy alto (Límites)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_producto = f"Producto Costoso {int(time.time())}"
        
        # Act
        self.productos_page.crear_producto(nombre_producto, 999999.99, 1)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_exito(), "Precio alto debería ser aceptado"
        print("Producto con precio alto creado correctamente")
    
    def test_crear_producto_nombre_largo_limites(self):
        """
        US-002: Prueba de límites
        """
        print("\nTest: Nombre muy largo (Límites)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_largo = "A" * 100 
        
        # Act
        self.productos_page.crear_producto(nombre_largo, 50.00, 5)
        time.sleep(1)
        
        # Assert 
        url_actual = self.driver.current_url
        assert "productos" in url_actual or "crear" in url_actual
        print("Nombre largo manejado correctamente")
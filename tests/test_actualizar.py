import pytest
from pages.login_page import LoginPage
from pages.productos_page import ProductosPage
import time

class TestActualizarProducto:
    """US-004: Pruebas de Actualización de Productos"""
    
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
    
    def test_actualizar_producto_exitoso_camino_feliz(self):
        """
        US-004: Camino feliz """
        print("\nTest: Actualizar producto exitoso (Camino Feliz)")
        
        # Arrange 
        self.productos_page.open_crear()
        nombre_original = f"Producto Original {int(time.time())}"
        self.productos_page.crear_producto(nombre_original, 100.00, 10)
        time.sleep(1)
        
        # Act 
        self.productos_page.open_lista()
        time.sleep(1)
        self.productos_page.click_editar_producto(nombre_original)
        time.sleep(1)
        
        assert "editar" in self.driver.current_url, "No está en página de editar"
        
        nombre_nuevo = f"Producto Actualizado {int(time.time())}"
        self.productos_page.actualizar_producto(nombre_nuevo, 150.00, 20)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_exito(), "No se mostró mensaje de éxito"
        
        self.productos_page.open_lista()
        time.sleep(1)
        producto = self.productos_page.buscar_producto_por_nombre(nombre_nuevo)
        assert producto is not None, "Producto actualizado no aparece en lista"
        
        print(f"Producto actualizado de '{nombre_original}' a '{nombre_nuevo}'")
    
    def test_actualizar_producto_id_inexistente_negativa(self):
        """
        US-004: Prueba negativa """
        print("\n🧪 Test: ID inexistente (Negativa)")
        
        # Act 
        self.driver.get("http://localhost:5000/productos/editar/99999")
        time.sleep(1)
        
        # Assert
        page_source = self.driver.page_source.lower()
        assert "404" in page_source or "not found" in page_source, "Debería mostrar error 404"
        
        print("Error 404 mostrado correctamente para ID inexistente")
    
    def test_actualizar_producto_nombre_vacio_negativa(self):
        """
        US-004: Prueba negativa """
        print("\nTest: Nombre vacío en actualización (Negativa)")
        
        # Arrange 
        self.productos_page.open_crear()
        nombre_test = f"Producto Test {int(time.time())}"
        self.productos_page.crear_producto(nombre_test, 50.00, 5)
        time.sleep(1)
        
        # Act 
        self.productos_page.open_lista()
        time.sleep(1)
        self.productos_page.click_editar_producto(nombre_test)
        time.sleep(1)
        
        self.productos_page.actualizar_producto("", 60.00, 10)
        time.sleep(1)
        
        # Assert
        assert "editar" in self.driver.current_url or self.productos_page.tiene_mensaje_error(), \
            "Debería rechazar nombre vacío"
        
        print("Validación correcta: Nombre vacío rechazado")
    
    def test_actualizar_producto_precio_negativo_negativa(self):
        """
        US-004: Prueba negativa"""
        print("\nTest: Precio negativo en actualización (Negativa)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_test = f"Producto Test Precio {int(time.time())}"
        self.productos_page.crear_producto(nombre_test, 50.00, 5)
        time.sleep(1)
        
        # Act
        self.productos_page.open_lista()
        time.sleep(1)
        self.productos_page.click_editar_producto(nombre_test)
        time.sleep(1)
        
        self.productos_page.actualizar_producto(nombre_test, -100.00, 10)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_error(), "Debería mostrar error para precio negativo"
        
        print("Validación correcta: Precio negativo rechazado")
    
    def test_actualizar_producto_cantidad_negativa_negativa(self):
        """
        US-004: Prueba negativa
        """
        print("\nTest: Cantidad negativa en actualización (Negativa)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_test = f"Producto Test Cantidad {int(time.time())}"
        self.productos_page.crear_producto(nombre_test, 50.00, 5)
        time.sleep(1)
        
        # Act
        self.productos_page.open_lista()
        time.sleep(1)
        self.productos_page.click_editar_producto(nombre_test)
        time.sleep(1)
        
        self.productos_page.actualizar_producto(nombre_test, 50.00, -10)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_error(), "Debería mostrar error para cantidad negativa"
        
        print("Validación correcta: Cantidad negativa rechazada")
    
    def test_actualizar_producto_precio_cero_limites(self):
        """
        US-004: Prueba de límites
        """
        print("\nTest: Actualizar precio a cero (Límites)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_test = f"Producto Precio Cero {int(time.time())}"
        self.productos_page.crear_producto(nombre_test, 100.00, 5)
        time.sleep(1)
        
        # Act
        self.productos_page.open_lista()
        time.sleep(1)
        self.productos_page.click_editar_producto(nombre_test)
        time.sleep(1)
        
        self.productos_page.actualizar_producto(nombre_test, 0, 5)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_exito(), "Precio cero debería ser válido"
        
        print("Precio actualizado a cero correctamente")
    
    def test_actualizar_producto_cantidad_cero_limites(self):
        """
        US-004: Prueba de límites
        """
        print("\nTest: Actualizar cantidad a cero (Límites)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_test = f"Producto Cantidad Cero {int(time.time())}"
        self.productos_page.crear_producto(nombre_test, 50.00, 10)
        time.sleep(1)
        
        # Act
        self.productos_page.open_lista()
        time.sleep(1)
        self.productos_page.click_editar_producto(nombre_test)
        time.sleep(1)
        
        self.productos_page.actualizar_producto(nombre_test, 50.00, 0)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_exito(), "Cantidad cero debería ser válida"
        
        print("Cantidad actualizada a cero correctamente")
    
    def test_actualizar_producto_valores_extremos_limites(self):
        """
        US-004: Prueba de límites
        """
        print("\nTest: Valores extremos (Límites)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_test = f"Producto Extremos {int(time.time())}"
        self.productos_page.crear_producto(nombre_test, 50.00, 5)
        time.sleep(1)
        
        # Act
        self.productos_page.open_lista()
        time.sleep(1)
        self.productos_page.click_editar_producto(nombre_test)
        time.sleep(1)
        
        self.productos_page.actualizar_producto(nombre_test, 999999.99, 999999)
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_exito(), "Valores extremos válidos deberían ser aceptados"
        
        print("Valores extremos actualizados correctamente")
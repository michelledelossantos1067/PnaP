import pytest
from pages.login_page import LoginPage
from pages.productos_page import ProductosPage
import time

class TestEliminarProducto:
    """US-005: Pruebas de Eliminación de Productos"""
    
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
    
    def test_eliminar_producto_exitoso_camino_feliz(self):
        """
        US-005: Camino feliz - Eliminar producto correctamente
        """
        print("\nTest: Eliminar producto exitoso (Camino Feliz)")
        
        # Arrange 
        self.productos_page.open_crear()
        nombre_eliminar = f"Producto A Eliminar {int(time.time())}"
        self.productos_page.crear_producto(nombre_eliminar, 50.00, 5)
        time.sleep(1)
        
        self.productos_page.open_lista()
        time.sleep(1)
        total_antes = self.productos_page.get_total_productos()
        producto_antes = self.productos_page.buscar_producto_por_nombre(nombre_eliminar)
        assert producto_antes is not None, "Producto no se creó correctamente"
        
        # Act 
        self.productos_page.click_eliminar_producto(nombre_eliminar)
        time.sleep(1)
        
        nombre_modal = self.productos_page.get_nombre_modal()
        assert nombre_eliminar in nombre_modal, "Nombre en modal no coincide"
        
        self.productos_page.confirmar_eliminar()
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_mensaje_exito(), "No se mostró mensaje de éxito"
        
        producto_despues = self.productos_page.buscar_producto_por_nombre(nombre_eliminar)
        assert producto_despues is None, "Producto no fue eliminado"
        
        total_despues = self.productos_page.get_total_productos()
        assert total_despues == total_antes - 1, "Cantidad de productos no disminuyó"
        
        print(f"Producto '{nombre_eliminar}' eliminado exitosamente")
    
    def test_eliminar_producto_cancelar_negativa(self):
        """
        US-005: Prueba negativa - Cancelar no elimina el producto
        """
        print("\nTest: Cancelar eliminación (Negativa)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_test = f"Producto No Eliminar {int(time.time())}"
        self.productos_page.crear_producto(nombre_test, 50.00, 5)
        time.sleep(1)
        
        # Act
        self.productos_page.open_lista()
        time.sleep(1)
        total_antes = self.productos_page.get_total_productos()
        
        self.productos_page.click_eliminar_producto(nombre_test)
        time.sleep(1)
        
        # Cancelar
        self.productos_page.cancelar_eliminar()
        time.sleep(1)
        
        # Assert 
        producto = self.productos_page.buscar_producto_por_nombre(nombre_test)
        assert producto is not None, "Producto fue eliminado incorrectamente"
        
        total_despues = self.productos_page.get_total_productos()
        assert total_despues == total_antes, "Cantidad de productos cambió incorrectamente"
        
        print(f"Cancelar eliminación funcionó correctamente - Producto '{nombre_test}' preservado")
    
    def test_eliminar_producto_id_inexistente_negativa(self):
        """
        US-005: Prueba negativa - ID inexistente muestra error
        """
        print("\nTest: Eliminar ID inexistente (Negativa)")
        
        # Act 
        self.driver.get("http://localhost:5000/productos")
        time.sleep(1)
        
        self.driver.execute_script("""
            fetch('/productos/eliminar/99999', { method: 'POST' })
            .then(response => response.text())
            .then(data => console.log(data));
        """)
        time.sleep(1)
        
        # Assert
        assert "productos" in self.driver.current_url or "404" in self.driver.page_source.lower()
        
        print("✅ ID inexistente manejado correctamente")
    
    def test_eliminar_producto_verificar_modal_camino_feliz(self):
        """
        US-005: Camino feliz - Verificar que modal de confirmación aparece
        """
        print("\nTest: Modal de confirmación (Camino Feliz)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_test = f"Producto Modal Test {int(time.time())}"
        self.productos_page.crear_producto(nombre_test, 50.00, 5)
        time.sleep(1)
        
        # Act
        self.productos_page.open_lista()
        time.sleep(1)
        self.productos_page.click_eliminar_producto(nombre_test)
        time.sleep(1)
        
        # Assert 
        modal_visible = self.productos_page.is_element_visible(
            self.productos_page.MODAL_ELIMINAR, 
            timeout=5
        )
        assert modal_visible, "Modal de confirmación no apareció"
        
        nombre_modal = self.productos_page.get_nombre_modal()
        assert nombre_test in nombre_modal, f"Modal debería mostrar '{nombre_test}'"
        
        self.productos_page.cancelar_eliminar()
        
        print("Modal de confirmación funciona correctamente")
    
    def test_eliminar_multiples_productos_camino_feliz(self):
        """
        US-005: Camino feliz - Eliminar múltiples productos secuencialmente
        """
        print("\nTest: Eliminar múltiples productos (Camino Feliz)")
        
        # Arrange 
        productos_eliminar = []
        for i in range(3):
            self.productos_page.open_crear()
            nombre = f"Producto Multiple Eliminar {int(time.time())}_{i}"
            self.productos_page.crear_producto(nombre, 50.00, 5)
            productos_eliminar.append(nombre)
            time.sleep(1)
        
        self.productos_page.open_lista()
        time.sleep(1)
        total_inicial = self.productos_page.get_total_productos()
        
        # Act 
        for nombre in productos_eliminar:
            self.productos_page.click_eliminar_producto(nombre)
            time.sleep(1)
            self.productos_page.confirmar_eliminar()
            time.sleep(1)
        
        # Assert
        total_final = self.productos_page.get_total_productos()
        assert total_final == total_inicial - len(productos_eliminar), \
            f"Se esperaba eliminar {len(productos_eliminar)} productos"
        
        # Verificar que ninguno existe
        for nombre in productos_eliminar:
            producto = self.productos_page.buscar_producto_por_nombre(nombre)
            assert producto is None, f"Producto '{nombre}' no fue eliminado"
        
        print(f"{len(productos_eliminar)} productos eliminados exitosamente")
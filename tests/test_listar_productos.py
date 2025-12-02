import pytest
from pages.login_page import LoginPage
from pages.productos_page import ProductosPage
import time

class TestListarProductos:
    """US-003: Pruebas de Listado de Productos"""
    
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
    
    def test_listar_productos_exitoso_camino_feliz(self):
        """
        US-003: Camino feliz - Ver lista de todos los productos
        """
        print("\nTest: Listar productos exitoso (Camino Feliz)")
        
        # Arrange & Act
        self.productos_page.open_lista()
        time.sleep(1)
        
        # Assert
        assert self.productos_page.tiene_tabla_productos(), "No se muestra la tabla de productos"
        
        total = self.productos_page.get_total_productos()
        assert total >= 0, "Debería mostrar al menos 0 productos"
        
        print(f" Lista mostrando {total} productos correctamente")
    
    def test_listar_productos_con_datos_camino_feliz(self):
        """
        US-003: Camino feliz - Verificar que productos creados aparecen en lista
        """
        print("\nTest: Productos creados aparecen en lista (Camino Feliz)")
        
        # Arrange
        self.productos_page.open_crear()
        nombre_test = f"Producto Lista Test {int(time.time())}"
        self.productos_page.crear_producto(nombre_test, 75.00, 15)
        time.sleep(1)
        
        # Act 
        self.productos_page.open_lista()
        time.sleep(1)
        
        # Assert
        producto = self.productos_page.buscar_producto_por_nombre(nombre_test)
        assert producto is not None, f"Producto '{nombre_test}' no aparece en la lista"
        
        assert "Editar" in producto.text, "No se muestra botón Editar"
        assert "Eliminar" in producto.text, "No se muestra botón Eliminar"
        
        print(f" Producto '{nombre_test}' visible en lista con botones de acción")
    
    def test_listar_productos_vacio_negativa(self):
        """
        US-003: Prueba negativa - Lista vacía muestra mensaje apropiado
        
        """
        print("\n🧪 Test: Lista vacía (Negativa)")
        
        # Arrange & Act
        self.productos_page.open_lista()
        time.sleep(1)
        
        # Assert
        total = self.productos_page.get_total_productos()
        
        if total == 0:
            assert self.productos_page.tiene_mensaje_vacio(), "Debería mostrar mensaje de lista vacía"
            print("Mensaje de lista vacía mostrado correctamente")
        else:
            assert self.productos_page.tiene_tabla_productos(), "Debería mostrar tabla con productos"
            print(f"lista con {total} productos mostrada correctamente")
    
    def test_listar_productos_informacion_completa_camino_feliz(self):
        """
        US-003: Camino feliz - Verificar que se muestra toda la información del producto
        """
        print("\n Test: Información completa en lista (Camino Feliz)")
        
        # Arrange 
        self.productos_page.open_crear()
        nombre_test = f"Producto Completo {int(time.time())}"
        precio_test = 123.45
        cantidad_test = 20
        self.productos_page.crear_producto(nombre_test, precio_test, cantidad_test)
        time.sleep(1)
        
        # Act
        self.productos_page.open_lista()
        time.sleep(1)
        
        # Assert
        producto = self.productos_page.buscar_producto_por_nombre(nombre_test)
        assert producto is not None, "Producto no encontrado"
        
        texto_fila = producto.text
        assert nombre_test in texto_fila, "Nombre no visible"
        assert str(precio_test) in texto_fila or f"{precio_test:.2f}" in texto_fila, "Precio no visible"
        assert str(cantidad_test) in texto_fila, "Cantidad no visible"
        
        print("Toda la información del producto es visible en la lista")
    
    def test_listar_productos_multiples_camino_feliz(self):
        """
        US-003: Camino feliz - Listar múltiples productos
        """
        print("\nTest: Múltiples productos en lista (Camino Feliz)")
        
        # Arrange - Crear varios productos
        productos_test = []
        for i in range(3):
            self.productos_page.open_crear()
            nombre = f"Producto Multiple {int(time.time())}_{i}"
            self.productos_page.crear_producto(nombre, 50 + i * 10, 5 + i)
            productos_test.append(nombre)
            time.sleep(1)
        
        # Act
        self.productos_page.open_lista()
        time.sleep(1)
        
        # Assert
        for nombre in productos_test:
            producto = self.productos_page.buscar_producto_por_nombre(nombre)
            assert producto is not None, f"Producto '{nombre}' no encontrado"
        
        print(f"{len(productos_test)} productos mostrados correctamente en lista")
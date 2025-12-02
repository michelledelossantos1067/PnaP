from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class ProductosPage(BasePage):
    """Page Object para gestión de productos"""
    
    # Locators - Lista
    TABLA_PRODUCTOS = (By.ID, "tabla-productos")
    MENSAJE_VACIO = (By.CLASS_NAME, "mensaje-vacio")
    BTN_NUEVO_PRODUCTO = (By.LINK_TEXT, "+ Nuevo Producto")
    FILAS_PRODUCTOS = (By.CSS_SELECTOR, "tbody tr")
    BTN_EDITAR = (By.CLASS_NAME, "btn-editar")
    BTN_ELIMINAR = (By.CLASS_NAME, "btn-eliminar")
    
    # Locators - Formulario Crear/Editar
    INPUT_NOMBRE = (By.ID, "nombre")
    INPUT_PRECIO = (By.ID, "precio")
    INPUT_CANTIDAD = (By.ID, "cantidad")
    BTN_GUARDAR = (By.ID, "btn-guardar")
    BTN_ACTUALIZAR = (By.ID, "btn-actualizar")
    ALERT_SUCCESS = (By.CLASS_NAME, "alert-success")
    ALERT_DANGER = (By.CLASS_NAME, "alert-danger")
    
    # Locators - Modal Eliminar
    MODAL_ELIMINAR = (By.ID, "modalEliminar")
    BTN_CONFIRMAR_ELIMINAR = (By.ID, "btn-confirmar-eliminar")
    BTN_CANCELAR = (By.ID, "btn-cancelar")
    PRODUCTO_NOMBRE_MODAL = (By.ID, "producto-nombre-modal")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url_lista = "http://localhost:5000/productos"
        self.url_crear = "http://localhost:5000/productos/crear"
    
    # Métodos - Lista
    def open_lista(self):
        """Abre la página de lista de productos"""
        self.driver.get(self.url_lista)
        time.sleep(0.5)
    
    def open_crear(self):
        """Abre formulario de crear producto"""
        self.driver.get(self.url_crear)
        time.sleep(0.5)
    
    def get_total_productos(self):
        """Cuenta total de productos en la tabla"""
        try:
            filas = self.find_elements(self.FILAS_PRODUCTOS)
            return len(filas)
        except:
            return 0
    
    def click_nuevo_producto(self):
        """Click en botón nuevo producto"""
        self.click(self.BTN_NUEVO_PRODUCTO)
    
    def buscar_producto_por_nombre(self, nombre):
        """Busca un producto por nombre en la tabla"""
        filas = self.find_elements(self.FILAS_PRODUCTOS)
        for fila in filas:
            if nombre in fila.text:
                return fila
        return None
    
    def click_editar_producto(self, nombre):
        """Click en editar de un producto específico"""
        fila = self.buscar_producto_por_nombre(nombre)
        if fila:
            btn_editar = fila.find_element(By.CLASS_NAME, "btn-editar")
            btn_editar.click()
            time.sleep(0.5)
    
    def click_eliminar_producto(self, nombre):
        """Click en eliminar de un producto específico"""
        fila = self.buscar_producto_por_nombre(nombre)
        if fila:
            btn_eliminar = fila.find_element(By.CLASS_NAME, "btn-eliminar")
            btn_eliminar.click()
            time.sleep(0.5)
    
    # Métodos - Formulario
    def crear_producto(self, nombre, precio, cantidad):
        """Crea un nuevo producto"""
        self.enter_text(self.INPUT_NOMBRE, nombre)
        self.enter_text(self.INPUT_PRECIO, str(precio))
        self.enter_text(self.INPUT_CANTIDAD, str(cantidad))
        self.click(self.BTN_GUARDAR)
        time.sleep(0.5)
    
    def actualizar_producto(self, nombre, precio, cantidad):
        """Actualiza un producto existente"""
        self.enter_text(self.INPUT_NOMBRE, nombre)
        self.enter_text(self.INPUT_PRECIO, str(precio))
        self.enter_text(self.INPUT_CANTIDAD, str(cantidad))
        self.click(self.BTN_ACTUALIZAR)
        time.sleep(0.5)
    
    def get_nombre_producto(self):
        """Obtiene valor del campo nombre"""
        return self.find_element(self.INPUT_NOMBRE).get_attribute("value")
    
    def get_precio_producto(self):
        """Obtiene valor del campo precio"""
        return self.find_element(self.INPUT_PRECIO).get_attribute("value")
    
    def get_cantidad_producto(self):
        """Obtiene valor del campo cantidad"""
        return self.find_element(self.INPUT_CANTIDAD).get_attribute("value")
    
    # Métodos - Modal
    def confirmar_eliminar(self):
        """Confirma la eliminación en el modal"""
        self.click(self.BTN_CONFIRMAR_ELIMINAR)
        time.sleep(0.5)
    
    def cancelar_eliminar(self):
        """Cancela la eliminación en el modal"""
        self.click(self.BTN_CANCELAR)
        time.sleep(0.5)
    
    def get_nombre_modal(self):
        """Obtiene el nombre del producto en el modal"""
        return self.get_text(self.PRODUCTO_NOMBRE_MODAL)
    
    # Métodos - Validación
    def tiene_mensaje_exito(self):
        """Verifica si hay mensaje de éxito"""
        return self.is_element_visible(self.ALERT_SUCCESS, timeout=3)
    
    def tiene_mensaje_error(self):
        """Verifica si hay mensaje de error"""
        return self.is_element_visible(self.ALERT_DANGER, timeout=3)
    
    def tiene_tabla_productos(self):
        """Verifica si la tabla de productos está presente"""
        return self.is_element_present(self.TABLA_PRODUCTOS)
    
    def tiene_mensaje_vacio(self):
        """Verifica si aparece mensaje de lista vacía"""
        return self.is_element_visible(self.MENSAJE_VACIO, timeout=3)
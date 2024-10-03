class BrazoRobotico:
    def __init__(self, nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje):
        self.nombre_maquina = nombre_maquina
        self.cantidad_lineas = cantidad_lineas
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.cabeza_productos = None
        self.siguiente = None
        
    def agregar_producto(self, producto):
        if not self.cabeza_productos:
            self.cabeza_productos = producto
        else:
            actual = self.cabeza_productos
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = producto
            
    def obtener_productos(self):
        actual = self.cabeza_productos
        while actual:
            yield actual
            actual = actual.siguiente
class BrazoRobotico:
    def __init__(self, nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje):
        self.nombre_maquina = nombre_maquina
        self.cantidad_lineas = cantidad_lineas
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.cabeza = None
        self.siguiente = None

    def agregar_producto(self, nodo_producto):
        if not self.cabeza:
            self.cabeza = nodo_producto
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nodo_producto
            
    def obtener_productos(self):
        actual = self.cabeza
        while actual:
            yield actual
            actual = actual.siguiente

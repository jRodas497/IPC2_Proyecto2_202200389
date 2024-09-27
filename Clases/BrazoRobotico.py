from Clases.Productos import Productos

class BrazoRobotico:
    def __init__(self, nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje):
        self.nombre_maquina = nombre_maquina
        self.cantidad_lineas = cantidad_lineas
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.productos = Productos(None)
        self.posicion_actual = 0  # Posición inicial del brazo
        self.ensamblando = False

    def agregar_producto(self, nombre_producto):
        self.productos = Productos(nombre_producto)

    def mover_a(self, posicion):
        tiempo_movimiento = abs(self.posicion_actual - posicion)
        self.posicion_actual = posicion
        return tiempo_movimiento

    def ensamblar(self):
        if self.ensamblando:
            return 0  # Si ya está ensamblando, no hacer nada
        self.ensamblando = True
        tiempo_ensamblaje = self.tiempo_ensamblaje
        self.ensamblando = False
        return tiempo_ensamblaje
    
    def ensamblar_productos(self):
        for producto in self.productos:
            tiempo_total = producto.ensamblar(self)
            print(f"Tiempo total de ensamblaje para {producto.nombre}: {tiempo_total} segundos")
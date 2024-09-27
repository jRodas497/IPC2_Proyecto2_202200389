from Clases.Elaboracion import Elaboracion

class Nodo:
    def __init__(self, nombre_producto):
        self.nombre_producto = nombre_producto
        self.elaboracion = Elaboracion()
        self.siguiente = None

    def agregar_paso(self, paso_cadena):
        self.elaboracion = Elaboracion(conjunto=paso_cadena)
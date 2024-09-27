from Clases.Elaboracion import Elaboracion
from Listas.Nodo import Nodo

class Productos:
    def __init__(self, nombre):
        self.nombre = nombre
        self.pasos = None

    def agregar_paso(self, paso):
        nuevo_paso = Nodo(paso)
        if self.pasos is None:
            self.pasos = nuevo_paso
            nuevo_paso.siguiente = nuevo_paso  # La lista es circular
        else:
            actual = self.pasos
            while actual.siguiente != self.pasos:
                actual = actual.siguiente
            actual.siguiente = nuevo_paso
            nuevo_paso.siguiente = self.pasos

    def ensamblar(self, brazo_robotico):
        tiempo_total = 0
        actual = self.pasos
        if actual is None:
            return tiempo_total
        while True:
            paso = actual.paso
            # Aquí puedes descomponer el paso en línea y columna si es necesario
            tiempo_movimiento = brazo_robotico.mover_a(paso)
            tiempo_ensamblaje = brazo_robotico.ensamblar()
            tiempo_total += tiempo_movimiento + tiempo_ensamblaje
            actual = actual.siguiente
            if actual == self.pasos:
                break
        return tiempo_total
from Clases.Elaboracion import Elaboracion

class Productos:
    def __init__(self, nombre):
        self.nombre = nombre
        self.elaboracion = None

    def agregar_paso(self, paso, conjunto):
        self.elaboracion = Elaboracion(paso, conjunto)

    def ensamblar(self, lineas_ensamblaje, ensamblando):
        tiempo_total = 0
        if self.elaboracion:
            linea_id, componente_id = self.elaboracion.linea, self.elaboracion.componente
            linea = lineas_ensamblaje.obtener(linea_id)
            componente = linea.obtener_componente(componente_id)
            tiempo_movimiento = linea.brazo_robotico.mover_a(componente_id)
            tiempo_total += tiempo_movimiento
            tiempo_ensamblaje = linea.brazo_robotico.ensamblar(componente, ensamblando)
            tiempo_total += tiempo_ensamblaje
        return tiempo_total
class Producto:
    def __init__(self, nombre, instrucciones):
        self.nombre = nombre
        self.instrucciones = instrucciones

    def ensamblar(self, lineas_ensamblaje, ensamblando):
        tiempo_total = 0
        for instruccion in self.instrucciones:
            linea_id, componente_id = instruccion
            linea = lineas_ensamblaje.obtener(linea_id)
            componente = linea.obtener_componente(componente_id)
            tiempo_movimiento = linea.brazo_robotico.mover_a(componente_id)
            tiempo_total += tiempo_movimiento
            tiempo_ensamblaje = linea.brazo_robotico.ensamblar(componente, ensamblando)
            tiempo_total += tiempo_ensamblaje
        return tiempo_total
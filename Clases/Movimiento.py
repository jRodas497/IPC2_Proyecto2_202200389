class Movimiento:
    def __init__(self, tiempo, linea, componente, accion):
        self.tiempo = tiempo
        self.linea = linea
        self.componente = componente
        self.accion = accion
        self.siguiente = None
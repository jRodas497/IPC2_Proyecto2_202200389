class BrazoRobotico:
    def __init__(self):
        self.posicion_actual = 0

    def mover_a(self, posicion):
        tiempo_movimiento = abs(self.posicion_actual - posicion)
        self.posicion_actual = posicion
        return tiempo_movimiento

    def ensamblar(self, componente, ensamblando):
        while ensamblando[0]:
            pass 
        ensamblando[0] = True
        tiempo_ensamblaje = componente.tiempo_ensamblaje
        ensamblando[0] = False
        return tiempo_ensamblaje
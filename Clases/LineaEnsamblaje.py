from Listas.ListaEnlazada import ListaEnlazada
from .BrazoRobotico import BrazoRobotico

class LineaEnsamblaje:
    def __init__(self, id):
        self.id = id
        self.componentes = ListaEnlazada()
        self.brazo_robotico = BrazoRobotico()

    def agregar_componente(self, componente):
        self.componentes.agregar(componente)

    def obtener_componente(self, indice):
        return self.componentes.obtener(indice)
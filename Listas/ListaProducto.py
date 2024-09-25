from Listas.Nodo import Nodo

class ListaProductos:
    def __init__(self):
        self.cabeza = None

    def agregar(self, producto):
        nuevo_nodo = Nodo(producto)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener(self, indice):
        actual = self.cabeza
        contador = 0
        while actual:
            if contador == indice:
                return actual.dato
            actual = actual.siguiente
            contador += 1
        return None
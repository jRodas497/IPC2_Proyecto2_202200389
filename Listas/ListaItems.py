from Listas.NodoItem import NodoItem

class ListaItems:
    def __init__(self):
        self.cabeza = None

    def agregar(self, item):
        nuevo_nodo = NodoItem(item)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_todos(self):
        actual = self.cabeza
        while actual:
            yield actual.item
            actual = actual.siguiente

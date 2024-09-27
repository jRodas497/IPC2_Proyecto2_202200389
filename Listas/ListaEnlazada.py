from .Nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza 
        else:
            actual = self.cabeza
            while actual.siguiente != self.cabeza:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza

    def obtener(self, indice):
        actual = self.cabeza
        contador = 0
        while actual:
            if contador == indice:
                return actual.dato
            actual = actual.siguiente
            contador += 1
        return None
    
    def __iter__(self):
        self.actual = self.cabeza
        return self

    def __next__(self):
        if self.actual:
            dato = self.actual.dato
            self.actual = self.actual.siguiente
            return dato
        else:
            raise StopIteration
        
    def mostrar(self):
        if self.cabeza is None:
            return
        actual = self.cabeza
        while True:
            pasos_str = f"L{actual.elaboracion.linea}C{actual.elaboracion.componente}" if actual.elaboracion.linea is not None else "No pasos"
            print(f"Producto: {actual.nombre_producto}, Pasos: {pasos_str}")
            actual = actual.siguiente
            if actual == self.cabeza:
                break
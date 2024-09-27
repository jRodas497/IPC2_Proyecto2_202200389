from Listas.Nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self.primero = None

    def agregar(self, elemento):
        if isinstance(elemento, Nodo):
            nuevo = elemento
        else:
            nuevo = Nodo(elemento)

        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
            nuevo.siguiente = nuevo 
        else:
            actual = self.primero
            while actual.siguiente != self.primero:
                actual = actual.siguiente
            actual.siguiente = nuevo
            nuevo.siguiente = self.primero

    def obtener(self, indice):
        actual = self.primero
        contador = 0
        while actual:
            if contador == indice:
                return actual
            actual = actual.siguiente
            contador += 1
        return None
    
    def mostrar(self):
        if self.primero is None:
            return
        actual = self.primero
        while True:
            pasos_str = f"L{actual.elaboracion.linea}C{actual.elaboracion.componente}" if actual.elaboracion.linea is not None else "No pasos"
            print(f"Producto: {actual.nombre_producto}, Pasos: {pasos_str}")
            actual = actual.siguiente
            if actual == self.primero:
                break
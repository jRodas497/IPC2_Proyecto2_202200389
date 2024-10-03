class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, brazo_robotico):
        if not self.cabeza:
            self.cabeza = brazo_robotico
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = brazo_robotico

    def obtener(self, indice):
        actual = self.cabeza
        contador = 0
        while actual:
            if contador == indice:
                return actual
            actual = actual.siguiente
            contador += 1
        return None
    
    def contar(self):
        actual = self.cabeza
        contador = 0
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador
    
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
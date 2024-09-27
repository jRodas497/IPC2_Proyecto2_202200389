from Listas.Nodo import Nodo

class ListaProductos:
    def __init__(self):
        self.cabeza = None
        self.size = 0

    def agregar(self, producto):
        nuevo_nodo = Nodo(dato = producto)
        
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.size += 1
            return 
        
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
            
        actual.siguiente = nuevo_nodo
        self.size += 1
        
    def __iter__(self):
        self.actual = self.cabeza
        return self

    def __next__(self):
        if self.actual is not None:
            valor_actual = self.actual.dato
            self.actual = self.actual.siguiente
            return valor_actual
        else:
            raise StopIteration
        
    def obtener_size(self):
        return self.size
    
    def listar(self):
        print("TOTAL PRODUCTOS:", self.size)
        print("")

        actual = self.cabeza
        while actual != None:
            print("Altura:", actual.dato.nombre, "| Valor:", actual.dato.elaboracion)
            actual = actual.siguiente
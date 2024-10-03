from Listas.NodoElaboracion import NodoElaboracion

class NodoProducto:
    def __init__(self, nombre_producto):
        self.nombre_producto = nombre_producto
        self.cabeza_pasos = None
        self.siguiente = None

    def agregar_paso(self, linea, componente):
        nuevo_paso = NodoElaboracion(linea, componente)
        if not self.cabeza_pasos:
            self.cabeza_pasos = nuevo_paso
        else:
            actual = self.cabeza_pasos
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_paso
            
    def obtener_pasos(self):
        actual = self.cabeza_pasos
        while actual:
            yield actual.linea, actual.componente
            actual = actual.siguiente
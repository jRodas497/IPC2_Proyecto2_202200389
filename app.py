from tkinter import filedialog
import xml.etree.ElementTree as ET
import threading

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
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

class BrazoRobotico:
    def __init__(self):
        self.posicion_actual = 0

    def mover_a(self, posicion):
        tiempo_movimiento = abs(self.posicion_actual - posicion)
        self.posicion_actual = posicion
        return tiempo_movimiento

    def ensamblar(self, componente, lock):
        lock.acquire()
        try:
            tiempo_ensamblaje = componente.tiempo_ensamblaje
        finally:
            lock.release()
        return tiempo_ensamblaje

class Componente:
    def __init__(self, id, tiempo_ensamblaje):
        self.id = id
        self.tiempo_ensamblaje = tiempo_ensamblaje

class LineaEnsamblaje:
    def __init__(self, id):
        self.id = id
        self.componentes = ListaEnlazada()
        self.brazo_robotico = BrazoRobotico()

    def agregar_componente(self, componente):
        self.componentes.agregar(componente)

    def obtener_componente(self, indice):
        componente = self.componentes.obtener(indice)
        if componente is None:
            raise ValueError(f"Componente en el índice {indice} no encontrado en la línea {self.id}")
        return componente

class Producto:
    def __init__(self, nombre, instrucciones):
        self.nombre = nombre
        self.instrucciones = instrucciones

    def ensamblar(self, lineas_ensamblaje, lock):
        tiempo_total = 0
        for instruccion in self.instrucciones:
            linea_id, componente_id = instruccion
            linea = lineas_ensamblaje.obtener(linea_id)
            componente = linea.obtener_componente(componente_id)
            tiempo_movimiento = linea.brazo_robotico.mover_a(componente_id)
            tiempo_total += tiempo_movimiento
            tiempo_ensamblaje = linea.brazo_robotico.ensamblar(componente, lock)
            tiempo_total += tiempo_ensamblaje
        return tiempo_total

def abrir_archivo():
    print("Abriendo el cuadro de diálogo para seleccionar un archivo...")
    ruta = filedialog.askopenfilename(filetypes=[("Archivo XML", "*.xml")])
    if ruta:
        print(f"Archivo seleccionado: {ruta}")
        try:
            with open(ruta, 'r', encoding='utf-8') as file:
                txt = file.read()
                print("Contenido del archivo:")
                print()
                print("--------------------------------------------------")
                print(txt)
                print("--------------------------------------------------")
                print()
            
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            
        return ruta

def leerArchivoET():
    rutaArchivo = abrir_archivo()
    tree = ET.parse(rutaArchivo)
    root = tree.getroot()
    
    lineas_ensamblaje = ListaEnlazada()
    productos = ListaProductos()

    for maquina in root.findall('Maquina'):
        cantidad_lineas = int(maquina.find('CantidadLineasProduccion').text)
        cantidad_componentes = int(maquina.find('CantidadComponentes').text)

        for i in range(1, cantidad_lineas + 1):
            nueva_linea = LineaEnsamblaje(i)
            for j in range(cantidad_componentes):
                tiempo_ensamblaje = int(maquina.find('TiempoEnsamblaje').text)
                nuevo_componente = Componente(j, tiempo_ensamblaje)
                nueva_linea.agregar_componente(nuevo_componente)
            lineas_ensamblaje.agregar(nueva_linea)

        for producto in maquina.find('ListadoProductos').findall('Producto'):
            nombre_producto = producto.find('nombre').text
            instrucciones = ListaEnlazada()
            for instruccion in producto.find('elaboracion').text.split():
                linea_id, componente_id = map(int, instruccion[1:].split('C'))
                instrucciones.agregar((linea_id, componente_id))
            nuevo_producto = Producto(nombre_producto, instrucciones)
            productos.agregar(nuevo_producto)

    return lineas_ensamblaje, productos

lineas_ensamblaje, productos = leerArchivoET()

lock = threading.Lock()

indice_producto = 0
producto = productos.obtener(indice_producto)
while producto:
    tiempo_total = producto.ensamblar(lineas_ensamblaje, lock)
    print(f"Tiempo total de ensamblaje para {producto.nombre}: {tiempo_total} segundos")
    indice_producto += 1
    producto = productos.obtener(indice_producto)
from tkinter import filedialog
from flask import Flask, render_template, request, redirect, url_for, render_template_string
from werkzeug.utils import secure_filename
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)
ITEMS_PER_PAGE = 10
    
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

class NodoElaboracion:
    def __init__(self, linea, componente):
        self.linea = linea
        self.componente = componente
        self.siguiente = None

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

class BrazoRobotico:
    def __init__(self, nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje):
        self.nombre_maquina = nombre_maquina
        self.cantidad_lineas = cantidad_lineas
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.cabeza_productos = None
        self.siguiente = None
        
    def agregar_producto(self, producto):
        if not self.cabeza_productos:
            self.cabeza_productos = producto
        else:
            actual = self.cabeza_productos
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = producto
            
    def obtener_productos(self):
        actual = self.cabeza_productos
        while actual:
            yield actual
            actual = actual.siguiente

class Movimiento:
    def __init__(self, tiempo, linea, componente, accion):
        self.tiempo = tiempo
        self.linea = linea
        self.componente = componente
        self.accion = accion
        self.siguiente = None

class NodoItem:
    def __init__(self, item):
        self.item = item
        self.siguiente = None

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

#---------------- FUNCIONES PYTHON ------------------

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
    
def leerArchivoET(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    lineas_ensamblaje = ListaEnlazada()

    for maquina in root.findall('Maquina'):
        nombre_maquina = maquina.find('NombreMaquina').text.strip()
        cantidad_lineas = int(maquina.find('CantidadLineasProduccion').text.strip())
        cantidad_componentes = int(maquina.find('CantidadComponentes').text.strip())
        tiempo_ensamblaje = int(maquina.find('TiempoEnsamblaje').text.strip())

        brazo_robotico = BrazoRobotico(nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje)

        for producto in maquina.find('ListadoProductos').findall('Producto'):
            nombre_producto = producto.find('nombre').text.strip()
            nodo_producto = NodoProducto(nombre_producto)
            instrucciones = producto.find('elaboracion').text.strip().split()
            for instruccion in instrucciones:
                linea = int(instruccion[1])  # Extraer el número de línea
                componente = int(instruccion[3])  # Extraer el número de componente
                nodo_producto.agregar_paso(linea, componente)
            brazo_robotico.agregar_producto(nodo_producto)

        lineas_ensamblaje.agregar(brazo_robotico)  # Agregar la máquina a la lista enlazada

    return lineas_ensamblaje

def mostrar_listado_consola(lineas_ensamblaje):
    indice_maquina = 0
    maquina = lineas_ensamblaje.obtener(indice_maquina)
    while maquina:
        print('------------------------------------------------------')
        print(f'Número de Máquina(s):' + str(indice_maquina + 1))
        print(f"Nombre de maquina: {maquina.nombre_maquina}")
        print(f"Cantidad de lineas: {maquina.cantidad_lineas}")
        print(f"Cantidad de Componentes: {maquina.cantidad_componentes}")
        print(f"Tiempo ensamblaje: {maquina.tiempo_ensamblaje}")
        print("Productos:")
        for producto in maquina.obtener_productos():
            print(f"    Nombre: {producto.nombre_producto}")
            print( "    Elaboración:")
            for paso, conjunto in producto.obtener_pasos():
                print(f"      Paso: {paso}, Conjunto: {conjunto}")
        print()
        print()
        indice_maquina += 1
        maquina = lineas_ensamblaje.obtener(indice_maquina)

def mostrar_brazos_roboticos(lineas_ensamblaje):
    actual_brazo = lineas_ensamblaje.cabeza
    while actual_brazo:
        print(f"Nombre de maquina: {actual_brazo.nombre_maquina}")
        print(f"Cantidad de lineas: {actual_brazo.cantidad_lineas}")
        print(f"Cantidad de Componentes: {actual_brazo.cantidad_componentes}")
        print(f"Tiempo ensamblaje: {actual_brazo.tiempo_ensamblaje}")
        actual_brazo = actual_brazo.siguiente
        if not actual_brazo:
            break

def mostrar_productos(lineas_ensamblaje):
    actual_brazo = lineas_ensamblaje.cabeza
    while actual_brazo:
        print(f"Productos de la maquina: {actual_brazo.nombre_maquina}")
        actual_producto = actual_brazo.cabeza
        while actual_producto:
            print(f"    Nombre: {actual_producto.nombre_producto}")
            actual_producto = actual_producto.siguiente
            if not actual_producto:
                break
        actual_brazo = actual_brazo.siguiente
        if not actual_brazo:
            break

def mostrar_pasos(lineas_ensamblaje):
    actual_brazo = lineas_ensamblaje.cabeza
    while actual_brazo:
        print(f"Pasos de los productos de la maquina: {actual_brazo.nombre_maquina}")
        actual_producto = actual_brazo.cabeza
        while actual_producto:
            print(f"    Nombre: {actual_producto.nombre_producto}")
            print("    Elaboración:")
            actual_paso = actual_producto.cabeza_pasos
            while actual_paso:
                print(f"      Paso: {actual_paso.paso}, Conjunto: {actual_paso.conjunto}")
                actual_paso = actual_paso.siguiente
                if not actual_paso:
                    break
            actual_producto = actual_producto.siguiente
            if not actual_producto:
                break
        actual_brazo = actual_brazo.siguiente
        if not actual_brazo:
            break
               
def mostrar_cantidad_datos(lineas_ensamblaje):
    # Contar brazos robóticos
    cantidad_brazos = 0
    actual_brazo = lineas_ensamblaje.cabeza
    while actual_brazo:
        cantidad_brazos += 1
        actual_brazo = actual_brazo.siguiente

    # Contar productos
    cantidad_productos = 0
    actual_brazo = lineas_ensamblaje.cabeza
    while actual_brazo:
        actual_producto = actual_brazo.cabeza
        while actual_producto:
            cantidad_productos += 1
            actual_producto = actual_producto.siguiente

        actual_brazo = actual_brazo.siguiente

    # Contar pasos
    cantidad_pasos = 0
    actual_brazo = lineas_ensamblaje.cabeza
    while actual_brazo:
        actual_producto = actual_brazo.cabeza
        while actual_producto:
            actual_paso = actual_producto.cabeza_pasos
            while actual_paso:
                cantidad_pasos += 1
                actual_paso = actual_paso.siguiente

            actual_producto = actual_producto.siguiente

        actual_brazo = actual_brazo.siguiente

    print(f"Cantidad de brazos robóticos: {cantidad_brazos}")
    print(f"Cantidad de productos: {cantidad_productos}")
    print(f"Cantidad de pasos: {cantidad_pasos}")
   
def simular_ensamblaje(maquina, producto):
    tiempo = 0
    cabeza_movimientos = None
    posiciones = [0] * maquina.cantidad_lineas

    for linea, componente in producto.obtener_pasos():
        linea -= 1
        componente -= 1

        while posiciones[linea] < componente:
            tiempo += 1
            posiciones[linea] += 1
            nuevo_movimiento = Movimiento(tiempo, linea + 1, posiciones[linea] + 1, "Mover brazo")
            if not cabeza_movimientos:
                cabeza_movimientos = nuevo_movimiento
            else:
                actual = cabeza_movimientos
                while actual.siguiente:
                    actual = actual.siguiente
                actual.siguiente = nuevo_movimiento

        tiempo += 1
        nuevo_movimiento = Movimiento(tiempo, linea + 1, posiciones[linea] + 1, "Ensamblar componente")
        if not cabeza_movimientos:
            cabeza_movimientos = nuevo_movimiento
        else:
            actual = cabeza_movimientos
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_movimiento

    return cabeza_movimientos, tiempo 

def generar_reporte_html(maquina, producto, cabeza_movimientos, tiempo_total):
    html = f"""
    <html>
    <head>
        <title>Reporte de Simulación para {producto.nombre_producto}</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <h1>Reporte de Simulación para {producto.nombre_producto}</h1>
        <h2>Máquina: {maquina.nombre_maquina}</h2>
        <p>Cantidad de líneas: {maquina.cantidad_lineas}</p>
        <p>Cantidad de componentes: {maquina.cantidad_componentes}</p>
        <p>Tiempo de ensamblaje: {maquina.tiempo_ensamblaje}</p>
        <h3>Pasos de Elaboración:</h3>
        <table>
            <thead>
                <tr>
                    <th>Tiempo</th>
                    <th>Línea de Ensamblaje</th>
                    <th>Componente</th>
                    <th>Acción</th>
                </tr>
            </thead>
            <tbody>
    """
    actual = cabeza_movimientos
    while actual:
        html += f"""
        <tr>
            <td>{actual.tiempo}</td>
            <td>Línea: {actual.linea}</td>
            <td>Componente: {actual.componente}</td>
            <td>{actual.accion}</td>
        </tr>
        """
        actual = actual.siguiente
    html += f"""
            </tbody>
        </table>
        <h3>Tiempo Total de Ensamblaje: {tiempo_total} segundos</h3>
    </body>
    </html>
    """
    return html
   
#---------------- FUNCIONES FLASK ------------------
@app.route('/')
def mostrar_listado():
    filepath = 'C:/Users/Usuario/Desktop/Python/IPC2_Proyecto2_202200389/prueba1.xml'
    lineas_ensamblaje = leerArchivoET(filepath)
    mostrar_listado_consola(lineas_ensamblaje)

    # Obtener todos los elementos
    items = ListaItems()
    for i in range(lineas_ensamblaje.contar()):
        item = lineas_ensamblaje.obtener(i)
        if item is not None:
            items.agregar(item)
        else:
            break

    return render_template('listado.html', items=items.obtener_todos())

@app.route('/reporte/<nombre_producto>')
def generar_reporte(nombre_producto):
    filepath =  'C:/Users/Usuario/Desktop/Python/IPC2_Proyecto2_202200389/prueba1.xml' # Ajusta la ruta al archivo XML
    lineas_ensamblaje = leerArchivoET(filepath)

    # Buscar el producto en las líneas de ensamblaje
    for i in range(lineas_ensamblaje.contar()):
        maquina = lineas_ensamblaje.obtener(i)
        for producto in maquina.obtener_productos():
            if producto.nombre_producto == nombre_producto:
                # Simular el ensamblaje
                cabeza_movimientos, tiempo_total = simular_ensamblaje(maquina, producto)

                # Generar el reporte HTML
                reporte_html = generar_reporte_html(maquina, producto, cabeza_movimientos, tiempo_total)

                return render_template_string(reporte_html)

    return "Producto no encontrado", 404

'''filepath = abrir_archivo()
lineas_ensamblaje = leerArchivoET(filepath)
mostrar_listado(lineas_ensamblaje)

# Mostrar listado general
mostrar_listado(lineas_ensamblaje)

# Mostrar los brazos robóticos
mostrar_brazos_roboticos(lineas_ensamblaje)

# Mostrar los productos
mostrar_productos(lineas_ensamblaje)

# Mostrar los pasos
mostrar_pasos(lineas_ensamblaje)

# Mostrar la cantidad de datos
mostrar_cantidad_datos(lineas_ensamblaje)'''

ruta = abrir_archivo()
print(ruta)

if __name__ == '__main__':
    app.run(debug=True)
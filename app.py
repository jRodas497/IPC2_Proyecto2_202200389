from tkinter import filedialog
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import xml.etree.ElementTree as ET
from Listas.ListaEnlazada import ListaEnlazada
from Listas.NodoProducto import NodoProducto
from Clases.BrazoRobotico import BrazoRobotico

app = Flask(__name__)
ITEMS_PER_PAGE = 10

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
            for paso, instruccion in enumerate(instrucciones, start=1):
                nodo_producto.agregar_paso(paso, instruccion)  # Pasar el conjunto directamente
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
   
#---------------- FUNCIONES FLASK ------------------
@app.route('/')
def mostrar_listado():
    filepath = 'C:/Users/Usuario/Desktop/Python/IPC2_Proyecto2_202200389/prueba1.xml'
    lineas_ensamblaje = leerArchivoET(filepath)
    mostrar_listado_consola(lineas_ensamblaje)

    # Get the current page from the query parameters
    page = request.args.get('page', 1, type=int)
    total_items = lineas_ensamblaje.contar()
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE

    # Get the items for the current page
    items = []
    for i in range(start_index, end_index):
        item = lineas_ensamblaje.obtener(i)
        if item is not None:
            items.append(item)
        else:
            break

    return render_template('listado.html', items=items, page=page, total_pages=total_pages)

@app.route('/reporte/<nombre_producto>')
def generar_reporte(nombre_producto):
    filepath = 'C:/Users/Usuario/Desktop/Python/IPC2_Proyecto2_202200389/prueba1.xml'
    lineas_ensamblaje = leerArchivoET(filepath)

    # Buscar el producto en las líneas de ensamblaje
    for i in range(lineas_ensamblaje.contar()):
        maquina = lineas_ensamblaje.obtener(i)
        for producto in maquina.obtener_productos():
            if producto.nombre_producto == nombre_producto:
                return render_template('reporte.html', producto=producto, maquina=maquina)

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

if __name__ == '__main__':
    app.run(debug=True)
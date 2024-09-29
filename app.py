from tkinter import filedialog
from flask import Flask, render_template, request, redirect, url_for, Blueprint
import xml.etree.ElementTree as ET
from Listas.ListaEnlazada import ListaEnlazada
from Clases.BrazoRobotico import BrazoRobotico
from Clases.Productos import Productos

app = Flask(__name__)
blueprints = Blueprint("app", __name__, template_folder="templates")
#---------------------- RUTAS ----------------------
@blueprints.route('/')
def listado():
    return render_template('listado.html')

@app.route('/listado')
def listado():
    return render_template('listado.html')

app.register_blueprint(blueprints)
if __name__ == "__main__":
    app.run(debug=True)


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

def leerArchivoET():
    rutaArchivo = abrir_archivo()
    tree = ET.parse(rutaArchivo)
    root = tree.getroot()
    
    lineas_ensamblaje = ListaEnlazada()

    for maquina in root.findall('Maquina'):
        nombre_maquina = maquina.find('NombreMaquina').text.strip()
        cantidad_lineas = int(maquina.find('CantidadLineasProduccion').text.strip())
        cantidad_componentes = int(maquina.find('CantidadComponentes').text.strip())
        tiempo_ensamblaje = int(maquina.find('TiempoEnsamblaje').text.strip())

        brazo_robotico = BrazoRobotico(nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje)
        lista_productos = ListaEnlazada()
        for producto in maquina.find('ListadoProductos').findall('Producto'):
            nombre_producto = producto.find('nombre').text.strip()
            nuevo_producto = Productos(nombre_producto)
            instrucciones = producto.find('elaboracion').text.strip().split()
            for paso, instruccion in enumerate(instrucciones, start=1):
                nuevo_producto.agregar_paso(paso, instruccion)  # Pasar el conjunto directamente
            brazo_robotico.agregar_producto(nuevo_producto)

        lineas_ensamblaje.agregar(brazo_robotico)  # Agregar la máquina a la lista enlazada

    return lineas_ensamblaje

def mostrar_listado(lineas_ensamblaje):
    indice_maquina = 0
    maquina = lineas_ensamblaje.obtener(indice_maquina)
    primera_maquina = maquina  # Guardar la referencia a la primera máquina para detectar el ciclo
    while maquina:
        print(f"Nombre de maquina: {maquina.nombre_maquina}")
        print(f"Cantidad de lineas: {maquina.cantidad_lineas}")
        print(f"Cantidad de Componentes: {maquina.cantidad_componentes}")
        print(f"Tiempo ensamblaje: {maquina.tiempo_ensamblaje}")
        print("  Productos:")
        '''for producto in maquina.productos:
            print(f"    Nombre: {producto.nombre_producto}")
            print("    Elaboración:")
            pasos = " | ".join([f"L{paso.linea}C{paso.componente}" for paso in producto.elaboracion])
            print(f"      Pasos: {pasos}")'''
        indice_maquina += 1
        maquina = lineas_ensamblaje.obtener(indice_maquina)
        if maquina == primera_maquina:
            break  # Salir del bucle si hemos vuelto al inicio

if __name__ == "__main__":
    app.run(debug=True)

lineas_ensamblaje = leerArchivoET()
mostrar_listado(lineas_ensamblaje)
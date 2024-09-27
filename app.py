from tkinter import filedialog
import xml.etree.ElementTree as ET
import threading
from Listas.ListaEnlazada import ListaEnlazada
from Clases.BrazoRobotico import BrazoRobotico
from Listas.Nodo import Nodo

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

        for producto in maquina.find('ListadoProductos').findall('Producto'):
            nombre_producto = producto.find('nombre').text.strip()
            nuevo_producto = Nodo(nombre_producto)
            instrucciones = producto.find('elaboracion').text.strip().split()
            for instruccion in instrucciones:
                nuevo_producto.agregar_paso(instruccion)
            brazo_robotico.agregar_producto(nuevo_producto)

        lineas_ensamblaje.agregar(brazo_robotico)

    return lineas_ensamblaje

lineas_ensamblaje = leerArchivoET()

lock = threading.Lock()

indice_maquina = 0
maquina = lineas_ensamblaje.obtener(indice_maquina)
while maquina:
    # Aquí puedes realizar operaciones con cada máquina
    print(f"Procesando máquina: {maquina.nombre_maquina}")
    maquina.ensamblar_productos()
    indice_maquina += 1
    maquina = lineas_ensamblaje.obtener(indice_maquina)
    
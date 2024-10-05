from tkinter import filedialog
import os, re
from xml.dom import minidom
from graphviz import Digraph
import xml.etree.ElementTree as ET
from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from Listas.ListaEnlazada import ListaEnlazada
from Listas.NodoProducto import NodoProducto
from Listas.ListaItems import ListaItems
from Clases.BrazoRobotico import BrazoRobotico
from Clases.Movimiento import Movimiento
from Clases.Posicion import Posicion

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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

def abrir_archivo_2():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.xml'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        session['filepath'] = filepath
        return filepath
    return None
    
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
            instrucciones = producto.find('elaboracion').text.strip()
            
            matches = re.findall(r'L(\d+)C(\d+)', instrucciones)
            for match in matches:
                linea = int(match[0])
                componente = int(match[1])
                nodo_producto.agregar_paso(linea, componente)
            
            brazo_robotico.agregar_producto(nodo_producto)

        lineas_ensamblaje.agregar(brazo_robotico)

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
    cantidad_brazos = 0
    actual_brazo = lineas_ensamblaje.cabeza
    while actual_brazo:
        cantidad_brazos += 1
        actual_brazo = actual_brazo.siguiente

    cantidad_productos = 0
    actual_brazo = lineas_ensamblaje.cabeza
    while actual_brazo:
        actual_producto = actual_brazo.cabeza
        while actual_producto:
            cantidad_productos += 1
            actual_producto = actual_producto.siguiente

        actual_brazo = actual_brazo.siguiente

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
    cabeza_posiciones = None

    for i in range(maquina.cantidad_lineas):
        nueva_posicion = Posicion(i + 1, 0)
        if not cabeza_posiciones:
            cabeza_posiciones = nueva_posicion
        else:
            actual = cabeza_posiciones
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nueva_posicion

    for linea, componente in producto.obtener_pasos():
        linea = int(linea)
        componente = int(componente)

        actual_posicion = cabeza_posiciones
        while actual_posicion and actual_posicion.linea != linea:
            actual_posicion = actual_posicion.siguiente

        while actual_posicion.componente < componente:
            tiempo += 1
            actual_posicion.componente += 1
            nuevo_movimiento = Movimiento(tiempo, linea, actual_posicion.componente, "Mover brazo")
            if not cabeza_movimientos:
                cabeza_movimientos = nuevo_movimiento
            else:
                actual = cabeza_movimientos
                while actual.siguiente:
                    actual = actual.siguiente
                actual.siguiente = nuevo_movimiento

        for _ in range(maquina.tiempo_ensamblaje):
            tiempo += 1
            nuevo_movimiento = Movimiento(tiempo, linea, actual_posicion.componente, "Ensamblar componente")
            if not cabeza_movimientos:
                cabeza_movimientos = nuevo_movimiento
            else:
                actual = cabeza_movimientos
                while actual.siguiente:
                    actual = actual.siguiente
                actual.siguiente = nuevo_movimiento

    return cabeza_movimientos, tiempo
    
def generar_reporte_html(maquina, producto, cabeza_movimientos, tiempo_total):
    '''
    
    print("PATH:", os.environ['PATH'])

    # Crear el gráfico de Graphviz
    dot = Digraph(comment='Movimientos de Ensamblaje')
    actual = cabeza_movimientos
    while actual and actual.siguiente:
        dot.node(f"L{actual.linea}C{actual.componente}", f"L{actual.linea}C{actual.componente}")
        dot.edge(f"L{actual.linea}C{actual.componente}", f"L{actual.siguiente.linea}C{actual.siguiente.componente}")
        actual = actual.siguiente

    # Renderizar el gráfico a una imagen
    try:
        dot.format = 'png'
        dot.render('movimientos', view=False)
    except Exception as e:
        return f"Error al renderizar el gráfico: {e}"
        
    '''
    
    html = f"""
    <html>
    <head>
        <title>Reporte de Simulación para {producto.nombre_producto}</title>
        <style>
        h1, h2, h3 {{ font-weight: 300; 
            margin-top: 25px;
            margin-left: 25px;
        }}
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
        p {{
            font-size: 1.2rem;
            text-align: left;
            margin-left: 45px;
          }}
        .top-right {{
            position: absolute;
            top: 10px;
            right: 10px;
        }}
        </style>
    </head>
    <body>
        <div class="top-right">
        <p><a href="https://github.com/jRodas497">Github del Estudiante</a></p>
        </div>
        <h1>Reporte de Simulación para {producto.nombre_producto}</h1>
        <h2><strong>Máquina: {maquina.nombre_maquina}</strong></h2>
        <p>Cantidad de líneas: {maquina.cantidad_lineas}</p>
        <p>Cantidad de componentes: {maquina.cantidad_componentes}</p>
        <p>Tiempo de ensamblaje: {maquina.tiempo_ensamblaje}</p>
        <h3><strong>Movimientos de Ensamblaje:</strong></h3>
        
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
        <h3><strong>Tiempo Total de Ensamblaje: {tiempo_total} segundos</strong></h3>
    </body>
    </html>
    """
    return html

def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generar_xml(maquina, producto, cabeza_movimientos, tiempo_total):
    root = ET.Element("SalidaSimulacion")
    
    maquina_elem = ET.SubElement(root, "Maquina")
    
    nombre_maquina_elem = ET.SubElement(maquina_elem, "Nombre")
    nombre_maquina_elem.text = maquina.nombre_maquina
    
    listado_productos_elem = ET.SubElement(maquina_elem, "ListadoProductos")
    
    producto_elem = ET.SubElement(listado_productos_elem, "Producto")
    
    nombre_producto_elem = ET.SubElement(producto_elem, "Nombre")
    nombre_producto_elem.text = producto.nombre_producto
    
    tiempo_total_elem = ET.SubElement(producto_elem, "TiempoTotal")
    tiempo_total_elem.text = str(tiempo_total)
    
    elaboracion_optima_elem = ET.SubElement(producto_elem, "ElaboracionOptima")
    
    movimiento_actual = cabeza_movimientos
    idx = 1
    while movimiento_actual is not None:
        tiempo_elem = ET.SubElement(elaboracion_optima_elem, "Tiempo", NoSegundo=str(idx))
        linea_ensamblaje_elem = ET.SubElement(tiempo_elem, "LineaEnsamblaje", NoLinea=str(movimiento_actual.linea), NoComponente=str(movimiento_actual.componente))
        linea_ensamblaje_elem.text = f"L{movimiento_actual.linea}C{movimiento_actual.componente}"
        movimiento_actual = movimiento_actual.siguiente
        idx += 1

    pretty_xml_as_string = prettify(root)
    
    return pretty_xml_as_string

#---------------- FUNCIONES FLASK ------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filepath = abrir_archivo_2()
        if filepath:
            return redirect(url_for('mostrar_listado', filepath=filepath))
    return render_template('index.html')

@app.route('/listado')
def mostrar_listado():
    filepath = request.args.get('filepath')
    if not filepath:
        return redirect(url_for('index'))
    
    lineas_ensamblaje = leerArchivoET(filepath)
    mostrar_listado_consola(lineas_ensamblaje)

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
    filepath = session.get('filepath')
    if not filepath:
        return redirect(url_for('index'))
    
    lineas_ensamblaje = leerArchivoET(filepath)

    for i in range(lineas_ensamblaje.contar()):
        maquina = lineas_ensamblaje.obtener(i)
        for producto in maquina.obtener_productos():
            if producto.nombre_producto == nombre_producto:
                cabeza_movimientos, tiempo_total = simular_ensamblaje(maquina, producto)
                
                pasos = ""
                movimiento_actual = cabeza_movimientos
                while movimiento_actual is not None:
                    pasos += f"L{movimiento_actual.linea}C{movimiento_actual.componente} "
                    movimiento_actual = movimiento_actual.siguiente
                
                pasos = pasos.strip()
                
                xml_content = generar_xml(maquina, producto, cabeza_movimientos, tiempo_total)
                
                # Ensure the uploads directory exists
                uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
                os.makedirs(uploads_dir, exist_ok=True)
                
                # Write the XML content to a file in the uploads directory
                file_path = os.path.join(uploads_dir, f"salida_{producto.nombre_producto}.xml")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(xml_content)
                
                html = generar_reporte_html(maquina, producto, cabeza_movimientos, tiempo_total)
                return html

    return redirect(url_for('index'))

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
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import sys
import os

# Agregar el directorio modules al path para importar modcatal
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from modules.modcatal import CatalogosManager
from modules.modboldis import DisenoModelosManager

app = Flask(__name__)

# Configuración de la base de datos
DB_PATH = "database/ChromaBags.db"
diseno_manager = DisenoModelosManager(DB_PATH)

def get_connection():
    """Obtiene una conexión a la base de datos SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Instancia global del gestor de catálogos
catalogos = CatalogosManager(DB_PATH)

# Página principal
@app.route('/')
def index():
    return redirect(url_for('clientes'))

# ============ CLIENTES ============

@app.route('/clientes')
def clientes():
    conn = get_connection()
    clientes_data = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre_cliente, telefono, correo, tipo_cliente, direccion, id_cliente 
            FROM clientes 
            ORDER BY id_cliente;
        """)
        clientes_data = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('clientes.html', clientes=clientes_data)

@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    correo = request.form['correo']
    tipo = request.form['tipo']
    direccion = request.form['direccion']

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre_cliente, telefono, correo, tipo_cliente, direccion)
            VALUES (?, ?, ?, ?, ?);
        """, (nombre, telefono, correo, tipo, direccion))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('clientes'))

@app.route('/eliminar_cliente/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id_cliente = ?;", (id,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('clientes'))

@app.route('/modificar_cliente/<int:id>', methods=['POST'])
def modificar_cliente(id):
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    correo = request.form['correo']
    tipo = request.form['tipo']
    direccion = request.form['direccion']

    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE clientes 
            SET nombre_cliente=?, telefono=?, correo=?, tipo_cliente=?, direccion=?
            WHERE id_cliente=?;
        """, (nombre, telefono, correo, tipo, direccion, id))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('clientes'))

# ============ CATÁLOGO - USANDO MODCATAL ============

@app.route('/catalogo')
def catalogo():
    """Muestra el catálogo de productos usando el módulo modcatal"""
    # Obtener parámetros de filtrado opcionales
    filtro_tipo = request.args.get('tipo', None)
    filtro_modelo = request.args.get('modelo', None)
    
    # Convertir filtro_modelo a int si existe
    if filtro_modelo:
        try:
            filtro_modelo = int(filtro_modelo)
        except ValueError:
            filtro_modelo = None
    
    # Usar el gestor de catálogos para obtener los productos
    productos = catalogos.listar_productos_catalogo(
        filtro_tipo=filtro_tipo,
        filtro_modelo=filtro_modelo
    )
    
    # Convertir los objetos ProductoTerminado a tuplas para compatibilidad con el template
    productos_tuplas = []
    for p in productos:
        productos_tuplas.append((
            p.nombre,           # p[0]
            p.modelo,           # p[1]
            p.tipo_modelo,      # p[2]
            p.color_principal,  # p[3]
            p.precio,           # p[4]
            p.stock             # p[5]
        ))
    
    # Obtener lista de modelos para filtros
    modelos = catalogos.listar_disenos()
    
    return render_template('catalogo.html', 
                         productos=productos_tuplas,
                         modelos=modelos,
                         filtro_actual=filtro_tipo)

@app.route('/catalogo/producto/<int:id>')
def detalle_producto(id):
    """Muestra los detalles de un producto específico"""
    producto = catalogos.obtener_producto(id)
    if not producto:
        return "Producto no encontrado", 404
    
    return render_template('detalle_producto.html', producto=producto.to_dict())

# ============ GESTIÓN DE COLORES ============

@app.route('/colores')
def listar_colores():
    """Lista todos los colores del catálogo"""
    colores = catalogos.listar_colores()
    return render_template('colores.html', colores=[c.to_dict() for c in colores])

@app.route('/colores/agregar', methods=['POST'])
def agregar_color():
    """Agrega un nuevo color"""
    nombre = request.form.get('nombre')
    codigo_hex = request.form.get('codigo_hex')
    id_paleta = request.form.get('id_paleta')
    
    if id_paleta:
        id_paleta = int(id_paleta)
    else:
        id_paleta = None
    
    color = catalogos.agregar_color(nombre, codigo_hex, id_paleta)
    
    if request.headers.get('Accept') == 'application/json':
        if color:
            return jsonify({'success': True, 'color': color.to_dict()})
        return jsonify({'success': False, 'error': 'No se pudo agregar el color'}), 400
    
    return redirect(url_for('listar_colores'))

@app.route('/colores/actualizar/<int:id>', methods=['POST'])
def actualizar_color(id):
    """Actualiza un color existente"""
    datos = {}
    
    if 'nombre' in request.form:
        datos['nombre'] = request.form['nombre']
    if 'codigo_hex' in request.form:
        datos['codigo_hex'] = request.form['codigo_hex']
    if 'id_paleta' in request.form:
        datos['id_paleta'] = int(request.form['id_paleta']) if request.form['id_paleta'] else None
    
    success = catalogos.actualizar_color(id, **datos)
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'success': success})
    
    return redirect(url_for('listar_colores'))

@app.route('/colores/eliminar/<int:id>', methods=['POST'])
def eliminar_color(id):
    """Elimina un color"""
    success = catalogos.eliminar_color(id)
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'success': success})
    
    return redirect(url_for('listar_colores'))

# ============ GESTIÓN DE DISEÑOS/MODELOS ============

@app.route('/disenos')
def listar_disenos():
    """Lista todos los diseños"""
    disenos = catalogos.listar_disenos()
    return render_template('disenos.html', disenos=[d.to_dict() for d in disenos])

@app.route('/disenos/agregar', methods=['POST'])
def agregar_diseno():
    """Agrega un nuevo diseño"""
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    descripcion = request.form.get('descripcion', '')
    ancho = float(request.form.get('ancho', 30.0))
    alto = float(request.form.get('alto', 40.0))
    
    diseno = catalogos.agregar_diseno(nombre, tipo, descripcion, ancho, alto)
    
    if request.headers.get('Accept') == 'application/json':
        if diseno:
            return jsonify({'success': True, 'diseno': diseno.to_dict()})
        return jsonify({'success': False, 'error': 'No se pudo agregar el diseño'}), 400
    
    return redirect(url_for('listar_disenos'))
@app.route('/diseno_color', methods=['GET', 'POST'])
def diseno_color():
    """Ruta para diseño y combinaciones de colores"""
    
    if request.method == 'POST':
        # Obtener datos del formulario
        esquema = request.form.get('esquema_color')
        id_modelo = int(request.form.get('modelo_bolsa'))
        nombre = request.form.get('nombre_combinacion')
        id_paleta = int(request.form.get('id_paleta'))
        
        # Obtener el primer color de la paleta como color principal
        colores_paleta = diseno_manager.obtener_colores_por_paleta(id_paleta)
        
        id_color_principal = colores_paleta[0]['id_color'] if colores_paleta else None
        id_color_secundario = colores_paleta[1]['id_color'] if len(colores_paleta) > 1 else None
        id_color_hilo = colores_paleta[2]['id_color'] if len(colores_paleta) > 2 else id_color_principal
        id_color_asa = colores_paleta[3]['id_color'] if len(colores_paleta) > 3 else id_color_principal
        
        # Crear la combinación
        combinacion = diseno_manager.crear_combinacion(
            id_modelo=id_modelo,
            nombre=nombre,
            esquema=esquema,
            id_color_principal=id_color_principal,
            id_color_secundario=id_color_secundario,
            id_color_hilo=id_color_hilo,
            id_color_asa=id_color_asa
        )
        
        if combinacion:
            return redirect(url_for('diseno_color'))
    
    # GET: Mostrar el formulario
    modelos = diseno_manager.listar_modelos()
    paletas = diseno_manager.obtener_paletas_disponibles()
    combinaciones = diseno_manager.listar_combinaciones()
    
    # Convertir a formato compatible con el template
    modelos_tuplas = [(m.id_modelo, m.nombre, m.tipo) for m in modelos]
    paletas_tuplas = [(p['id_paleta'], p['nombre'], p['esquema']) for p in paletas]
    
    # Convertir combinaciones a tuplas
    combinaciones_tuplas = []
    for comb_det in combinaciones:
        combinaciones_tuplas.append((
            comb_det.combinacion.id_combinacion,
            comb_det.combinacion.nombre,
            comb_det.combinacion.esquema,
            comb_det.combinacion.fecha_creacion
        ))
    
    return render_template('diseno_color.html',
                         modelos=modelos_tuplas,
                         paletas=paletas_tuplas,
                         combinaciones=combinaciones_tuplas)


@app.route('/disenos/eliminar/<int:id>', methods=['POST'])
def eliminar_diseno(id):
    """Elimina un diseño"""
    success = catalogos.eliminar_diseno(id)
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'success': success})
    
    return redirect(url_for('listar_disenos'))

# ============ GESTIÓN DE MATERIALES ============

@app.route('/materiales')
def listar_materiales():
    """Lista todos los materiales"""
    tipo_filtro = request.args.get('tipo')
    materiales = catalogos.listar_materiales(tipo=tipo_filtro)
    
    # Enriquecer con información de stock
    materiales_con_stock = []
    for m in materiales:
        mat_dict = m.to_dict()
        mat_dict['stock_actual'] = catalogos.obtener_stock_material(m.id_material)
        materiales_con_stock.append(mat_dict)
    
    return render_template('materiales.html', materiales=materiales_con_stock)

@app.route('/materiales/agregar', methods=['POST'])
def agregar_material():
    """Agrega un nuevo material"""
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    unidad_medida = request.form.get('unidad_medida', 'm')
    costo_unitario = float(request.form.get('costo_unitario', 0))
    descripcion = request.form.get('descripcion', '')
    stock_inicial = float(request.form.get('stock_inicial', 0))
    
    material = catalogos.agregar_material(nombre, tipo, unidad_medida, 
                                         costo_unitario, descripcion)
    
    # Si se especificó stock inicial, agregarlo al inventario
    if material and stock_inicial > 0:
        catalogos.ajustar_stock_material(material.id_material, stock_inicial)
    
    if request.headers.get('Accept') == 'application/json':
        if material:
            return jsonify({'success': True, 'material': material.to_dict()})
        return jsonify({'success': False, 'error': 'No se pudo agregar el material'}), 400
    
    return redirect(url_for('listar_materiales'))

@app.route('/materiales/actualizar/<int:id>', methods=['POST'])
def actualizar_material(id):
    """Actualiza un material existente"""
    datos = {}
    
    if 'nombre' in request.form:
        datos['nombre'] = request.form['nombre']
    if 'tipo' in request.form:
        datos['tipo'] = request.form['tipo']
    if 'unidad_medida' in request.form:
        datos['unidad_medida'] = request.form['unidad_medida']
    if 'costo_unitario' in request.form:
        datos['costo_unitario'] = float(request.form['costo_unitario'])
    if 'descripcion' in request.form:
        datos['descripcion'] = request.form['descripcion']
    
    success = catalogos.actualizar_material(id, **datos)
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'success': success})
    
    return redirect(url_for('listar_materiales'))

@app.route('/materiales/ajustar_stock/<int:id>', methods=['POST'])
def ajustar_stock(id):
    """Ajusta el stock de un material"""
    cantidad = float(request.form.get('cantidad', 0))
    success = catalogos.ajustar_stock_material(id, cantidad)
    
    if request.headers.get('Accept') == 'application/json':
        stock_actual = catalogos.obtener_stock_material(id)
        return jsonify({'success': success, 'stock_actual': stock_actual})
    
    return redirect(url_for('listar_materiales'))

@app.route('/materiales/eliminar/<int:id>', methods=['POST'])
def eliminar_material(id):
    """Elimina un material"""
    success = catalogos.eliminar_material(id)
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'success': success})
    
    return redirect(url_for('listar_materiales'))

# ============ DISEÑO Y COLOR (Funcionalidad existente) ============

# Cargar colores según paleta (Ajax)
@app.route('/ver_colores/<int:id_paleta>')
def ver_colores(id_paleta):
    """Obtiene los colores de una paleta específica"""
    colores = diseno_manager.obtener_colores_por_paleta(id_paleta)
    # Formato: [(nombre, hex), ...]
    colores_lista = [(c['nombre'], c['codigo_hex']) for c in colores]
    return jsonify(colores_lista)


@app.route('/modelos')
def listar_modelos_view():
    """Lista todos los modelos de bolsas"""
    tipo_filtro = request.args.get('tipo')
    modelos = diseno_manager.listar_modelos(tipo=tipo_filtro)
    
    # Obtener estadísticas para cada modelo
    modelos_con_stats = []
    for m in modelos:
        stats = diseno_manager.obtener_estadisticas_modelo(m.id_modelo)
        modelo_dict = m.to_dict()
        modelo_dict['estadisticas'] = stats
        modelos_con_stats.append(modelo_dict)
    
    return render_template('modelos.html', modelos=modelos_con_stats)


@app.route('/modelos/agregar', methods=['POST'])
def agregar_modelo_view():
    """Agrega un nuevo modelo"""
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo', 'estandar')
    descripcion = request.form.get('descripcion', '')
    ancho = float(request.form.get('ancho', 30.0))
    alto = float(request.form.get('alto', 35.0))
    
    modelo = diseno_manager.agregar_modelo(nombre, tipo, descripcion, ancho, alto)
    
    if request.headers.get('Accept') == 'application/json':
        if modelo:
            return jsonify({'success': True, 'modelo': modelo.to_dict()})
        return jsonify({'success': False, 'error': 'No se pudo agregar el modelo'}), 400
    
    return redirect(url_for('listar_modelos_view'))


@app.route('/modelos/actualizar/<int:id>', methods=['POST'])
def actualizar_modelo_view(id):
    """Actualiza un modelo existente"""
    datos = {}
    
    if 'nombre' in request.form:
        datos['nombre'] = request.form['nombre']
    if 'tipo' in request.form:
        datos['tipo'] = request.form['tipo']
    if 'descripcion' in request.form:
        datos['descripcion'] = request.form['descripcion']
    if 'ancho' in request.form:
        datos['ancho'] = float(request.form['ancho'])
    if 'alto' in request.form:
        datos['alto'] = float(request.form['alto'])
    
    success = diseno_manager.actualizar_modelo(id, **datos)
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'success': success})
    
    return redirect(url_for('listar_modelos_view'))


@app.route('/modelos/eliminar/<int:id>', methods=['POST'])
def eliminar_modelo_view(id):
    """Elimina un modelo"""
    success = diseno_manager.eliminar_modelo(id)
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'success': success})
    
    return redirect(url_for('listar_modelos_view'))


# ============================================================
# NUEVAS RUTAS PARA GESTIÓN DE COMBINACIONES
# ============================================================

@app.route('/combinaciones')
def listar_combinaciones_view():
    """Lista todas las combinaciones guardadas"""
    id_modelo = request.args.get('modelo', type=int)
    esquema = request.args.get('esquema')
    
    combinaciones = diseno_manager.listar_combinaciones(
        id_modelo=id_modelo,
        esquema=esquema
    )
    
    return render_template('combinaciones.html', 
                         combinaciones=[c.to_dict() for c in combinaciones])


@app.route('/combinaciones/<int:id>')
def detalle_combinacion(id):
    """Muestra los detalles de una combinación específica"""
    combinacion = diseno_manager.obtener_combinacion_detallada(id)
    
    if not combinacion:
        return "Combinación no encontrada", 404
    
    return render_template('detalle_combinacion.html', 
                         combinacion=combinacion.to_dict())


@app.route('/combinaciones/actualizar/<int:id>', methods=['POST'])
def actualizar_combinacion_view(id):
    """Actualiza una combinación existente"""
    datos = {}
    
    if 'nombre' in request.form:
        datos['nombre'] = request.form['nombre']
    if 'esquema' in request.form:
        datos['esquema'] = request.form['esquema']
    if 'id_color_principal' in request.form:
        datos['id_color_principal'] = int(request.form['id_color_principal'])
    if 'id_color_secundario' in request.form:
        datos['id_color_secundario'] = int(request.form['id_color_secundario'])
    if 'id_color_hilo' in request.form:
        datos['id_color_hilo'] = int(request.form['id_color_hilo'])
    if 'id_color_asa' in request.form:
        datos['id_color_asa'] = int(request.form['id_color_asa'])
    
    success = diseno_manager.actualizar_combinacion(id, **datos)
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'success': success})
    
    return redirect(url_for('listar_combinaciones_view'))


@app.route('/combinaciones/eliminar/<int:id>', methods=['POST'])
def eliminar_combinacion_view(id):
    """Elimina una combinación"""
    success = diseno_manager.eliminar_combinacion(id)
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'success': success})
    
    return redirect(url_for('diseno_color'))


# ============================================================
# RUTAS DE ESTADÍSTICAS Y REPORTES
# ============================================================

@app.route('/estadisticas/modelos')
def estadisticas_modelos():
    """Muestra estadísticas de todos los modelos"""
    modelos = diseno_manager.listar_modelos()
    estadisticas = []
    
    for modelo in modelos:
        stats = diseno_manager.obtener_estadisticas_modelo(modelo.id_modelo)
        if stats:
            estadisticas.append(stats)
    
    return render_template('estadisticas_modelos.html', estadisticas=estadisticas)


@app.route('/estadisticas/colores')
def estadisticas_colores():
    """Muestra los colores más usados"""
    colores_mas_usados = diseno_manager.obtener_colores_mas_usados(limite=10)
    
    return render_template('estadisticas_colores.html', 
                         colores=colores_mas_usados)


# ============ API JSON para integración con otros sistemas ============

@app.route('/api/catalogo')
def api_catalogo():
    """API JSON para obtener el catálogo completo"""
    productos = catalogos.listar_productos_catalogo()
    return jsonify([p.to_dict() for p in productos])

@app.route('/api/colores')
def api_colores():
    """API JSON para obtener todos los colores"""
    colores = catalogos.listar_colores()
    return jsonify([c.to_dict() for c in colores])


@app.route('/api/materiales')
def api_materiales():
    """API JSON para obtener todos los materiales con stock"""
    materiales = catalogos.listar_materiales()
    materiales_con_stock = []
    for m in materiales:
        mat_dict = m.to_dict()
        mat_dict['stock_actual'] = catalogos.obtener_stock_material(m.id_material)
        materiales_con_stock.append(mat_dict)
    return jsonify(materiales_con_stock)

@app.route('/api/modelos')
def api_modelos_diseno():
    """API JSON para obtener todos los modelos"""
    modelos = diseno_manager.listar_modelos()
    return jsonify([m.to_dict() for m in modelos])


@app.route('/api/combinaciones')
def api_combinaciones():
    """API JSON para obtener todas las combinaciones"""
    combinaciones = diseno_manager.listar_combinaciones()
    return jsonify([c.to_dict() for c in combinaciones])


@app.route('/api/paletas')
def api_paletas():
    """API JSON para obtener todas las paletas"""
    paletas = diseno_manager.obtener_paletas_disponibles()
    return jsonify(paletas)


@app.route('/api/paletas/<int:id_paleta>/colores')
def api_colores_paleta(id_paleta):
    """API JSON para obtener colores de una paleta"""
    colores = diseno_manager.obtener_colores_por_paleta(id_paleta)
    return jsonify(colores)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5050)
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# ==============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# ==============================================================================
DB_PATH = 'inventario.db'
SQL_SCRIPT_PATH = os.path.join('static', 'sql', 'SuperInventarioIT.sql')

def init_db():
    """Inicializa la base de datos si no existe, ejecutando el script SQL."""
    if not os.path.exists(DB_PATH):
        print(f"[BD LOG] Creando la base de datos a partir de {SQL_SCRIPT_PATH}...")
        with sqlite3.connect(DB_PATH) as conn:
            with open(SQL_SCRIPT_PATH, 'r') as f:
                conn.executescript(f.read())
        print("[BD LOG] Base de datos inicializada con éxito.")

def get_db_connection():
    """Crea una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    # Permite acceder a las columnas por su nombre como si fueran diccionarios
    conn.row_factory = sqlite3.Row 
    return conn

# ------------------------------------------------------------------------------
# RUTAS DE NAVEGACIÓN (Vistas HTML)
# ------------------------------------------------------------------------------


@app.route('/')
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    
    # 1. Total de equipos
    total_equipos = conn.execute('SELECT COUNT(*) FROM Stock').fetchone()[0]
    
    # 2. Total de usuarios
    total_usuarios = conn.execute('SELECT COUNT(*) FROM Usuario').fetchone()[0]
    
    # 3. Equipos SIN licencia (id_licencia es NULL)
    equipos_sin_licencia_count = conn.execute('SELECT COUNT(*) FROM Stock WHERE id_licencia IS NULL').fetchone()[0]
    
    # 4. Lista detallada de los equipos sin licencia
    equipos_sin_licencia_lista = conn.execute('''
        SELECT s.SN_equipo, s.marca_equipo, s.SO_equipo, u.nombre, u.departamento 
        FROM Stock s
        JOIN Usuario u ON s.id_usuario = u.id_usuario
        WHERE s.id_licencia IS NULL
    ''').fetchall()

    # 5. Conteo por marca
    equipos_por_marca = conn.execute('''
        SELECT marca_equipo, COUNT(*) as cantidad 
        FROM Stock 
        GROUP BY marca_equipo
        ORDER BY cantidad DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                           total_equipos=total_equipos,
                           total_usuarios=total_usuarios,
                           equipos_sin_licencia_count=equipos_sin_licencia_count,
                           equipos_sin_licencia_lista=equipos_sin_licencia_lista,
                           equipos_por_marca=equipos_por_marca,
                           active_page='dashboard')

from flask import redirect, url_for, request

@app.route('/alta-equipos')
def alta_equipos():
    """Ruta para el formulario de registro. Carga catálogos para los menús desplegables."""
    conn = get_db_connection()
    usuarios = conn.execute('SELECT id_usuario, nombre, apellido_paterno, departamento FROM Usuario').fetchall()
    licencias = conn.execute('SELECT id_licencia, tipo_licencia FROM Licencia').fetchall()
    conn.close()
    
    return render_template('alta_equipos.html', usuarios=usuarios, licencias=licencias, active_page='alta')

@app.route('/editar/<sn_equipo>')
def editar_equipo(sn_equipo):
    """Carga el formulario de alta pero pre-llenado con los datos del equipo."""
    conn = get_db_connection()
    # Obtenemos todos los datos del equipo específico
    equipo = conn.execute('SELECT * FROM Stock WHERE SN_equipo = ?', (sn_equipo,)).fetchone()
    usuarios = conn.execute('SELECT id_usuario, nombre, apellido_paterno, departamento FROM Usuario').fetchall()
    licencias = conn.execute('SELECT id_licencia, tipo_licencia FROM Licencia').fetchall()
    conn.close()
    
    # Renderizamos la misma plantilla, pero pasándole la variable 'equipo'
    return render_template('alta_equipos.html', equipo=equipo, usuarios=usuarios, licencias=licencias, active_page='inventario')

@app.route('/eliminar/<sn_equipo>', methods=['POST'])
def eliminar_equipo(sn_equipo):
    """Elimina un equipo de la base de datos."""
    conn = get_db_connection()
    conn.execute('DELETE FROM Stock WHERE SN_equipo = ?', (sn_equipo,))
    conn.commit()
    conn.close()
    
    # Te regresa a la página donde estabas (búsqueda o inventario)
    return redirect(request.referrer or url_for('inventario'))

@app.route('/api/equipo', methods=['POST'])
def guardar_equipo():
    """Guarda un equipo nuevo o actualiza uno existente."""
    sn_equipo = request.form.get('sn_equipo')
    marca_equipo = request.form.get('marca_equipo')
    id_usuario = request.form.get('id_usuario')
    id_usuario = request.form.get('id_usuario')
    if not id_usuario or id_usuario == '0':
        id_usuario = 0
    procesador = request.form.get('procesador')
    ram = request.form.get('ram')
    almacenamiento = request.form.get('almacenamiento')
    so_equipo = request.form.get('so_equipo')
    id_licencia = request.form.get('id_licencia')
    marca_monitor = request.form.get('marca_monitor')
    pulgadas_monitor = request.form.get('pulgadas_monitor')
    marca_teclado = request.form.get('marca_teclado')
    marca_mouse = request.form.get('marca_mouse')
    
    # Campo oculto que nos dice si estamos editando
    original_sn = request.form.get('original_sn')
    id_licencia = id_licencia if id_licencia else None

    conn = get_db_connection()
    
    if original_sn:
        # Si existe original_sn, es una EDICIÓN (UPDATE)
        conn.execute('''
            UPDATE Stock SET 
                SN_equipo=?, marca_equipo=?, ram_equipo=?, almacenamiento_equipo=?, 
                procesador_equipo=?, SO_equipo=?, id_usuario=?, id_licencia=?,
                marca_monitor=?, pulgadas_monitor=?, marca_teclado=?, marca_mouse=?
            WHERE SN_equipo=?
        ''', (sn_equipo, marca_equipo, ram, almacenamiento, procesador, so_equipo, 
              id_usuario, id_licencia, marca_monitor, pulgadas_monitor, marca_teclado, marca_mouse, original_sn))
    else:
        # Si NO existe, es un ALTA NUEVA (INSERT)
        conn.execute('''
            INSERT INTO Stock (
                SN_equipo, marca_equipo, ram_equipo, almacenamiento_equipo, 
                procesador_equipo, SO_equipo, id_usuario, id_licencia,
                marca_monitor, pulgadas_monitor, marca_teclado, marca_mouse
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sn_equipo, marca_equipo, ram, almacenamiento, procesador, so_equipo, 
              id_usuario, id_licencia, marca_monitor, pulgadas_monitor, marca_teclado, marca_mouse))
    
    conn.commit()
    conn.close()

    return redirect(url_for('inventario'))

@app.route('/busqueda')
def busqueda():
    """Módulo de búsqueda global en el inventario."""
    # Captura el término de búsqueda de la URL (ej. /busqueda?q=Dell)
    query = request.args.get('q', '')
    equipos = []

    if query:
        conn = get_db_connection()
        # Creamos el comodín para SQL (ej. %Dell%)
        search_term = f"%{query}%"
        
        # Buscamos coincidencias en múltiples columnas usando OR
        equipos = conn.execute('''
            SELECT 
                s.id_stock, s.SN_equipo, s.marca_equipo, s.procesador_equipo, 
                s.ram_equipo, s.almacenamiento_equipo, s.SO_equipo, 
                u.nombre, u.apellido_paterno, u.departamento,
                l.tipo_licencia
            FROM Stock s
            JOIN Usuario u ON s.id_usuario = u.id_usuario
            LEFT JOIN Licencia l ON s.id_licencia = l.id_licencia
            WHERE s.SN_equipo LIKE ? 
               OR s.marca_equipo LIKE ? 
               OR u.nombre LIKE ? 
               OR u.apellido_paterno LIKE ? 
               OR u.departamento LIKE ?
               OR s.SO_equipo LIKE ?
        ''', (search_term, search_term, search_term, search_term, search_term, search_term)).fetchall()
        conn.close()

    return render_template('busqueda.html', equipos=equipos, query=query, active_page='busqueda')

@app.route('/inventario')
def inventario():
    """Ruta para consultar el catálogo completo de equipos."""
    conn = get_db_connection()
    
    # Extraemos los datos del equipo, del usuario responsable y del tipo de licencia
    equipos = conn.execute('''
        SELECT 
            s.id_stock, s.SN_equipo, s.marca_equipo, s.procesador_equipo, 
            s.ram_equipo, s.almacenamiento_equipo, s.SO_equipo, 
            u.nombre, u.apellido_paterno, u.departamento,
            l.tipo_licencia
        FROM Stock s
        JOIN Usuario u ON s.id_usuario = u.id_usuario
        LEFT JOIN Licencia l ON s.id_licencia = l.id_licencia
    ''').fetchall()
    
    conn.close()
    
    return render_template('inventario.html', equipos=equipos, active_page='inventario')

@app.route('/mantenimiento')
def mantenimiento():
    """Módulo de auditoría: Lista equipos con información incompleta o sin licencia."""
    conn = get_db_connection()
    
    # Buscamos equipos donde CUALQUIER campo clave sea NULL o esté vacío ('')
    # Ignoramos id_usuario en la validación de nulos como solicitaste
    equipos_incompletos = conn.execute('''
        SELECT 
            s.*, 
            u.nombre, u.apellido_paterno, 
            l.tipo_licencia
        FROM Stock s
        LEFT JOIN Usuario u ON s.id_usuario = u.id_usuario
        LEFT JOIN Licencia l ON s.id_licencia = l.id_licencia
        WHERE s.id_licencia IS NULL
           OR s.marca_equipo IS NULL OR s.marca_equipo = ''
           OR s.procesador_equipo IS NULL OR s.procesador_equipo = ''
           OR s.ram_equipo IS NULL OR s.ram_equipo = ''
           OR s.almacenamiento_equipo IS NULL OR s.almacenamiento_equipo = ''
           OR s.SO_equipo IS NULL OR s.SO_equipo = ''
           OR s.marca_monitor IS NULL OR s.marca_monitor = ''
           OR s.pulgadas_monitor IS NULL OR s.pulgadas_monitor = ''
           OR s.marca_teclado IS NULL OR s.marca_teclado = ''
           OR s.marca_mouse IS NULL OR s.marca_mouse = ''
    ''').fetchall()
    conn.close()
    
    return render_template('mantenimiento.html', equipos=equipos_incompletos, active_page='mantenimiento')

# ==========================================
# RUTAS DE USUARIOS
# ==========================================

@app.route('/usuarios')
@app.route('/usuarios/editar/<int:id_usuario>')
def usuarios(id_usuario=None):
    """Muestra el formulario y el directorio. Si recibe un ID, precarga el formulario."""
    conn = get_db_connection()
    
    # Extraemos la lista de usuarios y contamos cuántos equipos tiene cada uno
    lista_usuarios = conn.execute('''
        SELECT u.*, COUNT(s.id_stock) as total_equipos
        FROM Usuario u
        LEFT JOIN Stock s ON u.id_usuario = s.id_usuario
        GROUP BY u.id_usuario
    ''').fetchall()
    
    # Si se pasó un ID en la URL, extraemos sus datos para editar
    usuario_edit = None
    if id_usuario:
        usuario_edit = conn.execute('SELECT * FROM Usuario WHERE id_usuario = ?', (id_usuario,)).fetchone()
        
    conn.close()
    return render_template('usuarios.html', usuarios=lista_usuarios, usuario_edit=usuario_edit, active_page='usuarios')


@app.route('/api/usuario', methods=['POST'])
def guardar_usuario():
    """Crea un usuario nuevo o actualiza uno existente."""
    id_usuario_original = request.form.get('id_usuario_original')
    nombre = request.form.get('nombre')
    apellido_paterno = request.form.get('apellido_paterno')
    apellido_materno = request.form.get('apellido_materno')
    edad = request.form.get('edad')
    departamento = request.form.get('departamento')

    conn = get_db_connection()
    
    if id_usuario_original:
        # Es una EDICIÓN
        conn.execute('''
            UPDATE Usuario SET 
                nombre=?, apellido_paterno=?, apellido_materno=?, edad=?, departamento=?
            WHERE id_usuario=?
        ''', (nombre, apellido_paterno, apellido_materno, edad, departamento, id_usuario_original))
    else:
        # Es un ALTA NUEVA (SQLite genera el ID automáticamente)
        conn.execute('''
            INSERT INTO Usuario (nombre, apellido_paterno, apellido_materno, edad, departamento) 
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, apellido_paterno, apellido_materno, edad, departamento))
        
    conn.commit()
    conn.close()
    
    return redirect(url_for('usuarios'))


@app.route('/eliminar_usuario/<int:id_usuario>', methods=['POST'])
def eliminar_usuario(id_usuario):
    """Elimina un usuario de la base de datos."""
    conn = get_db_connection()
    conn.execute('DELETE FROM Usuario WHERE id_usuario = ?', (id_usuario,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('usuarios'))


if __name__ == '__main__':
    # Inicializa la base de datos antes de arrancar el servidor
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
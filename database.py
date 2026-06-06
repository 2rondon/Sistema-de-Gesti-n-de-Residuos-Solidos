import sqlite3

def init_db():
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    
    # 1. Tabla de Usuarios (Autenticación)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # 2. Tabla de Camiones (Rutas de recolección)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS camiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT UNIQUE NOT NULL,
            modelo TEXT NOT NULL,
            capacidad_ton REAL NOT NULL,
            estado TEXT DEFAULT 'Activo' -- Activo, En Mantenimiento, Inactivo
        )
    """)

    # 3. Tabla de Personal (Choferes, Operadores)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            rol TEXT NOT NULL, -- Chofer, Operador, Supervisor
            telefono TEXT NOT NULL
        )
    """)

    # 4. Tabla de Cantidad de Residuos (Registro de Pesaje)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS residuos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT DEFAULT (DATE('now')),
            tipo_residuo TEXT NOT NULL, -- Orgánico, Plástico, Papel, Vidrio, Metal, General
            peso_ton REAL NOT NULL,
            placa_camion TEXT,
            FOREIGN KEY(placa_camion) REFERENCES camiones(placa) ON DELETE SET NULL
        )
    """)

    # 5. Tabla de Configuración (Preferencias de la app)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracion (
            clave TEXT PRIMARY KEY,
            valor TEXT NOT NULL
        )
    """)
    
    # --- Datos por defecto si las tablas están vacías ---
    
    # Usuario Admin por defecto
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)", 
                       ("Administrador", "admin@correo.com", "admin123"))
        print("➡️ Usuario administrador por defecto creado.")

    # Parámetros de configuración iniciales
    cursor.execute("SELECT COUNT(*) FROM configuracion")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO configuracion (clave, valor) VALUES (?, ?)", ("modo_oscuro", "True"))
        cursor.execute("INSERT INTO configuracion (clave, valor) VALUES (?, ?)", ("limite_alerta_ton", "10.0"))
        print("➡️ Parámetros de configuración iniciales establecidos.")
        
    conn.commit()
    conn.close()


# =========================================================================
# 👤 CRUD: USUARIOS
# =========================================================================

def registrar_usuario(nombre, email, password):
    try:
        conn = sqlite3.connect("sistema_residuos.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)", (nombre, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verificar_usuario(email, password):
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM usuarios WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user


# =========================================================================
# 🚛 CRUD: CAMIONES
# =========================================================================

def crear_camion(placa, modelo, capacidad):
    try:
        conn = sqlite3.connect("sistema_residuos.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO camiones (placa, modelo, capacidad_ton) VALUES (?, ?, ?)", (placa, modelo, capacidad))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def obtener_camiones():
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, placa, modelo, capacidad_ton, estado FROM camiones")
    datos = cursor.fetchall()
    conn.close()
    return datos

def eliminar_camion(camion_id):
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM camiones WHERE id = ?", (camion_id,))
    conn.commit()
    conn.close()


# =========================================================================
# 👥 CRUD: PERSONAL
# =========================================================================

def crear_personal(cedula, nombre, rol, telefono):
    try:
        conn = sqlite3.connect("sistema_residuos.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personal (cedula, nombre, rol, telefono) VALUES (?, ?, ?, ?)", (cedula, nombre, rol, telefono))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def obtener_personal():
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, cedula, nombre, rol, telefono FROM personal")
    datos = cursor.fetchall()
    conn.close()
    return datos

def eliminar_personal(personal_id):
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personal WHERE id = ?", (personal_id,))
    conn.commit()
    conn.close()


# =========================================================================
# 📊 CRUD Y MODIFICACIONES: CANTIDAD DE RESIDUOS
# =========================================================================

def registrar_pesaje_residuo(tipo_residuo, peso_ton, placa_camion):
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO residuos (tipo_residuo, peso_ton, placa_camion) VALUES (?, ?, ?)", (tipo_residuo, peso_ton, placa_camion))
    conn.commit()
    conn.close()

def obtener_registros_residuos():
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, fecha, tipo_residuo, peso_ton, placa_camion FROM residuos ORDER BY id DESC")
    datos = cursor.fetchall()
    conn.close()
    return datos

def actualizar_residuo(id_registro, tipo_residuo, peso_ton, placa_camion):
    """Actualiza los datos de un pesaje específico por su ID"""
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE residuos 
        SET tipo_residuo = ?, peso_ton = ?, placa_camion = ?
        WHERE id = ?
    """, (tipo_residuo, peso_ton, placa_camion, id_registro))
    conn.commit()
    conn.close()

def eliminar_residuo(id_registro):
    """Elimina permanentemente un registro de pesaje por su ID"""
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM residuos WHERE id = ?", (id_registro,))
    conn.commit()
    conn.close()

# 🔄 MODIFICADO: Ahora calcula los residuos segmentados por Día, Mes y Año para las 4 tarjetas
def obtener_metricas_dashboard():
    """Retorna los camiones activos y la suma de residuos agrupados por períodos de tiempo"""
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    
    # 1. Contar camiones activos
    cursor.execute("SELECT COUNT(*) FROM camiones WHERE estado = 'Activo'")
    camiones_activos = cursor.fetchone()[0] or 0
    
    # 2. Sumar el peso total recolectado HOY
    cursor.execute("SELECT SUM(peso_ton) FROM residuos WHERE fecha = DATE('now')")
    residuos_dia = cursor.fetchone()[0] or 0.0
    
    # 3. Sumar el peso total recolectado en el MES ACTUAL (Formato: YYYY-MM)
    cursor.execute("SELECT SUM(peso_ton) FROM residuos WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')")
    residuos_mes = cursor.fetchone()[0] or 0.0
    
    # 4. Sumar el peso total recolectado en el AÑO ACTUAL (Formato: YYYY)
    cursor.execute("SELECT SUM(peso_ton) FROM residuos WHERE strftime('%Y', fecha) = strftime('%Y', 'now')")
    residuos_ano = cursor.fetchone()[0] or 0.0
    
    conn.close()
    return camiones_activos, residuos_dia, residuos_mes, residuos_ano


# =========================================================================
# ⚙️ CRUD: CONFIGURACIÓN (SETTINGS)
# =========================================================================

def obtener_configuracion():
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT clave, valor FROM configuracion")
    datos = dict(cursor.fetchall())
    conn.close()
    return datos

def actualizar_configuracion(clave, valor):
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO configuracion (clave, valor) VALUES (?, ?)", (clave, valor))
    conn.commit()
    conn.close()

# =========================================================================
# 📈 CONSULTAS AVANZADAS PARA REPORTES
# =========================================================================

def obtener_estadisticas_por_tipo():
    """Retorna el total de toneladas recolectadas agrupadas por tipo de residuo"""
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tipo_residuo, SUM(peso_ton) as total 
        FROM residuos 
        GROUP BY tipo_residuo
        ORDER BY total DESC
    """)
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_reporte_detallado():
    """Retorna un historial completo con detalles del camión para el balance general"""
    conn = sqlite3.connect("sistema_residuos.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id, r.fecha, r.tipo_residuo, r.peso_ton, r.placa_camion, c.modelo
        FROM residuos r
        LEFT JOIN camiones c ON r.placa_camion = c.placa
        ORDER BY r.fecha DESC, r.id DESC
    """)
    datos = cursor.fetchall()
    conn.close()
    return datos
"""
Módulo de conexión a la base de datos SQLite para ChromaBags
"""

import sqlite3
import os

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'chromabags.db')

def get_connection():
    """
    Obtiene una conexión a la base de datos SQLite
    
    Returns:
        sqlite3.Connection: Conexión a la base de datos o None si hay error
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        # Configurar row_factory para acceder a columnas por nombre
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

def init_db():
    """
    Inicializa la base de datos creando las tablas si no existen
    Útil para desarrollo y primeras ejecuciones
    """
    conn = get_connection()
    if not conn:
        print("No se pudo conectar a la base de datos para inicializarla")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Aquí podrías agregar scripts de inicialización si es necesario
        # Por ahora, solo verificamos que la conexión funciona
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Base de datos inicializada. Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        if conn:
            conn.close()
        return False

def test_connection():
    """
    Prueba la conexión a la base de datos
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            print("✓ Conexión a la base de datos exitosa")
            return True
        except Exception as e:
            print(f"✗ Error al ejecutar consulta de prueba: {e}")
            if conn:
                conn.close()
            return False
    else:
        print("✗ No se pudo establecer conexión con la base de datos")
        return False

if __name__ == "__main__":
    # Prueba de conexión cuando se ejecuta directamente
    print("=== Prueba de Conexión a ChromaBags DB ===")
    print(f"Ruta de la base de datos: {DB_PATH}")
    print(f"Archivo existe: {os.path.exists(DB_PATH)}")
    print()
    
    if test_connection():
        print()
        init_db()
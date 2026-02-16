import sqlite3
import os
import sys

def get_database_path():
    # Si es ejecutable (.exe)
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        # Si es script normal
        base_path = os.path.dirname(os.path.abspath(__file__))

    data_folder = os.path.join(base_path, "Data")

    # Crear carpeta si no existe
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    return os.path.join(data_folder, "products.db")

def connect():
    db_path = get_database_path()
    return sqlite3.connect(db_path)

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            costo REAL NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    
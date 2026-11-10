import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()

def obtener_motor() -> str:
    """Devuelve el motor de base de datos configurado ('mysql' o 'sqlite')."""
    return os.getenv("DB_ENGINE", "sqlite").lower()

def obtener_configuracion() -> dict:
    """Devuelve un diccionario con toda la configuración actual de conexión."""
    motor = obtener_motor()
    # Si es mysql por defecto usa ecotech_db, si es sqlite usa ecotech.db
    db_name_default = "ecotech_db" if motor == "mysql" else "ecotech.db"
    
    return {
        "engine": motor,
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "javier"),
        "database": os.getenv("DB_NAME", db_name_default),
    }

def abrir_conexion_servidor():
    """
    Conecta al servidor de base de datos para operaciones globales 
    (como crear la base de datos si no existe en MySQL).
    Para SQLite, solo conecta al archivo local.
    """
    config = obtener_configuracion()
    
    if config["engine"] == "sqlite":
        return sqlite3.connect(config["database"])
        
    if config["engine"] == "mysql":
        return pymysql.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            charset="utf8mb4",
        )
        
    raise ValueError(f"Motor de base de datos no soportado: {config['engine']}")

def abrir_conexion():
    """
    Conecta directamente a la base de datos seleccionada 
    (lista para hacer consultas con los DAOs).
    """
    config = obtener_configuracion()
    
    if config["engine"] == "sqlite":
        conexion = sqlite3.connect(config["database"])
        # Activar restricciones de claves foráneas en SQLite
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion
        
    if config["engine"] == "mysql":
        return pymysql.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            charset="utf8mb4",
        )
        
    raise ValueError(f"Motor de base de datos no soportado: {config['engine']}")

def marcador_sql() -> str:
    """Devuelve el marcador de parámetros SQL correcto según el motor activo."""
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"
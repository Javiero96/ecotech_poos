import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def obtener_configuracion() -> dict:
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "ecotech"),
    }

def abrir_conexion_servidor():
    """Conecta al servidor MySQL para crear la base de datos si no existe."""
    config = obtener_configuracion()
    return pymysql.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
        charset="utf8mb4",
    )

def abrir_conexion():
    """Conecta directamente a la base de datos MySQL."""
    config = obtener_configuracion()
    return pymysql.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        charset="utf8mb4",
    )

def marcador_sql() -> str:
    return "%s"
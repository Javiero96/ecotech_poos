from persistencia.conexion import (
    abrir_conexion_servidor, 
    abrir_conexion, 
    obtener_configuracion, 
    obtener_motor
)

def crear_base_y_tablas():
    motor = obtener_motor()
    
    # 1. Crear base de datos (SOLO PARA MYSQL)
    if motor == "mysql":
        config = obtener_configuracion()
        nombre_bd = config["database"]

        conexion_srv = abrir_conexion_servidor()
        cursor_srv = conexion_srv.cursor()
        try:
            cursor_srv.execute(
                f"CREATE DATABASE IF NOT EXISTS `{nombre_bd}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            conexion_srv.commit()
        finally:
            cursor_srv.close()
            conexion_srv.close()

    # 2. Crear Tablas según el motor
    conexion = abrir_conexion()
    cursor = conexion.cursor()
    
    try:
        if motor == "sqlite":
            # --- SINTAXIS PARA SQLITE ---
            # SQLite permite referenciar tablas que aún no se crean dentro del mismo script
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamento (
                    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NULL,
                    id_gerente INTEGER NULL,
                    FOREIGN KEY (id_gerente) REFERENCES empleado(id_empleado)
                        ON UPDATE CASCADE ON DELETE SET NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleado (
                    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT NOT NULL UNIQUE,
                    id_departamento INTEGER NULL,
                    FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento)
                        ON UPDATE CASCADE ON DELETE SET NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proyecto (
                    id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NULL,
                    fecha_inicio DATE NOT NULL,
                    fecha_fin DATE NULL,
                    estado TEXT NOT NULL DEFAULT 'pendiente'
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS registro_tiempo (
                    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_empleado INTEGER NOT NULL,
                    id_proyecto INTEGER NOT NULL,
                    fecha DATE NOT NULL,
                    horas_trabajadas REAL NOT NULL,
                    descripcion_trabajo TEXT NULL,
                    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado) ON DELETE CASCADE,
                    FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_usuario TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    id_empleado INTEGER NOT NULL UNIQUE,
                    rol TEXT NOT NULL DEFAULT 'empleado' CHECK (rol IN ('admin', 'empleado')),
                    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
                        ON DELETE CASCADE ON UPDATE CASCADE
                )
            """)

            # ---> NUEVA TABLA PARA LA API (SQLITE) <---
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS indicador_api (
                    id_indicador INTEGER PRIMARY KEY AUTOINCREMENT,
                    fuente TEXT,
                    codigo TEXT,
                    fecha TEXT,
                    valor REAL,
                    unidad TEXT,
                    verificado_en TEXT
                )
            """)

        else:
            # --- SINTAXIS PARA MYSQL ---
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamento (
                    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion TEXT NULL,
                    id_gerente INT NULL
                ) ENGINE=InnoDB
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleado (
                    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    correo VARCHAR(150) NOT NULL UNIQUE,
                    id_departamento INT NULL,
                    CONSTRAINT fk_empleado_departamento
                        FOREIGN KEY (id_departamento)
                        REFERENCES departamento(id_departamento)
                        ON UPDATE CASCADE ON DELETE SET NULL
                ) ENGINE=InnoDB
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proyecto (
                    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion TEXT NULL,
                    fecha_inicio DATE NOT NULL,
                    fecha_fin DATE NULL,
                    estado VARCHAR(50) NOT NULL DEFAULT 'pendiente'
                ) ENGINE=InnoDB
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS registro_tiempo (
                    id_registro INT AUTO_INCREMENT PRIMARY KEY,
                    id_empleado INT NOT NULL,
                    id_proyecto INT NOT NULL,
                    fecha DATE NOT NULL,
                    horas_trabajadas DECIMAL(5,2) NOT NULL,
                    descripcion_trabajo TEXT NULL,
                    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado) ON DELETE CASCADE,
                    FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
                ) ENGINE=InnoDB
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    id_empleado INT NOT NULL UNIQUE,
                    rol TEXT NOT NULL DEFAULT 'empleado'
                    CHECK (rol IN ('admin', 'empleado')),
                    CONSTRAINT fk_usuario_empleado
                        FOREIGN KEY (id_empleado)
                        REFERENCES empleado(id_empleado)
                        ON DELETE CASCADE ON UPDATE CASCADE
                ) ENGINE=InnoDB
            """)

            # ---> NUEVA TABLA PARA LA API (MYSQL) <---
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS indicador_api (
                    id_indicador INT AUTO_INCREMENT PRIMARY KEY,
                    fuente VARCHAR(50),
                    codigo VARCHAR(20),
                    fecha VARCHAR(20),
                    valor FLOAT,
                    unidad VARCHAR(20),
                    verificado_en VARCHAR(30)
                ) ENGINE=InnoDB
            """)

            # MySQL requiere alterar la tabla después porque no deja referenciar tablas inexistentes
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.TABLE_CONSTRAINTS
                WHERE CONSTRAINT_SCHEMA=%s
                AND TABLE_NAME='departamento'
                AND CONSTRAINT_NAME='fk_departamento_gerente'
            """, (nombre_bd,))
            
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    ALTER TABLE departamento
                    ADD CONSTRAINT fk_departamento_gerente
                    FOREIGN KEY (id_gerente)
                    REFERENCES empleado(id_empleado)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
                """)

        conexion.commit()
        
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    crear_base_y_tablas()
    motor = obtener_motor()
    print(f"Base de datos y tablas preparadas exitosamente usando el motor: {motor.upper()}.")
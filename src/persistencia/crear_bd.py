from persistencia.conexion import abrir_conexion_servidor, abrir_conexion, obtener_configuracion

def crear_base_y_tablas():
    config = obtener_configuracion()
    nombre_bd = config["database"]

    conexion = abrir_conexion_servidor()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{nombre_bd}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()

    conexion = abrir_conexion()
    cursor = conexion.cursor()
    try:
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
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
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
                FOREIGN KEY (id_empleado)
                    REFERENCES empleado(id_empleado)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_proyecto)
                    REFERENCES proyecto(id_proyecto)
                    ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                id_empleado INT NOT NULL UNIQUE,
                CONSTRAINT fk_usuario_empleado
                    FOREIGN KEY (id_empleado)
                    REFERENCES empleado(id_empleado)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            ) ENGINE=InnoDB
        """)

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
    print("Base de datos y tablas MySQL creadas exitosamente.")
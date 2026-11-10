from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion, marcador_sql

class UsuarioDAO:
    @staticmethod
    def insertar(usuario: Usuario) -> Usuario:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"""
            INSERT INTO usuario (nombre_usuario, password_hash, id_empleado, rol)
            VALUES ({m}, {m}, {m}, {m})
        """
        cursor.execute(
            sql,
            (
                usuario.nombre_usuario,
                usuario.password_hash,
                usuario.empleado_id,
                usuario.rol, # <-- Agregado para guardar el rol correctamente
            ),
        )
        usuario.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return usuario

    @staticmethod
    def buscar_por_id(id_usuario: int):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"""
            SELECT id_usuario, nombre_usuario, password_hash, id_empleado, rol
            FROM usuario WHERE id_usuario = {m}
        """
        cursor.execute(sql, (id_usuario,))
        fila = cursor.fetchone()
        conexion.close()

        if not fila:
            return None

        return Usuario(
            id=fila[0],
            nombre_usuario=fila[1],
            password_hash=fila[2],
            empleado_id=fila[3],
            rol=fila[4], # <-- Agregado para recuperar el rol
        )

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = """
            SELECT id_usuario, nombre_usuario, password_hash, id_empleado, rol
            FROM usuario
        """
        cursor.execute(sql)
        filas = cursor.fetchall()
        conexion.close()

        usuarios = []
        for fila in filas:
            usuarios.append(
                Usuario(
                    id=fila[0],
                    nombre_usuario=fila[1],
                    password_hash=fila[2],
                    empleado_id=fila[3],
                    rol=fila[4], # <-- Agregado para recuperar el rol en la lista
                )
            )
        return usuarios

    @staticmethod
    def actualizar_clave(id_usuario: int, nuevo_password_hash: str) -> bool:
        """Omoambue pe contraseña hash usuario mba'e."""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"""
            UPDATE usuario
            SET password_hash = {m}
            WHERE id_usuario = {m}
        """
        cursor.execute(sql, (nuevo_password_hash, id_usuario))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def eliminar(id_usuario: int) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"DELETE FROM usuario WHERE id_usuario = {m}"
        cursor.execute(sql, (id_usuario,))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def buscar_por_nombre(nombre_usuario: str):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"SELECT id_usuario, nombre_usuario, password_hash, id_empleado, rol FROM usuario WHERE nombre_usuario = {m}"
        cursor.execute(sql, (nombre_usuario.strip().lower(),))
        fila = cursor.fetchone()
        conexion.close()

        if not fila:
            return None

        return Usuario(
            id=fila[0],
            nombre_usuario=fila[1],
            password_hash=fila[2],
            empleado_id=fila[3],
            rol=fila[4], # <-- Agregado crucial para que el login reconozca si es admin o empleado
        )
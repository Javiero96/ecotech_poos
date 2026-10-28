from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.proyecto import Proyecto
from datetime import date

class ProyectoDAO:
    @staticmethod
    def insertar(proyecto: Proyecto) -> Proyecto:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO proyecto (nombre, descripcion, fecha_inicio, fecha_fin, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, proyecto.fecha_fin, proyecto.estado))
        proyecto.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return proyecto

    @staticmethod
    def buscar_por_id(id_proyecto: int):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "SELECT id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin, estado FROM proyecto WHERE id_proyecto = %s"
        cursor.execute(sql, (id_proyecto,))
        fila = cursor.fetchone()
        conexion.close()

        if not fila:
            return None
        return Proyecto(id=fila[0], nombre=fila[1], descripcion=fila[2], fecha_inicio=fila[3], fecha_fin=fila[4], estado=fila[5])

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin, estado FROM proyecto")
        filas = cursor.fetchall()
        conexion.close()

        return [Proyecto(id=f[0], nombre=f[1], descripcion=f[2], fecha_inicio=f[3], fecha_fin=f[4], estado=f[5]) for f in filas]

    @staticmethod
    def actualizar_datos(id_proyecto: int, nombre: str, descripcion: str) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE proyecto SET nombre = %s, descripcion = %s WHERE id_proyecto = %s"
        cursor.execute(sql, (nombre, descripcion, id_proyecto))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def actualizar_fechas(id_proyecto: int, fecha_inicio: date, fecha_fin: date) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE proyecto SET fecha_inicio = %s, fecha_fin = %s WHERE id_proyecto = %s"
        cursor.execute(sql, (fecha_inicio, fecha_fin, id_proyecto))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def cambiar_estado(id_proyecto: int, estado: str) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE proyecto SET estado = %s WHERE id_proyecto = %s"
        cursor.execute(sql, (estado, id_proyecto))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito
from persistencia.conexion import abrir_conexion, marcador_sql
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from dominio.registroTiempo import RegistroTiempo
from datetime import date

class RegistroTiempoDAO:
    @staticmethod
    def insertar(registro: RegistroTiempo) -> RegistroTiempo:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO registro_tiempo (id_empleado, id_proyecto, fecha, horas_trabajadas, descripcion_trabajo)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (registro.empleado.id, registro.proyecto.id, registro.fecha, registro.horas, registro.descripcion))
        registro.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return registro

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_registro, id_empleado, id_proyecto, fecha, horas_trabajadas, descripcion_trabajo FROM registro_tiempo")
        filas = cursor.fetchall()
        conexion.close()

        registros = []
        for fila in filas:
            emp = EmpleadoDAO.buscar_por_id(fila[1])
            proy = ProyectoDAO.buscar_por_id(fila[2])
            registros.append(RegistroTiempo(id=fila[0], empleado=emp, proyecto=proy, fecha=fila[3], horas=float(fila[4]), descripcion=fila[5]))
        return registros

    @staticmethod
    def actualizar_detalle(id_registro: int, fecha: date, horas: float, descripcion: str) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = """
            UPDATE registro_tiempo 
            SET fecha = %s, horas_trabajadas = %s, descripcion_trabajo = %s 
            WHERE id_registro = %s
        """
        cursor.execute(sql, (fecha, horas, descripcion, id_registro))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito
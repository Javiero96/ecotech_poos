from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.departamento import Departamento
from persistencia.empleado_dao import EmpleadoDAO

class DepartamentoDAO:
    @staticmethod
    def insertar(departamento: Departamento) -> Departamento:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        gerente_id = departamento.gerente.id if departamento.gerente else None

        sql = "INSERT INTO departamento (nombre, descripcion, id_gerente) VALUES (%s, %s, %s)"
        cursor.execute(sql, (departamento.nombre, departamento.descripcion, gerente_id))
        departamento.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return departamento

    @staticmethod
    def buscar_por_id(id_departamento: int):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "SELECT id_departamento, nombre, descripcion, id_gerente FROM departamento WHERE id_departamento = %s"
        cursor.execute(sql, (id_departamento,))
        fila = cursor.fetchone()
        conexion.close()

        if not fila:
            return None
        gerente = EmpleadoDAO.buscar_por_id(fila[3]) if fila[3] else None
        return Departamento(id=fila[0], nombre=fila[1], descripcion=fila[2], gerente=gerente)

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_departamento, nombre, descripcion, id_gerente FROM departamento")
        filas = cursor.fetchall()
        conexion.close()

        deptos = []
        for fila in filas:
            gerente = EmpleadoDAO.buscar_por_id(fila[3]) if fila[3] else None
            deptos.append(Departamento(id=fila[0], nombre=fila[1], descripcion=fila[2], gerente=gerente))
        return deptos

    @staticmethod
    def actualizar_datos(id_departamento: int, nombre: str, descripcion: str) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE departamento SET nombre = %s, descripcion = %s WHERE id_departamento = %s"
        cursor.execute(sql, (nombre, descripcion, id_departamento))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def asignar_gerente(id_departamento: int, id_gerente: int) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE departamento SET id_gerente = %s WHERE id_departamento = %s"
        cursor.execute(sql, (id_gerente, id_departamento))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito
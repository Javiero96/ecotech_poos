from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.departamento import Departamento

class EmpleadoDAO:
    @staticmethod
    def insertar(empleado: Empleado) -> Empleado:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        depto_id = empleado.departamento.id if empleado.departamento else None

        sql = "INSERT INTO empleado (nombre, correo, id_departamento) VALUES (%s, %s, %s)"
        cursor.execute(sql, (empleado.nombre, empleado.correo, depto_id))
        empleado.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return empleado

    @staticmethod
    def buscar_por_id(id_empleado: int):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "SELECT id_empleado, nombre, correo, id_departamento FROM empleado WHERE id_empleado = %s"
        cursor.execute(sql, (id_empleado,))
        fila = cursor.fetchone()
        conexion.close()

        if not fila:
            return None
        depto = Departamento(id=fila[3], nombre="", descripcion="") if fila[3] else None
        return Empleado(id=fila[0], nombre=fila[1], correo=fila[2], departamento=depto)

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_empleado, nombre, correo, id_departamento FROM empleado")
        filas = cursor.fetchall()
        conexion.close()
        return [Empleado(id=f[0], nombre=f[1], correo=f[2]) for f in filas]

    @staticmethod
    def actualizar_datos(id_empleado: int, nombre: str, correo: str) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE empleado SET nombre = %s, correo = %s WHERE id_empleado = %s"
        cursor.execute(sql, (nombre, correo, id_empleado))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def cambiar_departamento(id_empleado: int, id_departamento: int) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE empleado SET id_departamento = %s WHERE id_empleado = %s"
        cursor.execute(sql, (id_departamento, id_empleado))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito



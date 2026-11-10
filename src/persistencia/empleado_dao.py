from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.departamento import Departamento

class EmpleadoDAO:
    @staticmethod
    def insertar(empleado: Empleado) -> Empleado:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        depto_id = empleado.departamento.id if empleado.departamento else None
        
        m = marcador_sql()
        sql = f"INSERT INTO empleado (nombre, correo, id_departamento) VALUES ({m}, {m}, {m})"
        cursor.execute(sql, (empleado.nombre, empleado.correo, depto_id))
        empleado.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return empleado

    @staticmethod
    def buscar_por_id(id_empleado: int):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"SELECT id_empleado, nombre, correo, id_departamento FROM empleado WHERE id_empleado = {m}"
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
        
        m = marcador_sql()
        sql = f"UPDATE empleado SET nombre = {m}, correo = {m} WHERE id_empleado = {m}"
        cursor.execute(sql, (nombre, correo, id_empleado))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def cambiar_departamento(id_empleado: int, id_departamento: int) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"UPDATE empleado SET id_departamento = {m} WHERE id_empleado = {m}"
        cursor.execute(sql, (id_departamento, id_empleado))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def buscar_por_correo(correo: str):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"SELECT id_empleado, nombre, correo, id_departamento FROM empleado WHERE correo = {m}"
        cursor.execute(sql, (correo,))
        fila = cursor.fetchone()
        conexion.close()

        if not fila:
            return None
    
        # Creamos un departamento base para mantener la estructura del objeto Empleado
        depto = Departamento(id=fila[3], nombre="", descripcion="") if fila[3] else None
        return Empleado(id=fila[0], nombre=fila[1], correo=fila[2], departamento=depto)
from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.proyecto import Proyecto
from datetime import date

class ProyectoDAO:
    
    @staticmethod
    def _parsear_fecha(valor):
        """Convierte una cadena de texto a un objeto date (necesario para SQLite)."""
        if isinstance(valor, str):
            # Asume el formato 'YYYY-MM-DD'
            return date.fromisoformat(valor.split(" ")[0])
        return valor

    @staticmethod
    def insertar(proyecto: Proyecto) -> Proyecto:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"""
            INSERT INTO proyecto (nombre, descripcion, fecha_inicio, fecha_fin, estado)
            VALUES ({m}, {m}, {m}, {m}, {m})
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
        
        m = marcador_sql()
        sql = f"SELECT id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin, estado FROM proyecto WHERE id_proyecto = {m}"
        cursor.execute(sql, (id_proyecto,))
        fila = cursor.fetchone()
        conexion.close()

        if not fila:
            return None
            
        fecha_ini = ProyectoDAO._parsear_fecha(fila[3])
        fecha_f = ProyectoDAO._parsear_fecha(fila[4]) if fila[4] else None
        
        return Proyecto(id=fila[0], nombre=fila[1], descripcion=fila[2], fecha_inicio=fecha_ini, fecha_fin=fecha_f, estado=fila[5])

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin, estado FROM proyecto")
        filas = cursor.fetchall()
        conexion.close()

        proyectos = []
        for f in filas:
            fecha_ini = ProyectoDAO._parsear_fecha(f[3])
            fecha_f = ProyectoDAO._parsear_fecha(f[4]) if f[4] else None
            proyectos.append(Proyecto(id=f[0], nombre=f[1], descripcion=f[2], fecha_inicio=fecha_ini, fecha_fin=fecha_f, estado=f[5]))

        return proyectos

    @staticmethod
    def actualizar_datos(id_proyecto: int, nombre: str, descripcion: str) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"UPDATE proyecto SET nombre = {m}, descripcion = {m} WHERE id_proyecto = {m}"
        cursor.execute(sql, (nombre, descripcion, id_proyecto))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def actualizar_fechas(id_proyecto: int, fecha_inicio: date, fecha_fin: date) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"UPDATE proyecto SET fecha_inicio = {m}, fecha_fin = {m} WHERE id_proyecto = {m}"
        cursor.execute(sql, (fecha_inicio, fecha_fin, id_proyecto))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def cambiar_estado(id_proyecto: int, estado: str) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"UPDATE proyecto SET estado = {m} WHERE id_proyecto = {m}"
        cursor.execute(sql, (estado, id_proyecto))
        conexion.commit()
        exito = cursor.rowcount > 0
        conexion.close()
        return exito

    @staticmethod
    def buscar_por_nombre(nombre: str):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        m = marcador_sql()
        sql = f"SELECT id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin, estado FROM proyecto WHERE nombre = {m}"
        cursor.execute(sql, (nombre,))
        fila = cursor.fetchone()
        conexion.close()

        if not fila:
            return None
        
        fecha_ini = ProyectoDAO._parsear_fecha(fila[3])
        fecha_f = ProyectoDAO._parsear_fecha(fila[4]) if fila[4] else None
        
        return Proyecto(
            id=fila[0], 
            nombre=fila[1], 
            descripcion=fila[2], 
            fecha_inicio=fecha_ini, 
            fecha_fin=fecha_f, 
            estado=fila[5]
        )
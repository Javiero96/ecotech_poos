from servicios.permisos import exigir_sesion
from persistencia.registro_tiempo_dao import RegistroTiempoDAO 
from persistencia.empleado_dao import EmpleadoDAO

def mis_registros(sesion: dict):
    exigir_sesion(sesion)
    return RegistroTiempoDAO.listar_por_empleado(sesion["empleado_id"])

def actualizar_mis_datos(sesion: dict, nombre: str, correo: str):
    exigir_sesion(sesion)
    
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("Empleado no encontrado en la base de datos.")
    
    empleado.nombre = nombre
    empleado.correo = correo
    
    return EmpleadoDAO.actualizar(empleado)
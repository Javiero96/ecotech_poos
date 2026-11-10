from servicios.permisos import exigir_admin
from persistencia.empleado_dao import EmpleadoDAO

def listar_todos_los_empleados(sesion: dict):
    exigir_admin(sesion) # Si no es admin, lanza error y no llega al DAO
    return EmpleadoDAO.listar()
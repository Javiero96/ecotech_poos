from persistencia.conexion import abrir_conexion
from servicios.autenticacion import registrar_usuario
from persistencia.empleado_dao import EmpleadoDAO

def reparar_acceso():
    # 1. Borramos al admin corrupto directamente de la base de datos
    conexion = abrir_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuario WHERE nombre_usuario = 'admin'")
    conexion.commit()
    conexion.close()
    print("[1] Admin defectuoso eliminado.")

    # 2. Buscamos el ID del empleado que le corresponde al admin
    empleado = EmpleadoDAO.buscar_por_correo("admin@ecotech.example")
    
    if not empleado:
        print("[!] Error: No se encontró al empleado admin. Corre semilla.py primero.")
        return

    # 3. Creamos el usuario usando tu función real que SÍ encripta la clave
    try:
        registrar_usuario(empleado.id, "admin", "admin123")
        print("[2] Admin nuevo creado correctamente con contraseña encriptada.")
        print("¡Ya puedes ir a tu main y entrar con admin / admin123!")
    except Exception as e:
        print(f"[!] Error al registrar: {e}")

if __name__ == "__main__":
    reparar_acceso()
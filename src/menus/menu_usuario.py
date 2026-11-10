import getpass
from entradas import pedir_dato
from servicios.autenticacion import registrar_usuario, autenticar
from dominio.usuario import Usuario
from menus.menu_indicadores import menu_indicadores
from menus.menu import menu_admin

def solicitar_registro(usuario_actual):
    """Solo los administradores pueden registrar nuevas cuentas de usuario."""
    if usuario_actual.get("rol") != "admin":
        print("\n[!] Acceso denegado: Solo el Administrador puede registrar usuarios.")
        return None
        
    try:
        print("\n--- REGISTRO DE NUEVO USUARIO ---")
        empleado_id = pedir_dato("ID del empleado al que pertenecerá la cuenta: ", int)
        nombre = pedir_dato("Nuevo nombre de usuario: ", Usuario.normalizar_usuario)
        
        # Opcional: Preguntar el rol si deseas crearlos como admin o empleado
        print("Roles disponibles: 1. empleado, 2. admin")
        opcion_rol = input("Elige el rol (por defecto es empleado): ").strip()
        rol = "admin" if opcion_rol == "2" else "empleado"

        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass.getpass)
    
        if clave != getpass.getpass("Repita la contraseña: "):
            print("\n[!] Las contraseñas no coinciden. Vuelva al registro.")
            return None

        # Nota: Asegúrate de que tu función registrar_usuario en autenticacion.py 
        # acepte el parámetro rol=rol si lo modificaste, o si pasas el objeto Usuario completo.
        usuario_id = registrar_usuario(empleado_id, nombre, clave, rol=rol)
        
    except (TypeError, ValueError) as error:
        print(f"\n[!] Error de validación: {error}")
        return None
    except Exception as error:
        print(f"\n[!] Error en BD (¿El ID de empleado existe o ya tiene usuario?): {error}")
        return None
    
    print(f"\n¡Cuenta creada correctamente! ID de usuario: {usuario_id} | Rol asignado: {rol}")
    return usuario_id


def solicitar_login():
    """Autentica al usuario y devuelve el diccionario de sesión con su rol."""
    print("\n--- INICIO DE SESIÓN ---")
    nombre = input("Usuario: ")
    clave = getpass.getpass("Contraseña: ")
    
    try:
        # autenticar() debe devolver el diccionario: {"id": X, "empleado_id": Y, "nombre_usuario": Z, "rol": "admin"/"empleado"}
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
        
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print(f"\nSesión iniciada correctamente. Bienvenido(a) {usuario['nombre_usuario']}!")
        print(f"Rol asignado: {usuario['rol'].upper()}")
        
    return usuario


def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return
        
    print("\n--- MI PERFIL ---")
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado ID: {usuario_actual['empleado_id']}")
    print(f"Rol en el sistema: {usuario_actual['rol'].upper()}")


def consultar_indicador(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return
    menu_indicadores()


def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
        
    while True:
        # El menú se adapta visualmente al rol de quien entró
        print(f"\n=== MENÚ PRINCIPAL ({usuario_actual['rol'].upper()}) ===")
        print("1. Ver mi Perfil")
        print("2. Consultar Indicadores (API Dólar)")
        
        # 2. MOSTRAR OPCIONES SEGÚN ROL: Solo el admin ve la opción de registro
        if usuario_actual["rol"] == "admin":
            print("3. Registrar nuevo usuario (Solo Admin)")
            print("4. Acceder al menú de administración")

        
        print("9. Cerrar sesión")
        print("0. Salir")
        
        opcion = input("Opción: ").strip()
        
        if opcion in ("0", "9"):
            return opcion
            
        if opcion == "1":
            mostrar_perfil(usuario_actual)
            
        elif opcion == "2":
            consultar_indicador(usuario_actual)
            
        elif opcion == "3":
            # 3. DOBLE PROTECCIÓN: Validamos de nuevo por si un empleado escribe '3' a la fuerza
            if usuario_actual["rol"] == "admin":
                solicitar_registro(usuario_actual)
            else:
                print("\n[!] Opción no válida.")
        elif opcion == "4":
            if usuario_actual["rol"] == "admin":
                try:
                    menu_admin()
                except PermissionError as error:
                    print(f"\n[!] ACCESO DENEGADO: {error}")
            else:
                print("Opción inválida.")
                
        else:
            print("\n[!] Opción no válida.")
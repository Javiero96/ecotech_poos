from menus.menu_usuario import  menu_privado
from menus.menu_usuario import solicitar_login, menu_privado
from persistencia.crear_bd import crear_base_y_tablas
from persistencia.crear_semilla import cargar_semillas
from menus.menu_indicadores import menu_indicadores
from menus.menu_usuario import solicitar_login, menu_privado

def iniciar_aplicacion():
    while True:
        print("\n=== BIENVENIDO A ECOTECH ===")
        print("1. Iniciar sesión")
        print("0. Salir del sistema")
        
        opcion = input("Elige una opción: ").strip()
        
        if opcion == "1":
            # 1. Llamamos a la función que pide usuario y clave
            usuario_logeado = solicitar_login()
            
            # 2. Si las credenciales son correctas, entramos al menú privado
            if usuario_logeado is not None:
                menu_privado(usuario_logeado)
                
        elif opcion == "0":
            print("\nSaliendo del sistema. ¡Hasta pronto!")
            break
            
        else:
            print("\n[!] Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    crear_base_y_tablas()
    cargar_semillas()
    iniciar_aplicacion()


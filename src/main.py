from menus.menu import menu_principal
from menus.menu_usuario import solicitar_login, menu_privado
from persistencia.crear_bd import crear_base_y_tablas
from persistencia.crear_semilla import cargar_semillas

def main():
    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ") == "0":
                return
            continue
        opcion = menu_privado(usuario_actual)
        usuario_actual = None # Terminar el acceso de esta sesión.
        if opcion == "0":
            return
        print("Sesión cerrada. Ingrese nuevamente.")


if __name__ == "__main__":
    crear_base_y_tablas()
    cargar_semillas()
    main()
    menu_principal()
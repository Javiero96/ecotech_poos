from servicios.gestion_empleados import listar_todos_los_empleados
from menus.menu import menu_admin

def menu_principal(usuario_actual: dict):
    while True:
        print(f"\n--- MENÚ PRINCIPAL (Rol: {usuario_actual['rol'].upper()}) ---")
        print("1. Mi ficha")
        print("2. Mis registros de tiempo")
        print("3. Consultar API Dólar")
        
        # Solo mostrar opciones extra si es admin
        if usuario_actual["rol"] == "admin":
            print("4. Administrar empleados (Solo Admin)")
            
        print("9. Cerrar sesión")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            print(f"Mostrando ficha del empleado ID: {usuario_actual['empleado_id']}")
            # Llamarías a la función de ver ficha
            
        elif opcion == "4":
            if usuario_actual["rol"] == "admin":
                try:
                    menu_admin()
                except PermissionError as error:
                    print(f"\n[!] ACCESO DENEGADO: {error}")
            else:
                print("Opción inválida.")
                
        elif opcion == "9":
            print("Cerrando sesión...")
            break
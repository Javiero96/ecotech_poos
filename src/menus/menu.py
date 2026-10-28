import os
import pymysql
from datetime import datetime
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.registroTiempo import RegistroTiempo

from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresione Enter para continuar...")


def menu_departamentos():
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE DEPARTAMENTOS ===")
        print("1. Crear Departamento")
        print("2. Listar Departamentos")
        print("3. Actualizar datos (nombre, descripción)")
        print("4. Asignar Gerente")
        print("5. Volver")
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre: ")
                descripcion = input("Descripción: ")
                d = Departamento(nombre=nombre, descripcion=descripcion)
                d.validar()
                DepartamentoDAO.insertar(d)
                print("\n[✓] Departamento creado exitosamente.")
                pausar()

            elif opcion == "2":
                print("\n--- LISTA DE DEPARTAMENTOS ---")
                deptos = DepartamentoDAO.listar()
                if not deptos:
                    print("No hay departamentos registrados.")
                else:
                    for d in deptos:
                        print(d)
                pausar()

            elif opcion == "3":
                id_d = int(input("ID Departamento a actualizar: "))
                nombre = input("Nuevo nombre: ")
                descripcion = input("Nueva descripción: ")
                
                dep_temp = Departamento(nombre=nombre, descripcion=descripcion)
                dep_temp.validar()

                if DepartamentoDAO.actualizar_datos(id_d, nombre, descripcion):
                    print("\n[✓] Departamento actualizado.")
                else:
                    print("\n[!] No se encontró el departamento con ese ID.")
                pausar()

            elif opcion == "4":
                id_d = int(input("ID Departamento: "))
                id_g = int(input("ID Empleado Gerente: "))

                # Validar primero si el empleado existe en MySQL
                if not EmpleadoDAO.buscar_por_id(id_g):
                    print(f"\n[!] El empleado con ID {id_g} no existe.")
                else:
                    if DepartamentoDAO.asignar_gerente(id_d, id_g):
                        print("\n[✓] Gerente asignado exitosamente.")
                    else:
                        print("\n[!] No se encontró el departamento indicado.")
                pausar()

            elif opcion == "5":
                break

        except ValueError as e:
            print(f"\n[Error de validación o entrada]: {e}")
            pausar()
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1452:
                print("\n[Error de BD]: El ID indicado no existe en la base de datos.")
            else:
                print(f"\n[Error de BD]: {e}")
            pausar()
        except Exception as e:
            print(f"\n[Error inesperado]: {e}")
            pausar()


def menu_empleados():
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE EMPLEADOS ===")
        print("1. Crear Empleado")
        print("2. Listar Empleados")
        print("3. Actualizar datos (nombre, correo)")
        print("4. Cambiar Departamento")
        print("5. Volver")
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre: ")
                correo = input("Correo: ")
                e = Empleado(nombre=nombre, correo=correo)
                e.validar()
                EmpleadoDAO.insertar(e)
                print("\n[✓] Empleado registrado exitosamente.")
                pausar()

            elif opcion == "2":
                print("\n--- LISTA DE EMPLEADOS ---")
                empleados = EmpleadoDAO.listar()
                if not empleados:
                    print("No hay empleados registrados.")
                else:
                    for e in empleados:
                        print(e)
                pausar()

            elif opcion == "3":
                id_e = int(input("ID Empleado a actualizar: "))
                nombre = input("Nuevo nombre: ")
                correo = input("Nuevo correo: ")
                
                emp_temp = Empleado(nombre=nombre, correo=correo)
                emp_temp.validar()

                if EmpleadoDAO.actualizar_datos(id_e, nombre, correo):
                    print("\n[✓] Empleado actualizado.")
                else:
                    print("\n[!] Empleado no encontrado.")
                pausar()

            elif opcion == "4":
                id_e = int(input("ID Empleado: "))
                id_dep = int(input("ID Nuevo Departamento: "))

                # Validar primero si el departamento existe
                if not DepartamentoDAO.buscar_por_id(id_dep):
                    print(f"\n[!] El departamento con ID {id_dep} no existe.")
                else:
                    if EmpleadoDAO.cambiar_departamento(id_e, id_dep):
                        print("\n[✓] Departamento asignado al empleado.")
                    else:
                        print("\n[!] No se encontró el empleado indicado.")
                pausar()

            elif opcion == "5":
                break

        except ValueError as e:
            print(f"\n[Error de validación o entrada]: {e}")
            pausar()
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:
                print("\n[Error de BD]: El correo electrónico ya está registrado.")
            elif e.args[0] == 1452:
                print("\n[Error de BD]: El ID del departamento no existe.")
            else:
                print(f"\n[Error de BD]: {e}")
            pausar()
        except Exception as e:
            print(f"\n[Error inesperado]: {e}")
            pausar()


while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE PROYECTOS ===")
        print("1. Crear Proyecto")
        print("2. Listar Proyectos")
        print("3. Actualizar datos (nombre, descripción)")
        print("4. Actualizar fechas (inicio, fin)")
        print("5. Cambiar estado")
        print("6. Volver")
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre: ")
                descripcion = input("Descripción: ")
                f_str = input("Fecha inicio (YYYY-MM-DD): ")
                f_inicio = datetime.strptime(f_str, "%Y-%m-%d").date()
                p = Proyecto(nombre=nombre, descripcion=descripcion, fecha_inicio=f_inicio)
                p.validar()
                ProyectoDAO.insertar(p)
                print("\n[✓] Proyecto creado exitosamente.")
                pausar()

            elif opcion == "2":
                print("\n--- LISTA DE PROYECTOS ---")
                proyectos = ProyectoDAO.listar()
                if not proyectos:
                    print("No hay proyectos registrados.")
                else:
                    for p in proyectos:
                        print(p)
                pausar()

            elif opcion == "3":
                id_p = int(input("ID Proyecto: "))
                nombre = input("Nuevo nombre: ")
                descripcion = input("Nueva descripción: ")

                # Buscar primero para mantener la fecha original en el objeto de validación
                proy_actual = ProyectoDAO.buscar_por_id(id_p)
                if not proy_actual:
                    print("\n[!] Proyecto no encontrado.")
                else:
                    proy_actual.actualizar_datos(nombre, descripcion)
                    if ProyectoDAO.actualizar_datos(id_p, nombre, descripcion):
                        print("\n[✓] Proyecto actualizado.")
                pausar()

            elif opcion == "4":
                id_p = int(input("ID Proyecto: "))
                f_ini_str = input("Nueva fecha inicio (YYYY-MM-DD): ")
                f_fin_str = input("Nueva fecha fin (YYYY-MM-DD): ")
                f_inicio = datetime.strptime(f_ini_str, "%Y-%m-%d").date()
                f_fin = datetime.strptime(f_fin_str, "%Y-%m-%d").date()

                if f_fin < f_inicio:
                    raise ValueError("La fecha fin no puede ser anterior a la fecha de inicio.")

                if ProyectoDAO.actualizar_fechas(id_p, f_inicio, f_fin):
                    print("\n[✓] Fechas actualizadas.")
                else:
                    print("\n[!] Error al actualizar fechas.")
                pausar()

            elif opcion == "5":
                id_p = int(input("ID Proyecto: "))
                nuevo_estado = input("Nuevo estado (pendiente/en proceso/finalizado): ")
                if ProyectoDAO.cambiar_estado(id_p, nuevo_estado):
                    print("\n[✓] Estado modificado.")
                else:
                    print("\n[!] Error al cambiar estado.")
                pausar()

            elif opcion == "6":
                break

        except ValueError as e:
            print(f"\n[Error de validación o entrada]: {e}")
            pausar()
        except pymysql.err.IntegrityError as e:
            print(f"\n[Error de BD]: {e}")
            pausar()
        except Exception as e:
            print(f"\n[Error inesperado]: {e}")
            pausar()


def menu_registro_tiempo():
    while True:
        limpiar_pantalla()
        print("=== REGISTRO DE TIEMPO ===")
        print("1. Registrar Horas")
        print("2. Listar Registros")
        print("3. Actualizar detalle (fecha, horas, descripción)")
        print("4. Volver")
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                id_e = int(input("ID Empleado: "))
                id_p = int(input("ID Proyecto: "))
                f_str = input("Fecha (YYYY-MM-DD): ")
                fecha = datetime.strptime(f_str, "%Y-%m-%d").date()
                horas = float(input("Horas trabajadas: "))
                desc = input("Descripción del trabajo: ")

                emp = EmpleadoDAO.buscar_por_id(id_e)
                proy = ProyectoDAO.buscar_por_id(id_p)

                if not emp:
                    print(f"\n[!] El empleado con ID {id_e} no existe.")
                elif not proy:
                    print(f"\n[!] El proyecto con ID {id_p} no existe.")
                else:
                    reg = RegistroTiempo(
                        empleado=emp,
                        proyecto=proy,
                        fecha=fecha,
                        horas=horas,
                        descripcion=desc,
                    )
                    reg.validar()
                    RegistroTiempoDAO.insertar(reg)
                    print("\n[✓] Tiempo registrado correctamente.")
                pausar()

            elif opcion == "2":
                print("\n--- LISTA DE REGISTROS DE TIEMPO ---")
                registros = RegistroTiempoDAO.listar()
                if not registros:
                    print("No hay registros de tiempo.")
                else:
                    for r in registros:
                        print(r)
                pausar()

            elif opcion == "3":
                id_r = int(input("ID Registro: "))
                f_str = input("Nueva fecha (YYYY-MM-DD): ")
                fecha = datetime.strptime(f_str, "%Y-%m-%d").date()
                horas = float(input("Horas trabajadas: "))
                desc = input("Nueva descripción: ")

                if horas <= 0 or horas > 24:
                    raise ValueError("Las horas deben estar entre 0 y 24.")
                if desc and len(desc) > 500:
                    raise ValueError("La descripción no puede superar los 500 caracteres.")

                if RegistroTiempoDAO.actualizar_detalle(id_r, fecha, horas, desc):
                    print("\n[✓] Registro de tiempo actualizado.")
                else:
                    print("\n[!] Registro no encontrado.")
                pausar()

            elif opcion == "4":
                break

        except ValueError as e:
            print(f"\n[Error de validación o entrada]: {e}")
            pausar()
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1452:
                print("\n[Error de BD]: El empleado o el proyecto indicado no existen.")
            else:
                print(f"\n[Error de BD]: {e}")
            pausar()
        except Exception as e:
            print(f"\n[Error inesperado]: {e}")
            pausar()


def menu_principal():
    

    while True:
        limpiar_pantalla()
        print("==================================")
        print("    SISTEMA DE ECOTECH     ")
        print("==================================")
        print("1. Gestión de Departamentos")
        print("2. Gestión de Empleados")
        print("3. Gestión de Proyectos")
        print("4. Gestión de Registro de Tiempo")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_departamentos()
        elif opcion == "2":
            menu_empleados()
        elif opcion == "3":
            menu_proyectos()
        elif opcion == "4":
            menu_registro_tiempo()
        elif opcion == "5":
            limpiar_pantalla()
            print("¡Hasta luego!")
            break
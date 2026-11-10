from datetime import date
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.registroTiempo import RegistroTiempo
from dominio.usuario import Usuario
import bcrypt

# Importamos las CLASES directamente
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.usuario_dao import UsuarioDAO

def cargar_semillas():
    print("=== INICIANDO CARGA DE SEMILLAS ===\n")

    # ==========================================
    # 1. SEMILLA DE DEPARTAMENTOS
    # ==========================================
    datos_deptos = [
        ("Dirección General", "Administración principal de la empresa"),
        ("Tecnología", "Desarrollo de software y soporte TI"),
        ("Recursos Humanos", "Gestión de personal y talento")
    ]
    
    depto_tecnologia = None

    for nombre, descripcion in datos_deptos:
        existente = DepartamentoDAO.buscar_por_nombre(nombre)
        if existente is not None:
            print(f"Ya existe Departamento: {nombre}")
            if nombre == "Tecnología":
                depto_tecnologia = existente
            continue
        
        depto = Departamento(nombre, descripcion)
        # Asumiendo que depto.validar() existe en tu modelo
        # depto.validar() 
        DepartamentoDAO.insertar(depto)
        print(f"Creado Departamento: {nombre}")
        
        if nombre == "Tecnología":
            depto_tecnologia = depto

    print("-" * 40)

    # ==========================================
    # 2. SEMILLA DE EMPLEADOS
    # ==========================================
    datos_empleados = [
        ("Admin Sistema", "admin@ecotech.example"), 
        ("Ana Torres", "ana@ecotech.example"),
        ("Carlos Silva", "carlos@ecotech.example")
    ]
    
    empleado_admin = None
    empleado_ana = None
    empleado_carlos = None

    for nombre, correo in datos_empleados:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe Empleado: {correo}")
            if correo == "admin@ecotech.example":
                empleado_admin = existente
            elif correo == "ana@ecotech.example":
                empleado_ana = existente
            elif correo == "carlos@ecotech.example":
                empleado_carlos = existente
            continue
        
        empleado = Empleado(nombre, correo, depto_tecnologia)
        # empleado.validar()
        EmpleadoDAO.insertar(empleado)
        print(f"Creado Empleado: {correo}")

        if correo == "admin@ecotech.example":
            empleado_admin = empleado
        elif correo == "ana@ecotech.example":
            empleado_ana = empleado
        elif correo == "carlos@ecotech.example":
            empleado_carlos = empleado

    print("-" * 40)

    # ==========================================
    # 3. SEMILLA DE USUARIOS (Admin y Empleados)
    # ==========================================
    # Para cumplir con el requerimiento de tener admin y 2 cuentas habituales
    datos_usuarios = [
        ("admin", "admin123", empleado_admin, "admin"),
        ("ana_torres", "empleado123", empleado_ana, "empleado"),
        ("carlos_silva", "empleado123", empleado_carlos, "empleado")
    ]
    for nombre_usr, clave_usr, emp_obj, rol_usr in datos_usuarios:
        if emp_obj is None:
            print(f"[!] No se pudo crear el usuario {nombre_usr} porque falta el empleado.")
            continue
            
        existente_user = UsuarioDAO.buscar_por_nombre(nombre_usr)
        if existente_user is not None:
            print(f"Ya existe Usuario: {nombre_usr}")
        else:
            hash_clave = bcrypt.hashpw(clave_usr.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Instanciamos la clase Usuario con el rol explícito
            usuario_nuevo = Usuario(
                nombre_usuario=nombre_usr,
                password_hash=hash_clave,
                empleado_id=emp_obj.id, # o emp_obj.id_empleado según como lo tengas
                rol=rol_usr
            )
            UsuarioDAO.insertar(usuario_nuevo)
            print(f"Creado Usuario: {nombre_usr} (Rol: {rol_usr})")

    print("-" * 40)

    # ==========================================
    # 4. SEMILLA DE PROYECTOS
    # ==========================================
    datos_proyectos = [
        ("Migración Cloud", "Paso de servidores físicos a AWS", date(2026, 1, 15)),
        ("Portal Web v2", "Actualización de la intranet corporativa", date(2026, 3, 10))
    ]

    proyecto_demo = None

    for nombre, descripcion, fecha_inicio in datos_proyectos:
        existente = ProyectoDAO.buscar_por_nombre(nombre)
        if existente is not None:
            print(f"Ya existe Proyecto: {nombre}")
            if nombre == "Migración Cloud":
                proyecto_demo = existente
            continue
        
        proyecto = Proyecto(nombre, descripcion, fecha_inicio)
        # proyecto.validar()
        ProyectoDAO.insertar(proyecto)
        print(f"Creado Proyecto: {nombre}")

        if nombre == "Migración Cloud":
            proyecto_demo = proyecto

    print("-" * 40)

    # ==========================================
    # 5. SEMILLA DE REGISTRO DE TIEMPO
    # ==========================================
    if empleado_ana and proyecto_demo:
        datos_registros = [
            (date(2026, 4, 1), 4.5, "Análisis de requerimientos iniciales"),
            (date(2026, 4, 2), 6.0, "Configuración de entorno de pruebas")
        ]

        registros_bd = RegistroTiempoDAO.listar()
        
        for fecha, horas, desc in datos_registros:
            # Buscamos manualmente si ya existe (asumiendo que empleado_ana tiene .id)
            ya_existe = any(
                r.empleado.id == empleado_ana.id and 
                r.proyecto.id == proyecto_demo.id and 
                r.fecha == fecha 
                for r in registros_bd
            )

            if ya_existe:
                print(f"Ya existe Registro de Tiempo para la fecha: {fecha}")
                continue

            registro = RegistroTiempo(
                empleado=empleado_ana,
                proyecto=proyecto_demo,
                fecha=fecha,
                horas=horas,
                descripcion=desc
            )
            # registro.validar()
            RegistroTiempoDAO.insertar(registro)
            print(f"Creado Registro de Tiempo para Ana: {fecha} ({horas} hrs)")

    print("\n=== SEMILLAS CARGADAS CON ÉXITO ===")

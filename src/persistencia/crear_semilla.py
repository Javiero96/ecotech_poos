from datetime import date
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.registroTiempo import RegistroTiempo
from dominio.usuario import Usuario
from servicios.autenticacion import registrar_usuario
import bcrypt

# Importamos las CLASES directamente
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.usuario_dao import UsuarioDAO
# Asumiendo que guardaste el UsuarioDAO en el mismo archivo de daos.py
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
    
    # Guardaremos una referencia para usarla en los empleados
    depto_tecnologia = None

    for nombre, descripcion in datos_deptos:
        existente = DepartamentoDAO.buscar_por_nombre(nombre)
        if existente is not None:
            print(f"Ya existe Departamento: {nombre}")
            if nombre == "Tecnología":
                depto_tecnologia = existente
            continue
        
        depto = Departamento(nombre, descripcion)
        depto.validar()
        DepartamentoDAO.insertar(depto)
        print(f"Creado Departamento: {nombre}")
        
        if nombre == "Tecnología":
            depto_tecnologia = depto

    print("-" * 40)

    # ==========================================
    # 2. SEMILLA DE EMPLEADOS
    # ==========================================
    datos_empleados = [
        ("Admin Sistema", "admin@ecotech.example"), # Empleado para el usuario admin
        ("Ana Torres", "ana@ecotech.example"),
        ("Carlos Silva", "carlos@ecotech.example")
    ]
    
    # Guardaremos referencias para el usuario admin y los registros de tiempo
    empleado_admin = None
    empleado_demo = None

    for nombre, correo in datos_empleados:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe Empleado: {correo}")
            if correo == "admin@ecotech.example":
                empleado_admin = existente
            elif correo == "ana@ecotech.example":
                empleado_demo = existente
            continue
        
        # Le asignamos a todos el departamento_tecnologia por defecto en esta semilla
        empleado = Empleado(nombre, correo, depto_tecnologia)
        empleado.validar()
        EmpleadoDAO.insertar(empleado)
        print(f"Creado Empleado: {correo}")

        if correo == "admin@ecotech.example":
            empleado_admin = empleado
        elif correo == "ana@ecotech.example":
            empleado_demo = empleado

    print("-" * 40)

    # ==========================================
    # 3. SEMILLA DE USUARIO ADMIN
    # ==========================================
    # Para el usuario admin no usamos un for masivo, sino una semilla puntual
    nombre_admin = "admin"
    
    # OPCIÓN A: Si tienes una función para encriptar
    # hash_clave_admin = generar_hash("admin123") 
    
    # OPCIÓN B: Usar directamente bcrypt si es lo que pide el profe
    hash_clave_admin = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    existente_user = UsuarioDAO.buscar_por_nombre(nombre_admin)
    if existente_user is not None:
        print(f"Ya existe Usuario: {nombre_admin}")
    else:
        if empleado_admin:
            # Creamos el usuario vinculándolo al ID del empleado "Admin Sistema"
            usuario_admin = Usuario(
                nombre_usuario=nombre_admin,
                password_hash=hash_clave_admin,
                empleado_id=empleado_admin.id
            )
            UsuarioDAO.insertar(usuario_admin)
            print(f"Creado Usuario: {nombre_admin}")
        else:
            print("[!] No se pudo crear el usuario admin porque falta el empleado.")

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
        proyecto.validar()
        ProyectoDAO.insertar(proyecto)
        print(f"Creado Proyecto: {nombre}")

        if nombre == "Migración Cloud":
            proyecto_demo = proyecto

    print("-" * 40)

    # ==========================================
    # 5. SEMILLA DE REGISTRO DE TIEMPO
    # ==========================================
    # Usamos referencias a los objetos ya recuperados arriba (empleado_demo y proyecto_demo)
    if empleado_demo and proyecto_demo:
        datos_registros = [
            (date(2026, 4, 1), 4.5, "Análisis de requerimientos iniciales"),
            (date(2026, 4, 2), 6.0, "Configuración de entorno de pruebas")
        ]

        # Para evitar registros duplicados, consultamos los de la base de datos
        registros_bd = RegistroTiempoDAO.listar()
        
        for fecha, horas, desc in datos_registros:
            # Buscamos manualmente si ya existe este registro en la lista devuelta por la BD
            ya_existe = any(
                r.empleado.id == empleado_demo.id and 
                r.proyecto.id == proyecto_demo.id and 
                r.fecha == fecha 
                for r in registros_bd
            )

            if ya_existe:
                print(f"Ya existe Registro de Tiempo para la fecha: {fecha}")
                continue

            registro = RegistroTiempo(
                empleado=empleado_demo,
                proyecto=proyecto_demo,
                fecha=fecha,
                horas=horas,
                descripcion=desc
            )
            registro.validar()
            RegistroTiempoDAO.insertar(registro)
            print(f"Creado Registro de Tiempo: {fecha} ({horas} hrs)")

    print("\n=== SEMILLAS CARGADAS CON ÉXITO ===")
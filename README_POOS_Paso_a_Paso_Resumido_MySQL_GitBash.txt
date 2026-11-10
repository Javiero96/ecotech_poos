README - GUÍA RÁPIDA POOS
===========================

OBJETIVO
Implementar el UML en Python, aplicar POO, conectar MySQL, realizar CRUD,
manejar errores, validar datos y poder explicar el uso de IA.

INICIO EN GIT BASH
------------------

mkdir proyecto-poos
cd proyecto-poos
python -m venv venv
source venv/Scripts/activate
pip install mysql-connector-python
pip freeze > requirements.txt
touch main.py conexion.py modelos.py crud.py

1. Descripción General del Proyecto
EcoTech es una solución de software orientada a la gestión empresarial modular y segura, desarrollada en Python. El sistema integra persistencia dual (compatible con MySQL y SQLite), un módulo de consumo y deserialización de la API de indicadores económicos, un sistema estricto de control de accesos basado en roles (admin y empleado), y trazabilidad de perfiles y horas de trabajo.

2. Arquitectura y Decisiones de Ingeniería
La arquitectura del software se rige bajo los principios de separación de responsabilidades (SoC) y diseño modular por capas:

Capa de Dominio (/dominio): Modelos de negocio puros (Usuario, Empleado, Proyecto, RegistroTiempo). Implementa validaciones estrictas en tiempo de construcción (ej. normalización de nombres de usuario y validación de roles permitidos).

Capa de Persistencia / DAOs (/persistencia): Abstracción del acceso a datos mediante una factoría unificada (conexion.py) y marcadores dinámicos (marcador_sql()), garantizando portabilidad entre motores relacionales.

Capa de Servicios y Seguridad (/servicios): Lógica de negocio y control de permisos (permisos.py), implementando interceptores de sesión (exigir_sesion, exigir_admin) para blindar operaciones críticas.

Capa de Presentación (/menus): Interfaces de terminal desacopladas y dinámicas que adaptan sus opciones de navegación en tiempo de ejecución según el rol del usuario autenticado (usuario_actual).

3. Análisis de Riesgos de Seguridad y Problemas Arquitectónicos
Durante el ciclo de desarrollo iterativo, se identificaron y resolvieron diversos desafíos críticos de ingeniería:

Elevación de Privilegios por Dependencia Visual en la Interfaz:

Riesgo: Limitar la seguridad únicamente a ocultar opciones en los menús de consola.

Mitigación: Se implementó una doble validación defensiva. Las capas de servicio interceptan y rechazan cualquier ejecución si el diccionario de sesión carece de los privilegios requeridos (PermissionError).

Seguridad en el Manejo de Credenciales:

Riesgo: Exposición o almacenamiento plano de contraseñas.

Mitigación: Uso obligatorio de hashes seguros mediante bcrypt con salts dinámicos en la autenticación y registro de usuarios.

Bloqueos de Concurrencia (database is locked en SQLite):

Riesgo: Bloqueos del archivo de base de datos local debido a cursores o conexiones huérfanas abiertas.

Mitigación: Refactorización sistemática de los DAOs utilizando bloques try-except-finally para asegurar el cierre explícito de cursores y conexiones tras cada operación.

Integridad Referencial y Mapeo de Roles:

Riesgo: Pérdida de atributos de control (como el rol) al omitir columnas en las consultas multitabla (SELECT y JOIN).

Mitigación: Sincronización estricta de las sentencias SQL en el UsuarioDAO para garantizar un mapeo bidireccional íntegro.

4. Metodología y Trazabilidad del Uso de Inteligencia Artificial
Siguiendo criterios rigurosos de ingeniería de software, se mantuvo un registro transparente de la colaboración con asistentes de inteligencia artificial para el diseño, depuración y refactorización del código base:

Evidencia de Interacción:

Fase de Diagnóstico: Se utilizaron consultas interactivas para analizar trazas de error en consola (ej. sqlite3.IntegrityError, TypeError: 'module' object is not callable y bloqueos de concurrencia).

Fase de Refactorización: Se plantearon prompts específicos orientados a la separación de menús por roles, optimización de DAOs de persistencia dual y parametrización de funciones de autenticación.

Criterios de Validación Técnica:

Ningún fragmento de código sugerido por la IA fue integrado sin una revisión previa de su compatibilidad tipada, manejo de excepciones y conformidad con el modelo de dominio establecido.

Las decisiones de diseño (como la inyección del diccionario usuario_actual y los interceptores de permisos) fueron sustentadas mediante principios de inversión de dependencias y defensa en profundidad.
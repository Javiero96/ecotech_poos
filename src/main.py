from dominio.empleado import Empleado # type: ignore

empleado = Empleado(
    nombre = "Ana Torres",
    correo = "ana.torres@ecotech.cl"
)

print(empleado.mostrar_datos())

from dominio.departamento import Departamento # type: ignore

departamento = Departamento(
    nombre = "Recursos Humanos"
)

print(departamento.mostrar_datos())
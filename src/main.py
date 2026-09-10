from dominio.empleado import Empleado # type: ignore

empleado = Empleado(
    nombre = "Ana Torres",
    correo = "ana.torres@ecotech.cl"
)

print(empleado.mostrar_datos())

from dominio.departamento import Departamento # type: ignore

desarrollo = Departamento("Dep desarrollo")

print(desarrollo.mostrar_datos())

desarrollo.agregar_empleado(empleado)

# print(desarrollo.cantidad_empleados())
#for empleado in desarrollo.empleados:
    #print(empleado.mostrar_datos())

from dominio.proyecto import Proyecto 

titulo = Proyecto("Nuevo edificio")
print(titulo.mostrar_datos())


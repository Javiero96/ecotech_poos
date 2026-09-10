from dominio.empleado import Empleado

class Departamento:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._empleados: list[Empleado] = []
    
    def agregar_empleado(self,empleado: Empleado) -> bool:
        if empleado in self._empleados:
            return False

        self._empleados.append(empleado)
    
    def mostrar_datos(self) -> str:
        return f"{self.nombre}"
    





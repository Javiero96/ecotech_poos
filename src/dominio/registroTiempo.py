from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from datetime import date
from typing import Optional

class RegistroTiempo:
    def __init__(
        self,
        empleado: Empleado,
        proyecto: Proyecto,
        fecha: date,
        horas: float,
        descripcion: str,
        id: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.empleado: Empleado = empleado
        self.proyecto: Proyecto = proyecto
        self.fecha: date = fecha
        self.horas: float = horas
        self.descripcion: str = descripcion

    def validar(self) -> None:
        """Valida los límites de registro de tiempo."""
        if self.horas <= 0:
            raise ValueError("Las horas trabajadas deben ser mayores a cero.")
        if self.horas > 24:
            raise ValueError("Las horas trabajadas en un solo registro no pueden superar las 24 horas.")

    def actualizar_detalle(self, fecha: date, horas: float, descripcion: str) -> None:
        """Actualiza la fecha, horas y descripción del registro."""
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion
        self.validar()

    def __str__(self) -> str:
        return f"RegistroTiempo(id={self.id}, empleado='{self.empleado.nombre}', proyecto='{self.proyecto.nombre}', horas={self.horas})"
from dominio.empleado import Empleado
from datetime import date
from typing import Optional

from datetime import date
from typing import Optional


class Proyecto:
    """Clase de dominio para representar un Proyecto."""

    def __init__(
        self,
        nombre: str,
        descripcion: str,
        fecha_inicio: date,
        fecha_fin: Optional[date] = None,
        estado: str = "pendiente",
        id: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.nombre: str = nombre
        self.descripcion: str = descripcion
        self.fecha_inicio: date = fecha_inicio
        self.fecha_fin: Optional[date] = fecha_fin
        self.estado: str = estado

    def validar(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío.")
        if len(self.nombre) > 100:
            raise ValueError("El nombre del proyecto no puede superar los 100 caracteres.")
        if self.descripcion and len(self.descripcion) > 500:
            raise ValueError("La descripción del proyecto no puede superar los 500 caracteres.")
        if len(self.estado) > 50:
            raise ValueError("El estado no puede superar los 50 caracteres.")
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio.")

    def actualizar_datos(self, nombre: str, descripcion: str) -> None:
        self.nombre = nombre
        self.descripcion = descripcion
        self.validar()

    def actualizar_fechas(self, fecha_inicio: date, fecha_fin: date) -> None:
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.validar()

    def cambiar_estado(self, estado: str) -> None:
        self.estado = estado
        self.validar()

    def __str__(self) -> str:
        return f"Proyecto(id={self.id}, nombre='{self.nombre}', estado='{self.estado}', fecha_inicio={self.fecha_inicio})"
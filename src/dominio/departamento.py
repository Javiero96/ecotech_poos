from dominio.empleado import Empleado
from typing import Optional

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from dominio.empleado import Empleado


class Departamento:
    """Clase de dominio para representar un Departamento."""

    def __init__(
        self,
        nombre: str,
        descripcion: str,
        gerente: Optional['Empleado'] = None,
        id: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.nombre: str = nombre
        self.descripcion: str = descripcion
        self.gerente: Optional['Empleado'] = gerente

    def validar(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del departamento no puede estar vacío.")
        if len(self.nombre) > 100:
            raise ValueError("El nombre del departamento no puede superar los 100 caracteres.")
        if self.descripcion and len(self.descripcion) > 500:
            raise ValueError("La descripción del departamento no puede superar los 500 caracteres.")

    def actualizar_datos(self, nombre: str, descripcion: str) -> None:
        self.nombre = nombre
        self.descripcion = descripcion
        self.validar()

    def asignar_gerente(self, gerente: 'Empleado') -> None:
        self.gerente = gerente

    def __str__(self) -> str:
        gerente_info = self.gerente.nombre if self.gerente else "Sin gerente"
        return f"Departamento(id={self.id}, nombre='{self.nombre}', gerente='{gerente_info}')"
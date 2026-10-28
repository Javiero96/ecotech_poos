from typing import TYPE_CHECKING, Optional

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from dominio.departamento import Departamento


class Empleado:
    """Clase de dominio para representar un Empleado."""

    def __init__(
        self,
        nombre: str,
        correo: str,
        departamento: Optional['Departamento'] = None,
        id: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.nombre: str = nombre
        self.correo: str = correo
        self.departamento: Optional['Departamento'] = departamento

    def validar(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del empleado no puede estar vacío.")
        if len(self.nombre) > 100:
            raise ValueError("El nombre del empleado no puede superar los 100 caracteres.")
        if not self.correo or "@" not in self.correo:
            raise ValueError("Debe proporcionar un correo electrónico válido.")
        if len(self.correo) > 150:
            raise ValueError("El correo no puede superar los 150 caracteres.")

    def actualizar_datos(self, nombre: str, correo: str) -> None:
        self.nombre = nombre
        self.correo = correo
        self.validar()

    def cambiar_departamento(self, departamento: 'Departamento') -> None:
        self.departamento = departamento

    def __str__(self) -> str:
        depto_info = self.departamento.nombre if self.departamento else "Sin departamento"
        return f"Empleado(id={self.id}, nombre='{self.nombre}', correo='{self.correo}', departamento='{depto_info}')"
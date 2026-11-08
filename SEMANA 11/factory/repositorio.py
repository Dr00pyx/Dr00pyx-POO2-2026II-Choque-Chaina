"""
Producto Abstracto: Interfaz de Repositorio de Estudiantes
Define el contrato para persistencia desacoplada.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .modelo import Estudiante


class RepositorioEstudiantes(ABC):
    """Interfaz abstracta que define las operaciones de persistencia del estudiante."""

    @abstractmethod
    def guardar(self, estudiante: Estudiante) -> bool:
        """Inserta o actualiza un estudiante en el almacenamiento."""
        pass

    @abstractmethod
    def buscar_por_codigo(self, codigo: str) -> Optional[Estudiante]:
        """Obtiene un estudiante según su código único."""
        pass

    @abstractmethod
    def listar_todos(self) -> List[Estudiante]:
        """Devuelve todos los estudiantes registrados."""
        pass

    @abstractmethod
    def eliminar(self, codigo: str) -> bool:
        """Elimina un estudiante según su código."""
        pass

    @property
    @abstractmethod
    def tipo_almacenamiento(self) -> str:
        """Nombre descriptivo del medio de persistencia."""
        pass

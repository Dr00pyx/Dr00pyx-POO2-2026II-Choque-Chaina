"""
Módulo de Repositorios para la persistencia de Estudiantes.
Define la abstracción IRepositorioEstudiante (DIP) y la implementación RepositorioMemoria.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Protocol
from estudiante import Estudiante


class IRepositorioEstudiante(Protocol):
    """Interfaz estructural para la persistencia de estudiantes."""
    def guardar(self, e: Estudiante) -> None:
        ...

    def buscar(self, cod: int) -> Optional[Estudiante]:
        ...

    def listar(self) -> List[Estudiante]:
        ...


class RepositorioMemoria:
    """Implementación de repositorio basada en diccionario en memoria."""
    def __init__(self) -> None:
        self._almacen: Dict[int, Estudiante] = {}

    def guardar(self, e: Estudiante) -> None:
        self._almacen[e.codigo] = e

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._almacen.get(cod)

    def listar(self) -> List[Estudiante]:
        return list(self._almacen.values())

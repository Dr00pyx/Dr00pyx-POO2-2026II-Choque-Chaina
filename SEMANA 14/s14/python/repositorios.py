from __future__ import annotations
from typing import Dict, List, Optional, Protocol
from estudiante import Estudiante
from repositorio_json import RepositorioJSON


class IRepositorioEstudiante(Protocol):
    def guardar(self, e: Estudiante) -> None:
        ...

    def buscar(self, cod: int) -> Optional[Estudiante]:
        ...

    def listar(self) -> List[Estudiante]:
        ...

    def eliminar(self, cod: int) -> None:
        ...


class RepositorioMemoria:
    def __init__(self) -> None:
        self._almacen: Dict[int, Estudiante] = {}

    def guardar(self, e: Estudiante) -> None:
        self._almacen[e.codigo] = e

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._almacen.get(cod)

    def listar(self) -> List[Estudiante]:
        return list(self._almacen.values())

    def eliminar(self, cod: int) -> None:
        self._almacen.pop(cod, None)


__all__ = [
    "IRepositorioEstudiante",
    "RepositorioMemoria",
    "RepositorioJSON",
]

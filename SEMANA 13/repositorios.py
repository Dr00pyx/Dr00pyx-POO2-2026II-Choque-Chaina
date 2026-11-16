"""
Módulo de Repositorios para la persistencia desacoplada de Estudiantes.
Define la abstracción IRepositorioEstudiante (DIP) y centraliza las implementaciones
en memoria y persistentes (JSON, CSV, SQLite), además de un Mock para pruebas.
Semana 13 — Persistencia Multicapa
"""
from __future__ import annotations
from typing import Dict, List, Optional, Protocol
from estudiante import Estudiante

# Re-exportamos los repositorios especializados
from repositorio_json import RepositorioJSON
from repositorio_csv import RepositorioCSV
from repositorio_sqlite import RepositorioSQLite


class IRepositorioEstudiante(Protocol):
    """
    Interfaz estructural (Protocol) para la persistencia de estudiantes.
    Asegura que cualquier backend cumpla el contrato de persistencia.
    """
    def guardar(self, e: Estudiante) -> None:
        """Guarda o actualiza la entidad Estudiante."""
        ...

    def buscar(self, cod: int) -> Optional[Estudiante]:
        """Busca y retorna un estudiante por su código, o None si no existe."""
        ...

    def listar(self) -> List[Estudiante]:
        """Retorna la lista de todos los estudiantes almacenados."""
        ...

    def eliminar(self, cod: int) -> None:
        """Elimina un estudiante por su código."""
        ...


class RepositorioMemoria:
    """
    Implementación en memoria volátil basada en un diccionario Python.
    Utilizada comúnmente para pruebas unitarias de alta velocidad.
    """
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


class MockRepositorio:
    """
    ADICIONAL Actividad 3A:
    Repositorio espía/mock para verificar y auditar llamadas en pruebas de sustitución.
    Registra cuántas veces se invocó guardar(), buscar(), etc.
    """
    def __init__(self) -> None:
        self._almacen: Dict[int, Estudiante] = {}
        self.veces_guardar = 0
        self.veces_buscar = 0
        self.veces_listar = 0
        self.veces_eliminar = 0

    def guardar(self, e: Estudiante) -> None:
        self.veces_guardar += 1
        self._almacen[e.codigo] = e

    def buscar(self, cod: int) -> Optional[Estudiante]:
        self.veces_buscar += 1
        return self._almacen.get(cod)

    def listar(self) -> List[Estudiante]:
        self.veces_listar += 1
        return list(self._almacen.values())

    def eliminar(self, cod: int) -> None:
        self.veces_eliminar += 1
        self._almacen.pop(cod, None)


__all__ = [
    "IRepositorioEstudiante",
    "RepositorioMemoria",
    "RepositorioJSON",
    "RepositorioCSV",
    "RepositorioSQLite",
    "MockRepositorio",
]

"""
Producto Concreto 1: Repositorio en Memoria Volátil (Diccionario).
Ideal para entornos de pruebas unitarias o desarrollo ligero.
"""
from typing import Dict, List, Optional
from .modelo import Estudiante
from .repositorio import RepositorioEstudiantes


class RepositorioMemoria(RepositorioEstudiantes):
    def __init__(self) -> None:
        self._almacen: Dict[str, Estudiante] = {}

    def guardar(self, estudiante: Estudiante) -> bool:
        self._almacen[estudiante.codigo] = estudiante
        return True

    def buscar_por_codigo(self, codigo: str) -> Optional[Estudiante]:
        return self._almacen.get(codigo)

    def listar_todos(self) -> List[Estudiante]:
        return list(self._almacen.values())

    def eliminar(self, codigo: str) -> bool:
        if codigo in self._almacen:
            del self._almacen[codigo]
            return True
        return False

    @property
    def tipo_almacenamiento(self) -> str:
        return "Memoria RAM (Volátil)"

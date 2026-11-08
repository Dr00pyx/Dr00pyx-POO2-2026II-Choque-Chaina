# -*- coding: utf-8 -*-
"""
repositorio.py — Repositorio genérico con TypeVar y Generic en Python 3.12+
"""
from typing import TypeVar, Generic, Callable, Iterator, Any
from functools import reduce

T = TypeVar("T")    # Tipo de la entidad
ID = TypeVar("ID")  # Tipo del identificador

class Repositorio(Generic[T, ID]):
    """
    Repositorio genérico en memoria para cualquier par (Entidad, TipoID).
    Usa un diccionario interno dict[ID, T] para acceso O(1).
    """
    def __init__(self, fn_id: Callable[[T], ID]) -> None:
        """
        fn_id: Función o lambda que extrae el identificador ID de una entidad T.
        """
        self._fn_id: Callable[[T], ID] = fn_id
        self._datos: dict[ID, T] = {}

    # ── CRUD Básico ──────────────────────────────────────────────────────────
    def guardar(self, entidad: T) -> None:
        """Guarda o sobreescribe la entidad indexada por su ID."""
        self._datos[self._fn_id(entidad)] = entidad

    def buscar(self, id_: ID) -> T | None:
        """Retorna la entidad asociada al ID o None si no existe."""
        return self._datos.get(id_)

    def eliminar(self, id_: ID) -> bool:
        """Elimina la entidad por su ID. Retorna True si existía y fue eliminada."""
        return bool(self._datos.pop(id_, None))

    # ── Consultas ────────────────────────────────────────────────────────────
    def todos(self) -> list[T]:
        """Retorna una lista con copia de todas las entidades."""
        return list(self._datos.values())

    def filtrar(self, pred: Callable[[T], bool]) -> list[T]:
        """Retorna una lista con las entidades que satisfacen el predicado."""
        return [e for e in self._datos.values() if pred(e)]

    def ordenar(self, key: Callable[[T], Any], reverse: bool = False) -> list[T]:
        """Retorna una lista ordenada según la función clave dada."""
        return sorted(self._datos.values(), key=key, reverse=reverse)

    def acumular(self, inicial: Any, f: Callable[[Any, T], Any]) -> Any:
        """Reduce todas las entidades acumulando mediante la función f."""
        return reduce(f, self._datos.values(), inicial)

    # ── Protocolo Python (Dunder methods) ─────────────────────────────────────
    def __len__(self) -> int:
        """Permite usar len(repo)."""
        return len(self._datos)

    def __contains__(self, id_: ID) -> bool:
        """Permite usar `id_ in repo`."""
        return id_ in self._datos

    def __iter__(self) -> Iterator[T]:
        """Permite iterar directamente sobre las entidades: `for e in repo:`."""
        return iter(self._datos.values())

    # ── Métodos Adicionales Requeridos en Actividad 2 ─────────────────────────
    def contar(self, pred: Callable[[T], bool]) -> int:
        """Cuenta cuántos elementos satisfacen el predicado."""
        return sum(1 for e in self._datos.values() if pred(e))

    def existe(self, id_: ID) -> bool:
        """Verifica si existe una entidad con el identificador dado."""
        return id_ in self._datos

    def primero(self, pred: Callable[[T], bool]) -> T | None:
        """Retorna el primer elemento que satisface el predicado, o None si no hay ninguno."""
        return next((e for e in self._datos.values() if pred(e)), None)

    # ── Análisis y Estadísticas ──────────────────────────────────────────────
    def estadisticas(self, attr: str) -> dict[str, Any]:
        """Calcula min, max, promedio y conteo de un atributo numérico de las entidades."""
        valores = [getattr(e, attr) for e in self._datos.values()]
        if not valores:
            return {"min": None, "max": None, "promedio": None, "n": 0}
        return {
            "min": min(valores),
            "max": max(valores),
            "promedio": sum(valores) / len(valores),
            "n": len(valores)
        }

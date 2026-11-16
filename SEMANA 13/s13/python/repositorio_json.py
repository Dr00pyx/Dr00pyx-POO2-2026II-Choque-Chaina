"""
Implementación del Repositorio basado en JSON.
Cumple con la interfaz IRepositorioEstudiante y persiste los datos en un archivo JSON en disco.
Semana 13 — Persistencia Multicapa
"""
from __future__ import annotations
import json
import os
import pathlib
from dataclasses import asdict
from typing import Optional, List
from estudiante import Estudiante


def _resolver_ruta(ruta: str | pathlib.Path) -> pathlib.Path:
    """Asegura que el directorio contenedor exista y retorna la ruta como Path."""
    p = pathlib.Path(ruta)
    try:
        if not p.parent.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return p


class RepositorioJSON:
    """
    Repositorio de persistencia documental en formato JSON.
    Almacena los estudiantes serializados como una lista de objetos JSON.
    """
    def __init__(self, ruta: str) -> None:
        self._ruta = _resolver_ruta(ruta)
        self._datos: dict[int, Estudiante] = {}
        self._cargar()

    @property
    def ruta(self) -> pathlib.Path:
        return self._ruta

    def _cargar(self) -> None:
        """Carga los estudiantes desde el archivo JSON si existe en disco."""
        if not self._ruta.exists():
            return
        with self._ruta.open(encoding="utf-8") as f:
            try:
                items = json.load(f)
                for item in items:
                    e = Estudiante(**item)
                    self._datos[e.codigo] = e
            except json.JSONDecodeError:
                self._datos = {}

    def _persistir(self) -> None:
        """Escribe la colección de estudiantes en el archivo JSON formateado."""
        lista = [asdict(e) for e in self._datos.values()]
        with self._ruta.open("w", encoding="utf-8") as f:
            json.dump(lista, f, indent=2, ensure_ascii=False)

    def guardar(self, e: Estudiante) -> None:
        """Guarda o actualiza un estudiante y persiste el estado en disco."""
        self._datos[e.codigo] = e
        self._persistir()

    def buscar(self, cod: int) -> Optional[Estudiante]:
        """Busca un estudiante por su código numérico."""
        return self._datos.get(cod)

    def listar(self) -> List[Estudiante]:
        """Retorna la lista completa de estudiantes registrados."""
        return list(self._datos.values())

    def eliminar(self, cod: int) -> None:
        """
        ADICIONAL Actividad 1A:
        Elimina un estudiante por su código y actualiza inmediatamente el archivo en disco.
        """
        if cod in self._datos:
            self._datos.pop(cod, None)
            self._persistir()

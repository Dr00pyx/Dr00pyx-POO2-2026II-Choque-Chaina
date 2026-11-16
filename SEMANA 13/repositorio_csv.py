"""
Implementación del Repositorio basado en CSV.
Cumple con la interfaz IRepositorioEstudiante y persiste los datos en un archivo CSV tabular.
Semana 13 — Persistencia Multicapa
"""
from __future__ import annotations
import csv
import json
import os
import pathlib
from typing import Optional, List
from estudiante import Estudiante

CAMPOS = ["codigo", "nombre", "ppa", "notas"]


def _resolver_ruta(ruta: str | pathlib.Path) -> pathlib.Path:
    """Asegura que el directorio contenedor exista y retorna la ruta como Path."""
    p = pathlib.Path(ruta)
    try:
        if not p.parent.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return p


class RepositorioCSV:
    """
    Repositorio de persistencia tabular en formato CSV.
    Mapea campos atómicos y serializa la lista de notas como JSON embebido en la columna 'notas'.
    """
    def __init__(self, ruta: str) -> None:
        self._ruta = _resolver_ruta(ruta)
        self._datos: dict[int, Estudiante] = {}
        self._cargar()

    @property
    def ruta(self) -> pathlib.Path:
        return self._ruta

    def _cargar(self) -> None:
        """Carga los registros desde el archivo CSV si existe."""
        if not self._ruta.exists():
            return
        with self._ruta.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row or not row.get("codigo"):
                    continue
                e = Estudiante(
                    codigo=int(row["codigo"]),
                    nombre=row["nombre"],
                    ppa=float(row["ppa"]),
                    notas=json.loads(row["notas"])
                )
                self._datos[e.codigo] = e

    def _persistir(self) -> None:
        """Guarda todos los estudiantes en el archivo CSV sobrescribiendo con cabeceras."""
        with self._ruta.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CAMPOS)
            writer.writeheader()
            for e in self._datos.values():
                writer.writerow({
                    "codigo": e.codigo,
                    "nombre": e.nombre,
                    "ppa": e.ppa,
                    "notas": json.dumps(e.notas)
                })

    def guardar(self, e: Estudiante) -> None:
        """Guarda o actualiza un estudiante y persiste en disco."""
        self._datos[e.codigo] = e
        self._persistir()

    def buscar(self, cod: int) -> Optional[Estudiante]:
        """Busca un estudiante por su código."""
        return self._datos.get(cod)

    def listar(self) -> List[Estudiante]:
        """Lista todos los estudiantes cargados."""
        return list(self._datos.values())

    def eliminar(self, cod: int) -> None:
        """Elimina un estudiante y actualiza el archivo CSV."""
        if cod in self._datos:
            self._datos.pop(cod, None)
            self._persistir()

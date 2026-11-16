"""
Implementación del Repositorio basado en SQLite.
Cumple con la interfaz IRepositorioEstudiante y persiste los datos en una base de datos relacional SQLite.
Semana 13 — Persistencia Multicapa
"""
from __future__ import annotations
import json
import os
import pathlib
import sqlite3
from typing import Optional, List
from estudiante import Estudiante

CREATE_SQL = (
    "CREATE TABLE IF NOT EXISTS estudiante("
    " codigo INTEGER PRIMARY KEY,"
    " nombre TEXT NOT NULL,"
    " ppa REAL NOT NULL DEFAULT 0,"
    " notas TEXT NOT NULL DEFAULT '[]')"
)


def _resolver_ruta(ruta: str | pathlib.Path) -> str:
    """Asegura que el directorio contenedor exista y retorna la ruta como string."""
    p = pathlib.Path(ruta)
    try:
        if not p.parent.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return str(p)


class RepositorioSQLite:
    """
    Repositorio de persistencia relacional con motor SQLite embebido.
    Implementa el patrón Data Mapper básico y garantiza transaccionalidad ACID.
    """
    def __init__(self, ruta: str) -> None:
        self._ruta = _resolver_ruta(ruta)
        self._con = sqlite3.connect(self._ruta, check_same_thread=False)
        self._con.execute(CREATE_SQL)
        self._con.commit()

    @property
    def ruta(self) -> str:
        return self._ruta

    def guardar(self, e: Estudiante) -> None:
        """Inserta o actualiza un registro de estudiante en la tabla relacional."""
        self._con.execute(
            "INSERT OR REPLACE INTO estudiante VALUES(?,?,?,?)",
            (e.codigo, e.nombre, e.ppa, json.dumps(e.notas))
        )
        self._con.commit()

    def buscar(self, cod: int) -> Optional[Estudiante]:
        """Consulta un estudiante por su clave primaria (código)."""
        row = self._con.execute(
            "SELECT * FROM estudiante WHERE codigo=?", (cod,)
        ).fetchone()
        if row is None:
            return None
        return Estudiante(row[0], row[1], row[2], json.loads(row[3]))

    def listar(self) -> List[Estudiante]:
        """Obtiene y desempaca todos los registros de estudiantes."""
        rows = self._con.execute("SELECT * FROM estudiante").fetchall()
        return [Estudiante(r[0], r[1], r[2], json.loads(r[3])) for r in rows]

    def eliminar(self, cod: int) -> None:
        """Elimina un registro de estudiante por su código."""
        self._con.execute("DELETE FROM estudiante WHERE codigo=?", (cod,))
        self._con.commit()

    def cerrar(self) -> None:
        """Cierra la conexión activa con la base de datos."""
        self._con.close()

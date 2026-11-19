from __future__ import annotations
import json
import pathlib
from dataclasses import asdict
from typing import Optional, List
from estudiante import Estudiante


def _resolver_ruta(ruta: str | pathlib.Path) -> pathlib.Path:
    p = pathlib.Path(ruta)
    try:
        if not p.parent.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return p


class RepositorioJSON:
    def __init__(self, ruta: str = "datos.json") -> None:
        self._ruta = _resolver_ruta(ruta)
        self._datos: dict[int, Estudiante] = {}
        self._cargar()

    @property
    def ruta(self) -> pathlib.Path:
        return self._ruta

    def _cargar(self) -> None:
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
        lista = [asdict(e) for e in self._datos.values()]
        with self._ruta.open("w", encoding="utf-8") as f:
            json.dump(lista, f, indent=2, ensure_ascii=False)

    def guardar(self, e: Estudiante) -> None:
        self._datos[e.codigo] = e
        self._persistir()

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._datos.get(cod)

    def listar(self) -> List[Estudiante]:
        return list(self._datos.values())

    def eliminar(self, cod: int) -> None:
        if cod in self._datos:
            self._datos.pop(cod, None)
            self._persistir()

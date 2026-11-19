from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Estudiante:
    codigo: int
    nombre: str
    ppa: float = 0.0
    notas: List[float] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.codigo}] {self.nombre} — PPA: {self.ppa:.2f} — Notas: {self.notas}"

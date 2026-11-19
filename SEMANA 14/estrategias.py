from __future__ import annotations
import math
from typing import Protocol, Sequence


class IEstrategiaCalculo(Protocol):
    def calcular(self, notas: Sequence[float]) -> float:
        ...


class PromedioSimple:
    def calcular(self, notas: Sequence[float]) -> float:
        if not notas:
            return 0.0
        return sum(notas) / len(notas)


class PromedioModerado:
    def calcular(self, notas: Sequence[float]) -> float:
        if not notas:
            return 0.0
        if len(notas) <= 2:
            return sum(notas) / len(notas)
        notas_ordenadas = sorted(notas)
        notas_intermedias = notas_ordenadas[1:-1]
        return sum(notas_intermedias) / len(notas_intermedias)


class PromedioGeometrico:
    def calcular(self, notas: Sequence[float]) -> float:
        if not notas:
            return 0.0
        producto = math.prod(notas)
        if producto < 0.0:
            return 0.0
        return float(producto ** (1.0 / len(notas)))

"""
Módulo de Estrategias de Cálculo de PPA (Patrón Strategy).
Permite intercambiar el algoritmo de evaluación académica en tiempo de ejecución.
"""
from __future__ import annotations
import math
from typing import Protocol, Sequence


class IEstrategiaCalculo(Protocol):
    """Protocolo abstracto que define el contrato de cálculo de notas."""
    def calcular(self, notas: Sequence[float]) -> float:
        ...


class PromedioSimple:
    """Calcula la media aritmética clásica de todas las notas."""
    def calcular(self, notas: Sequence[float]) -> float:
        if not notas:
            return 0.0
        return sum(notas) / len(notas)


class PromedioModerado:
    """
    Descarta la nota más baja y la más alta (valores extremos)
    y calcula la media de las calificaciones intermedias.
    """
    def calcular(self, notas: Sequence[float]) -> float:
        if not notas:
            return 0.0
        if len(notas) <= 2:
            return sum(notas) / len(notas)
        notas_ordenadas = sorted(notas)
        notas_intermedias = notas_ordenadas[1:-1]
        return sum(notas_intermedias) / len(notas_intermedias)


class PromedioGeometrico:
    """
    ADICIONAL Actividad 2A:
    Calcula la media geométrica (raíz n-ésima del producto de todas las notas).
    G = (x1 * x2 * ... * xn) ^ (1/n)
    """
    def calcular(self, notas: Sequence[float]) -> float:
        if not notas:
            return 0.0
        producto = math.prod(notas)
        if producto < 0.0:
            return 0.0
        return float(producto ** (1.0 / len(notas)))

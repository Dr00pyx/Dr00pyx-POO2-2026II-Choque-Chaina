"""
Módulo de Contexto para el Patrón Strategy.
Permite configurar y alternar dinámicamente la estrategia de cálculo en tiempo de ejecución.
"""
from __future__ import annotations
from typing import List
from estrategias import (
    IEstrategiaCalculo,
    PromedioSimple,
    PromedioModerado,
    PromedioGeometrico,
)
import logger as Logger


class ContextoCalculo:
    """Contexto que mantiene una referencia a una estrategia de cálculo."""
    def __init__(self, est: IEstrategiaCalculo) -> None:
        self._est = est

    def set_estrategia(self, est: IEstrategiaCalculo) -> None:
        Logger.log(f"Estrategia cambiada a {type(est).__name__}")
        self._est = est

    @property
    def estrategia_actual(self) -> IEstrategiaCalculo:
        return self._est

    def calcular(self, notas: List[float]) -> float:
        return self._est.calcular(notas)


def demostrar_strategy() -> None:
    print("=" * 65)
    print("DEMOSTRACIÓN DE STRATEGY CON CONTEXTO EXPLÍCITO")
    print("=" * 65)

    # 1. Caso estándar de la guía
    notas = [10.0, 15.0, 18.0, 20.0, 12.0]
    ctx = ContextoCalculo(PromedioSimple())
    ppa_simple = ctx.calcular(notas)
    ctx.set_estrategia(PromedioModerado())
    ppa_mod = ctx.calcular(notas)
    print(f"Notas simétricas: {notas}")
    print(f"Simple={ppa_simple:.1f} Moderado={ppa_mod:.1f}")

    # 2. Caso con notas asimétricas extremas para evidenciar la diferencia
    notas_asimetricas = [05.0, 14.0, 15.0, 16.0, 20.0]
    ctx.set_estrategia(PromedioSimple())
    ppa_sim_asym = ctx.calcular(notas_asimetricas)
    ctx.set_estrategia(PromedioModerado())
    ppa_mod_asym = ctx.calcular(notas_asimetricas)
    print(f"\nNotas asimétricas: {notas_asimetricas}")
    print(f"Simple={ppa_sim_asym:.2f} Moderado={ppa_mod_asym:.2f}")
    print(f"Diferencia observada: {abs(ppa_sim_asym - ppa_mod_asym):.2f} puntos")

    # 3. Caso con ADICIONAL: Promedio Geométrico
    ctx.set_estrategia(PromedioGeometrico())
    ppa_geo = ctx.calcular(notas_asimetricas)
    print(f"Geométrico={ppa_geo:.2f}")


if __name__ == "__main__":
    demostrar_strategy()

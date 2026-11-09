"""
Pruebas Unitarias para el Patrón Strategy (Actividad 2A).
"""
import pytest
import math
from estrategias import (
    PromedioSimple,
    PromedioModerado,
    PromedioGeometrico,
)
from strategy import ContextoCalculo
import logger


def test_promedio_simple():
    calc = PromedioSimple()
    assert calc.calcular([]) == 0.0
    assert calc.calcular([15.0]) == 15.0
    assert calc.calcular([10.0, 20.0]) == 15.0
    assert calc.calcular([10.0, 15.0, 18.0, 20.0, 12.0]) == 15.0


def test_promedio_moderado():
    calc = PromedioModerado()
    assert calc.calcular([]) == 0.0
    assert calc.calcular([15.0]) == 15.0
    assert calc.calcular([10.0, 20.0]) == 15.0

    # Caso guía: [10.0, 15.0, 18.0, 20.0, 12.0] -> descarta 10.0 y 20.0 -> [15, 18, 12] -> suma=45 / 3 = 15.0
    assert calc.calcular([10.0, 15.0, 18.0, 20.0, 12.0]) == 15.0

    # Caso asimétrico: [5.0, 14.0, 15.0, 16.0, 20.0] -> descarta 5 y 20 -> [14, 15, 16] -> suma=45 / 3 = 15.0
    assert calc.calcular([5.0, 14.0, 15.0, 16.0, 20.0]) == 15.0


def test_promedio_geometrico():
    calc = PromedioGeometrico()
    assert calc.calcular([]) == 0.0
    # [2.0, 8.0] -> sqrt(16) = 4.0
    assert pytest.approx(calc.calcular([2.0, 8.0]), 1e-4) == 4.0
    # [5.0, 5.0, 5.0] -> 5.0
    assert pytest.approx(calc.calcular([5.0, 5.0, 5.0]), 1e-4) == 5.0


def test_contexto_calculo_cambio_tiempo_ejecucion():
    logger.limpiar()
    ctx = ContextoCalculo(PromedioSimple())
    notas_asimetricas = [5.0, 14.0, 15.0, 16.0, 20.0]

    # Simple
    ppa_simple = ctx.calcular(notas_asimetricas)
    assert ppa_simple == 14.0

    # Cambiar a Moderado
    ctx.set_estrategia(PromedioModerado())
    ppa_mod = ctx.calcular(notas_asimetricas)
    assert ppa_mod == 15.0

    # Cambiar a Geométrico
    ctx.set_estrategia(PromedioGeometrico())
    ppa_geo = ctx.calcular(notas_asimetricas)
    producto_esperado = (5.0 * 14.0 * 15.0 * 16.0 * 20.0) ** (1.0 / 5.0)
    assert pytest.approx(ppa_geo, 1e-4) == producto_esperado

    # Verificar que el Logger registró los cambios de estrategia
    entradas = logger.get_entradas()
    assert len(entradas) == 2
    assert "Estrategia cambiada a PromedioModerado" in entradas[0]
    assert "Estrategia cambiada a PromedioGeometrico" in entradas[1]

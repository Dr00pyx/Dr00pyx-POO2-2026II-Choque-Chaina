"""
Actividad 2A: Demostración del Patrón Strategy con Contexto Explícito en Python 3.12+.
- Permite alternar la estrategia de cálculo en tiempo de ejecución con set_estrategia().
- Compara PromedioSimple vs PromedioModerado (descarte de extremos).
- Evidencia cuantitativamente la diferencia con notas extremas asimétricas.
- Incorpora el requerimiento adicional: PromedioGeometrico (raíz n-ésima del producto).
"""
from typing import List
from estrategias import (
    PromedioSimple,
    PromedioModerado,
    PromedioGeometrico,
)
from strategy import ContextoCalculo
import logger


def imprimir_tabla_comparativa(casos: List[tuple[str, List[float]]]) -> None:
    print("\n" + "=" * 80)
    print("TABLA COMPARATIVA DE ESTRATEGIAS DE CÁLCULO")
    print("=" * 80)
    print(f"{'Caso':<22} | {'Notas':<26} | {'Simple':<8} | {'Moderado':<8} | {'Geométr.':<8}")
    print("-" * 80)

    ctx_simple = ContextoCalculo(PromedioSimple())
    ctx_mod = ContextoCalculo(PromedioModerado())
    ctx_geo = ContextoCalculo(PromedioGeometrico())

    for nombre, notas in casos:
        p_simple = ctx_simple.calcular(notas)
        p_mod = ctx_mod.calcular(notas)
        p_geo = ctx_geo.calcular(notas)
        notas_str = str(notas)
        if len(notas_str) > 25:
            notas_str = notas_str[:22] + "..."
        print(f"{nombre:<22} | {notas_str:<26} | {p_simple:7.2f} | {p_mod:8.2f} | {p_geo:8.2f}")
    print("=" * 80)


def main():
    print("=" * 70)
    print("ACTIVIDAD 2A — PATRÓN STRATEGY CON CONTEXTO EXPLÍCITO (PYTHON 3.12+)")
    print("=" * 70)

    # 1. Caso base del documento oficial:
    notas_oficial = [10.0, 15.0, 18.0, 20.0, 12.0]
    print(f"\n[1] Caso base de la guía: notas = {notas_oficial}")

    ctx = ContextoCalculo(PromedioSimple())
    ppa_simple = ctx.calcular(notas_oficial)
    print(f"Cálculo inicial con PromedioSimple: {ppa_simple:.2f}")

    # Cambio dinámico de estrategia en runtime
    ctx.set_estrategia(PromedioModerado())
    ppa_mod = ctx.calcular(notas_oficial)
    print(f"Cálculo tras cambio a PromedioModerado: {ppa_mod:.2f}")
    print(f"Explicación del caso simétrico: sum([15, 18, 12])/3 = 45/3 = 15.0")
    print(f"Simple={ppa_simple:.1f} Moderado={ppa_mod:.1f}")

    # 2. Caso con notas extremas asimétricas para evidenciar la divergencia
    print("\n[2] Verificación de divergencia con notas extremas asimétricas:")
    notas_asimetricas = [05.0, 14.0, 15.0, 16.0, 20.0]
    ctx.set_estrategia(PromedioSimple())
    ppa_sim_asym = ctx.calcular(notas_asimetricas)
    ctx.set_estrategia(PromedioModerado())
    ppa_mod_asym = ctx.calcular(notas_asimetricas)
    diff = abs(ppa_sim_asym - ppa_mod_asym)
    print(f"Notas: {notas_asimetricas}")
    print(f"Promedio Simple   : {ppa_sim_asym:.2f} (suma=70 / 5 = 14.00)")
    print(f"Promedio Moderado : {ppa_mod_asym:.2f} (descarta 5.0 y 20.0 -> suma=45 / 3 = 15.00)")
    print(f"Diferencia real verificada: {diff:.2f} puntos")

    # 3. Adicional: Promedio Geométrico
    print("\n[3] ADICIONAL: Cálculo con PromedioGeometrico:")
    ctx.set_estrategia(PromedioGeometrico())
    ppa_geo = ctx.calcular(notas_asimetricas)
    print(f"Promedio Geométrico (raíz 5ta del producto): {ppa_geo:.2f}")

    # 4. Tabla de casos de prueba
    casos = [
        ("Simétricas (Guía)", [10.0, 15.0, 18.0, 20.0, 12.0]),
        ("Extrema Asimétrica", [5.0, 14.0, 15.0, 16.0, 20.0]),
        ("Uniforme", [14.0, 14.0, 14.0, 14.0]),
        ("Notas Altas", [18.0, 19.0, 20.0, 19.5, 18.5]),
        ("Notas Bajas", [05.0, 08.0, 06.0, 07.0, 09.0]),
    ]
    imprimir_tabla_comparativa(casos)


if __name__ == "__main__":
    main()

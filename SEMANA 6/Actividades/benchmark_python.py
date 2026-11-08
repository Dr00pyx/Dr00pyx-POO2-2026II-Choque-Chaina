# -*- coding: utf-8 -*-
"""
benchmark_python.py — Comparación empírica list vs dict vs set
"""
import timeit
import random

def benchmark(n: int) -> dict:
    datos = list(range(n))
    buscar = n // 2  # Buscar el elemento intermedio para consistencia
    datos_dict = dict.fromkeys(datos)
    datos_set = set(datos)

    # 5 000 búsquedas estándar; para 1 000 000 ajustamos muestras para rapidez
    reps = 5000 if n < 1_000_000 else 500
    factor = 1.0 if n < 1_000_000 else 10.0

    t_list = timeit.timeit(lambda: buscar in datos, number=reps) * factor
    t_dict = timeit.timeit(lambda: buscar in datos_dict, number=reps) * factor
    t_set  = timeit.timeit(lambda: buscar in datos_set, number=reps) * factor

    return {
        "n": n,
        "list_ms": t_list * 1000,
        "dict_ms": t_dict * 1000,
        "set_ms": t_set * 1000
    }

def main() -> None:
    print("=================================================================")
    print("BENCHMARK PYTHON 3.14: list vs dict vs set")
    print("=================================================================")
    print(f"{'N':>12} {'list (ms)':>15} {'dict (ms)':>15} {'set (ms)':>15}")
    print("-" * 62)

    for n in [1_000, 10_000, 100_000, 1_000_000]:
        r = benchmark(n)
        print(f"{r['n']:>12,} {r['list_ms']:>15.3f} {r['dict_ms']:>15.3f} {r['set_ms']:>15.3f}")

    print("=================================================================")

if __name__ == "__main__":
    main()

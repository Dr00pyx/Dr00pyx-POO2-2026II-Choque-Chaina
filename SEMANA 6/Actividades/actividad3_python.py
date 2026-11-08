# -*- coding: utf-8 -*-
"""
actividad3_python.py — Iteradores y estructuras en Python:
1. Generador ventana_deslizante
2. ColaAtencion con deque (FIFO)
3. Benchmark: deque.popleft() vs list.pop(0) con 10 000 elementos
"""
from collections import deque
from typing import Iterator, Any
import timeit

# ── 1. Generador ventana_deslizante ───────────────────────────────────────────
def ventana_deslizante(datos: list[Any], k: int) -> Iterator[list[Any]]:
    """
    Genera ventanas contiguas de tamaño k sobre una secuencia.
    Útil para cálculos en memoria eficiente (e.g. promedios móviles).
    """
    if k > len(datos):
        raise ValueError(f"Ventana k={k} mayor que datos={len(datos)}")
    for i in range(len(datos) - k + 1):
        yield datos[i : i + k]


# ── 2. ColaAtencion con deque (FIFO O(1)) ──────────────────────────────────────
class ColaAtencion:
    """
    Cola de atención FIFO para trámites o matrícula universitaria.
    deque garantiza append y popleft en O(1) amortizado, mientras que
    list.pop(0) es O(n) al desplazar todos los elementos restantes.
    """
    def __init__(self) -> None:
        self._cola: deque[Any] = deque()

    def encolar(self, elemento: Any) -> None:
        """Agrega un elemento al final de la cola: O(1)."""
        self._cola.append(elemento)

    def atender(self) -> Any | None:
        """Desencola y atiende el primer elemento de la cola: O(1)."""
        return self._cola.popleft() if self._cola else None

    def __len__(self) -> int:
        return len(self._cola)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._cola)

    def __bool__(self) -> bool:
        return bool(self._cola)


# ── 3. Benchmarking deque.popleft() vs list.pop(0) ────────────────────────────
def benchmark_cola(n: int = 10_000) -> None:
    """
    Compara el tiempo de vaciar una estructura de n elementos
    usando deque.popleft() [O(1)] vs list.pop(0) [O(n)].
    """
    print(f"\n>>> 3. BENCHMARK: deque.popleft() vs list.pop(0) (N = {n:,}):")
    print("-" * 65)

    setup_deque = f"from collections import deque; d = deque(range({n}))"
    stmt_deque = "while d: d.popleft()"
    t_deque = timeit.timeit(stmt=stmt_deque, setup=setup_deque, number=10)

    setup_list = f"l = list(range({n}))"
    stmt_list = "while l: l.pop(0)"
    t_list = timeit.timeit(stmt=stmt_list, setup=setup_list, number=10)

    t_deque_ms = (t_deque / 10) * 1000
    t_list_ms = (t_list / 10) * 1000
    ratio = t_list_ms / t_deque_ms if t_deque_ms > 0 else 0

    print(f"  * deque.popleft() : {t_deque_ms:.4f} ms por corrida (O(1) por op)")
    print(f"  * list.pop(0)     : {t_list_ms:.4f} ms por corrida (O(n) por op)")
    print(f"  -> deque es {ratio:.2f}x veces más rápido que list.pop(0)")


def main() -> None:
    print("=================================================================")
    print("ACTIVIDAD 3 (Python): GENERADOR, COLA FIFO Y BENCHMARK")
    print("=================================================================")

    # 1. Demostración de ventana deslizante
    print("\n>>> 1. GENERADOR DE VENTANA DESLIZANTE (Promedios móviles):")
    print("-" * 65)
    calificaciones = [10.0, 14.5, 18.0, 12.5, 16.0, 11.0, 19.0]
    print(f"Calificaciones: {calificaciones}")
    print("Promedios móviles (ventana k=3):")
    for ventana in ventana_deslizante(calificaciones, k=3):
        prom = sum(ventana) / len(ventana)
        print(f"  {ventana} -> promedio: {prom:.2f}")

    # 2. Demostración de ColaAtencion FIFO
    print("\n>>> 2. COLA DE ATENCIÓN FIFO CON deque:")
    print("-" * 65)
    cola = ColaAtencion()
    estudiantes_cola = ["Juan Mamani", "Maria Quispe", "Pedro Flores", "Ana Torres", "Carlos Condori"]
    for est in estudiantes_cola:
        cola.encolar(est)

    print(f"Total en cola de espera: {len(cola)}")
    print("Atención por ventanilla en estricto orden de llegada:")
    ticket = 1
    while cola:
        atendido = cola.atender()
        print(f"  Turno #{ticket}: {atendido} (restan {len(cola)} en espera)")
        ticket += 1

    # 3. Benchmark
    benchmark_cola(10_000)
    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
actividad2_main.py — Demostración de Repositorio genérico en Python con consultas de dominio y estadísticas
"""
from dataclasses import dataclass
from repositorio import Repositorio

@dataclass
class Estudiante:
    codigo: int
    nombre: str
    ppa: float
    escuela: str

def main() -> None:
    print("=" * 65)
    print("ACTIVIDAD 2: REPOSITORIO PYTHON GENÉRICO + CONSULTAS DE DOMINIO")
    print("=" * 65)

    # 1. Instanciación con lambda extractora de ID
    repo: Repositorio[Estudiante, int] = Repositorio(lambda e: e.codigo)

    # Guardar estudiantes
    estudiantes = [
        Estudiante(1001, "Juan Carlos Mamani", 15.2, "Ing. Sistemas"),
        Estudiante(1002, "Maria Elena Quispe", 18.5, "Ing. Sistemas"),
        Estudiante(1003, "Pedro Flores", 9.8, "Ciencias Comp."),
        Estudiante(1004, "Ana Torres", 13.0, "Ing. Sistemas"),
        Estudiante(1005, "Carlos Condori", 16.8, "Ing. Sistemas"),
        Estudiante(1006, "Lucia Morales", 14.7, "Ciencias Comp."),
    ]
    for e in estudiantes:
        repo.guardar(e)

    print(f"\nTotal estudiantes registrados (len): {len(repo)}")

    # Probar existe() y __contains__
    print(f"[existe(1002)]: {repo.existe(1002)}")
    print(f"[1002 in repo]: {1002 in repo}")
    print(f"[existe(9999)]: {repo.existe(9999)}")

    # Probar buscar()
    buscado = repo.buscar(1001)
    if buscado:
        print(f"[buscar(1001)]: Encontrado -> {buscado.nombre} (PPA: {buscado.ppa})")

    # Probar contar()
    n_destacados = repo.contar(lambda e: e.ppa >= 14.0)
    print(f"[contar(PPA >= 14.0)]: {n_destacados} estudiantes")

    # Probar primero()
    primer_cc = repo.primero(lambda e: e.escuela == "Ciencias Comp.")
    if primer_cc:
        print(f"[primero(escuela == 'Ciencias Comp.')]: {primer_cc.nombre} (PPA: {primer_cc.ppa})")

    # ── 3 CONSULTAS DE DOMINIO (REQUERIDAS) ───────────────────────────────────
    print("\n" + "-" * 65)
    print(">>> 3 CONSULTAS DE DOMINIO ACADÉMICO:")
    print("-" * 65)

    # Consulta 1: Estudiantes con PPA >= 14 en Ing. Sistemas
    destacados_sis = repo.filtrar(
        lambda e: e.ppa >= 14.0 and e.escuela == "Ing. Sistemas"
    )
    print(f"\n[Consulta 1] Destacados en Ing. Sistemas (PPA >= 14.0): {len(destacados_sis)}")
    for e in destacados_sis:
        print(f"  * [{e.codigo}] {e.nombre:<22} | PPA: {e.ppa:.2f}")

    # Consulta 2: Ranking completo por PPA
    ranking = repo.ordenar(key=lambda e: e.ppa, reverse=True)
    print("\n[Consulta 2] Ranking completo por PPA descendente:")
    for i, e in enumerate(ranking, 1):
        print(f"  {i}. [{e.codigo}] {e.nombre:<22} — {e.ppa:.2f} ({e.escuela})")

    # Consulta 3: Estadísticas por escuela usando comprensión de sets
    print("\n[Consulta 3] Estadísticas agrupadas por escuela:")
    escuelas = {e.escuela for e in repo}  # Set de escuelas únicas gracias a __iter__
    for esc in sorted(escuelas):
        alumnos = repo.filtrar(lambda e: e.escuela == esc)
        prom = sum(a.ppa for a in alumnos) / len(alumnos)
        print(f"  * Escuela '{esc}': {len(alumnos)} estudiantes | Promedio PPA: {prom:.2f}")

    # Protocolo iteración directa
    print("\n" + "-" * 65)
    print(">>> PROTOCOLO PYTHON (__iter__):")
    total_sistemas = sum(1 for e in repo if e.escuela == "Ing. Sistemas")
    print(f"Total directo iterando sobre repo (Ing. Sistemas): {total_sistemas}")

    # Estadísticas numéricas
    stats = repo.estadisticas("ppa")
    print(f"\n[Estadísticas globales PPA]:")
    print(f"  - Promedio : {stats['promedio']:.2f}")
    print(f"  - Máximo   : {stats['max']:.2f}")
    print(f"  - Mínimo   : {stats['min']:.2f}")
    print(f"  - Total (n): {stats['n']}")
    print("=" * 65)

if __name__ == "__main__":
    main()

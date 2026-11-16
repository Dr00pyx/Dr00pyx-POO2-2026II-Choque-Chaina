"""
Script Maestro de Ejecución — Semana 13
Ejecuta todas las actividades, pruebas unitarias y de persistencia, mostrando
los resultados formateados en consola.
"""
from __future__ import annotations
import subprocess
import sys


def ejecutar_comando(titulo: str, cmd: list[str]) -> bool:
    print("\n" + "=" * 75)
    print(f"▶ {titulo}")
    print("=" * 75)
    resultado = subprocess.run(cmd)
    if resultado.returncode == 0:
        print(f"\n[OK] {titulo} completado exitosamente.")
        return True
    else:
        print(f"\n[ERROR] Falló {titulo} (Código de salida: {resultado.returncode}).")
        return False


def main() -> None:
    print("***************************************************************************")
    print("*  UNIVERSIDAD NACIONAL DEL ALTIPLANO - PUNO                              *")
    print("*  SIS206 — Programación Orientada a Objetos II                           *")
    print("*  Semana 13 — Persistencia Multicapa (JSON, CSV, SQLite)                 *")
    print("***************************************************************************")

    pasos = [
        ("Actividad 1A: Demostración RepositorioJSON", [sys.executable, "actividad1_demo.py"]),
        ("Actividad 1: Pruebas de Persistencia JSON", [sys.executable, "test_json_persistencia.py"]),
        ("Actividad 2A: Demostración RepositorioCSV", [sys.executable, "actividad2_demo.py"]),
        ("Actividad 3A: Demostración RepositorioSQLite y LSP", [sys.executable, "actividad3_demo.py"]),
        ("Actividad 3: Pruebas de Sustitución con Pytest (LSP)", [sys.executable, "-m", "pytest", "test_repos.py", "-v"]),
    ]

    exitos = 0
    for titulo, cmd in pasos:
        if ejecutar_comando(titulo, cmd):
            exitos += 1

    print("\n" + "#" * 75)
    print(f"RESUMEN FINAL: {exitos}/{len(pasos)} fases ejecutadas con éxito.")
    print("#" * 75)
    if exitos == len(pasos):
        print("¡TODAS LAS PRÁCTICAS Y VERIFICACIONES DE LA SEMANA 13 PASARON EXITOSAMENTE!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

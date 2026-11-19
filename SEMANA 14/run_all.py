from __future__ import annotations
import subprocess
import sys


def run() -> None:
    print("=" * 65)
    print("UNIVERSIDAD NACIONAL DEL ALTIPLANO - PUNO")
    print("SIS206 - Programacion Orientada a Objetos II")
    print("Semana 14: GUI con Tkinter y PyQt5 - MVC para el Sistema Academico")
    print("=" * 65)

    print("\n[1/2] Ejecutando suite de pruebas unitarias...")
    res_test = subprocess.run([sys.executable, "-m", "unittest", "tests/test_practica14.py"])
    if res_test.returncode != 0:
        print("Error en las pruebas unitarias.")
        sys.exit(res_test.returncode)

    print("\n[2/2] Ejecutando demostración interactiva de MVC y Señales...")
    res_demo = subprocess.run([sys.executable, "demo_ejecucion.py"])
    if res_demo.returncode != 0:
        print("Error en la demostración.")
        sys.exit(res_demo.returncode)

    print("\n" + "=" * 65)
    print("TODAS LAS PRUEBAS Y DEMOSTRACIONES FINALIZARON CON EXITO")
    print("=" * 65)


if __name__ == "__main__":
    run()

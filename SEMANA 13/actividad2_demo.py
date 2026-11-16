"""
Demostración de Actividad 2A: RepositorioCSV con Persistencia Tabular.
Cubre:
1. Registro de 3 estudiantes en RepositorioCSV.
2. Verificación rigurosa del encabezado: codigo,nombre,ppa,notas.
3. Inspección del archivo CSV y formateo para visualización.
4. Edición manual simulada: agregado de un estudiante directamente en el archivo CSV.
5. Verificación de recarga automática al instanciar una nueva instancia de RepositorioCSV.
6. Eliminación y actualización física del archivo.
Semana 13 — Persistencia Multicapa
"""
from __future__ import annotations
import csv
import json
import os
import pathlib
from estudiante import Estudiante
from repositorio_csv import RepositorioCSV, CAMPOS

RUTA_CSV_DEMO = "/tmp/estudiantes_demo2.csv"


def demo_actividad_2a() -> None:
    print("=" * 70)
    print("ACTIVIDAD 2A — REPOSITORIOCSV CON PERSISTENCIA TABULAR")
    print("=" * 70)

    # 1. Registrar 3 estudiantes
    print("\n[Paso 1] Instanciando RepositorioCSV y registrando 3 estudiantes...")
    repo = RepositorioCSV(RUTA_CSV_DEMO)
    e1 = Estudiante(1001, "Ana Quispe", 15.5, [14.0, 18.0, 14.5])
    e2 = Estudiante(1002, "Juan Mamani", 12.0, [10.0, 12.0, 14.0])
    e3 = Estudiante(1003, "Lucia Morales", 17.5, [18.0, 17.0, 17.5])
    repo.guardar(e1)
    repo.guardar(e2)
    repo.guardar(e3)
    print(f"  ✓ Registrado: {e1}")
    print(f"  ✓ Registrado: {e2}")
    print(f"  ✓ Registrado: {e3}")
    assert len(repo.listar()) == 3

    # 2. Verificar encabezado y contenido del archivo CSV
    print(f"\n[Paso 2] Verificando encabezado y estructura en {repo.ruta}...")
    with repo.ruta.open("r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f if line.strip()]

    encabezado_real = lineas[0]
    encabezado_esperado = ",".join(CAMPOS)
    print(f"  Encabezado leído   : '{encabezado_real}'")
    print(f"  Encabezado esperado: '{encabezado_esperado}'")
    assert encabezado_real == encabezado_esperado, (
        f"Encabezado inválido. Obtenido '{encabezado_real}', esperado '{encabezado_esperado}'"
    )
    print("  ✓ Verificación de encabezado EXITOSA: codigo,nombre,ppa,notas")

    print("\n--- Contenido completo del archivo CSV ---")
    for i, linea in enumerate(lineas):
        print(f"  L{i+1}: {linea}")
    print("------------------------------------------")

    # 3. Agregar un 4to estudiante manualmente al CSV (simulando edición en VS Code / LibreOffice Calc)
    print("\n[Paso 3] Agregando un estudiante MANUALMENTE al archivo CSV (edición externa)...")
    estudiante_manual_csv = '1004,"Mario Vargas",14.0,"[13.0, 15.0]"\n'
    with repo.ruta.open("a", encoding="utf-8") as f:
        f.write(estudiante_manual_csv)
    print(f"  ✓ Línea anexada al archivo CSV: {estudiante_manual_csv.strip()}")

    # 4. Crear nueva instancia de RepositorioCSV para verificar la carga desde disco
    print("\n[Paso 4] Instanciando un nuevo RepositorioCSV para validar lectura del archivo editado...")
    repo_recargado = RepositorioCSV(RUTA_CSV_DEMO)
    estudiantes_cargados = repo_recargado.listar()
    print(f"  Total estudiantes cargados tras edición manual: {len(estudiantes_cargados)}")
    for est in estudiantes_cargados:
        print(f"    -> {est}")

    mario = repo_recargado.buscar(1004)
    assert mario is not None, "El estudiante agregado manualmente no fue encontrado"
    assert mario.nombre == "Mario Vargas"
    assert mario.notas == [13.0, 15.0]
    assert len(estudiantes_cargados) == 4, "Deberían haber exactamente 4 estudiantes cargados"
    print("  ✓ ÉXITO: El estudiante manual [1004] fue leído y deserializado correctamente.")

    # 5. Probar eliminación
    print("\n[Paso 5] Probando eliminación en CSV...")
    repo_recargado.eliminar(1002)
    assert repo_recargado.buscar(1002) is None
    assert len(repo_recargado.listar()) == 3
    print("  ✓ Estudiante 1002 eliminado del CSV.")

    # Limpieza final
    if repo.ruta.exists():
        repo.ruta.unlink()
    print(f"\n[Limpieza] Archivo temporal {repo.ruta} eliminado con éxito.")
    print("=" * 70)


if __name__ == "__main__":
    demo_actividad_2a()

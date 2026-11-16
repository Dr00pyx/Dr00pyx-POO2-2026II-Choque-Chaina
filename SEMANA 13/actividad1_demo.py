"""
Demostración de Actividad 1A: RepositorioJSON con Persistencia Real.
Cubre:
1. Registro de estudiantes y verificación de persistencia entre instancias.
2. Inspección del archivo JSON generado con formato legible.
3. Ejecución consecutiva sin borrar el archivo: análisis de idempotencia y conteo.
4. ADICIONAL: Eliminación de estudiante y verificación de sincronización en disco.
Semana 13 — Persistencia Multicapa
"""
from __future__ import annotations
import json
import os
import pathlib
from estudiante import Estudiante
from repositorio_json import RepositorioJSON

RUTA_DEMO = "/tmp/estudiantes_demo1.json"


def demo_actividad_1a() -> None:
    print("=" * 70)
    print("ACTIVIDAD 1A — REPOSITORIOJSON CON PERSISTENCIA REAL")
    print("=" * 70)

    # 1. Primera ejecución: instanciar y guardar
    print("\n[Paso 1] Creando instancia RepositorioJSON y guardando estudiantes...")
    r1 = RepositorioJSON(RUTA_DEMO)
    e1 = Estudiante(1001, "Ana Quispe", 15.5, [14.0, 18.0, 14.5])
    e2 = Estudiante(1002, "Juan Mamani", 12.0, [10.0, 12.0, 14.0])
    r1.guardar(e1)
    r1.guardar(e2)
    print(f"  ✓ Guardado: {e1}")
    print(f"  ✓ Guardado: {e2}")

    # 2. Inspeccionar el archivo JSON en disco
    print(f"\n[Paso 2] Inspeccionando archivo físico: {r1.ruta}")
    with r1.ruta.open("r", encoding="utf-8") as f:
        contenido = f.read()
    print("--- Contenido del archivo JSON generado ---")
    print(contenido)
    print("------------------------------------------")

    # 3. Segunda instancia: verificar que lee de disco
    print("\n[Paso 3] Creando segunda instancia independiente para verificar persistencia...")
    r2 = RepositorioJSON(RUTA_DEMO)
    estudiantes_cargados = r2.listar()
    print(f"  Total estudiantes recuperados de disco: {len(estudiantes_cargados)}")
    for est in estudiantes_cargados:
        print(f"    -> {est}")
    assert len(estudiantes_cargados) == 2, "Deberían haber exactamente 2 estudiantes"

    # 4. Pregunta reflexiva: ¿Cuántos estudiantes hay en la segunda ejecución sin borrar el JSON?
    print("\n[Paso 4] ANÁLISIS DE LA PREGUNTA REFLEXIVA:")
    print("  '¿Cuántos estudiantes hay si se ejecuta dos veces seguidas sin borrar el JSON?'")
    print("  -> Simulando segunda ejecución idéntica...")
    r_segunda_ejecucion = RepositorioJSON(RUTA_DEMO)
    # Volvemos a guardar los mismos estudiantes (códigos 1001 y 1002)
    r_segunda_ejecucion.guardar(Estudiante(1001, "Ana Quispe", 16.0, [15.0, 17.0]))
    r_segunda_ejecucion.guardar(Estudiante(1002, "Juan Mamani", 12.0, [10.0, 12.0, 14.0]))
    total_despues = len(r_segunda_ejecucion.listar())
    print(f"  Resultado obtenido: {total_despues} estudiantes.")
    print("  EXPLICACIÓN TÉCNICA:")
    print("  La colección interna usa un diccionario indexado por la clave primaria (e.codigo).")
    print("  Al guardar estudiantes con los mismos códigos (1001 y 1002), el diccionario actualiza")
    print("  el valor existente en lugar de duplicarlo (operación IDEMPOTENTE / UPSERT).")
    print("  Por lo tanto, la cantidad se mantiene exactamente en 2 estudiantes.")

    # 5. ADICIONAL: Probar método eliminar(cod)
    print("\n[Paso 5] ADICIONAL: Probar eliminar(cod) y verificar archivo en disco...")
    print("  Eliminando estudiante con código 1001...")
    r_segunda_ejecucion.eliminar(1001)

    # Verificar con una tercera instancia fresca
    r3 = RepositorioJSON(RUTA_DEMO)
    estudiantes_r3 = r3.listar()
    print(f"  Estudiantes en disco tras eliminación: {len(estudiantes_r3)}")
    for est in estudiantes_r3:
        print(f"    -> {est}")
    assert r3.buscar(1001) is None, "El estudiante 1001 debe haber sido eliminado"
    assert len(estudiantes_r3) == 1, "Debe quedar solo 1 estudiante"
    print("  ✓ Verificación de eliminación exitosa en memoria y disco.")

    # Limpieza final
    if r1.ruta.exists():
        r1.ruta.unlink()
    print(f"\n[Limpieza] Archivo temporal {r1.ruta} eliminado con éxito.")
    print("=" * 70)


if __name__ == "__main__":
    demo_actividad_1a()

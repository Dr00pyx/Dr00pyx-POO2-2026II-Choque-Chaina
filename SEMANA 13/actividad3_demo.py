"""
Demostración de Actividad 3A: RepositorioSQLite y Prueba de Sustitución LSP.
Cubre:
1. Creación y persistencia directa con RepositorioSQLite.
2. Comprobación de inserción, actualización (UPSERT) y borrado en SQLite.
3. Demostración en vivo de Sustitución Polimórfica (LSP): ServicioEstudiante
   funciona idénticamente con Memoria, JSON, CSV, SQLite y Mock.
4. Auditoría de invocaciones con MockRepositorio.
Semana 13 — Persistencia Multicapa
"""
from __future__ import annotations
import sqlite3
import os
from estudiante import Estudiante
from estrategias import PromedioSimple
from servicios import ServicioEstudiante
from repositorios import (
    RepositorioMemoria,
    RepositorioJSON,
    RepositorioCSV,
    RepositorioSQLite,
    MockRepositorio,
)

RUTA_SQLITE_DEMO = "/tmp/estudiantes_demo3.db"


def demo_actividad_3a() -> None:
    print("=" * 70)
    print("ACTIVIDAD 3A — REPOSITORIOSQLITE Y PRINCIPIO DE SUSTITUCIÓN (LSP)")
    print("=" * 70)

    # 1. Operaciones directas con RepositorioSQLite
    print("\n[Paso 1] Creando RepositorioSQLite y guardando estudiantes...")
    repo_sql = RepositorioSQLite(RUTA_SQLITE_DEMO)
    e1 = Estudiante(1001, "Ana Quispe", 15.5, [14.0, 18.0, 14.5])
    e2 = Estudiante(1002, "Juan Mamani", 12.0, [10.0, 12.0, 14.0])
    repo_sql.guardar(e1)
    repo_sql.guardar(e2)
    print(f"  ✓ Insertado: {e1}")
    print(f"  ✓ Insertado: {e2}")

    # Consultar y listar desde SQLite
    print("\n[Paso 2] Listando registros desde SQLite...")
    registros = repo_sql.listar()
    for r in registros:
        print(f"  -> {r}")
    assert len(registros) == 2

    # Actualización (UPSERT)
    print("\n[Paso 3] Probando actualización (INSERT OR REPLACE) de Juan Mamani...")
    e2_actualizado = Estudiante(1002, "Juan Mamani", 14.5, [14.0, 15.0])
    repo_sql.guardar(e2_actualizado)
    recuperado = repo_sql.buscar(1002)
    print(f"  -> Recuperado actualizado: {recuperado}")
    assert recuperado.ppa == 14.5

    # Cierre y limpieza de la demo directa
    repo_sql.cerrar()
    if os.path.exists(repo_sql.ruta):
        os.remove(repo_sql.ruta)
    print("  ✓ Conexión SQLite cerrada y archivo temporal removido.")

    # 2. Prueba de Sustitución Polimórfica (LSP) en tiempo de ejecución
    print("\n[Paso 4] DEMOSTRACIÓN DE SUSTITUCIÓN POLIMÓRFICA (LSP):")
    print("  El mismo ServicioEstudiante interactuará secuencialmente con 5 backends:")
    print("  1) RepositorioMemoria")
    print("  2) RepositorioJSON")
    print("  3) RepositorioCSV")
    print("  4) RepositorioSQLite")
    print("  5) MockRepositorio (con auditoría de llamadas)")

    backends = [
        ("Memoria", RepositorioMemoria()),
        ("JSON", RepositorioJSON("/tmp/lsp_temp.json")),
        ("CSV", RepositorioCSV("/tmp/lsp_temp.csv")),
        ("SQLite", RepositorioSQLite("/tmp/lsp_temp.db")),
        ("Mock", MockRepositorio()),
    ]

    for nombre, repo_backend in backends:
        # Se inyecta el repositorio sin alterar ninguna línea de ServicioEstudiante
        svc = ServicioEstudiante(repo_backend, PromedioSimple())
        nuevo_estudiante = Estudiante(3001, f"Estudiante_{nombre}", 0.0, [16.0, 18.0, 20.0])
        svc.registrar(nuevo_estudiante)

        # Verificación uniforme
        encontrado = svc.buscar(3001)
        assert encontrado is not None
        assert encontrado.nombre == f"Estudiante_{nombre}"
        assert abs(encontrado.ppa - 18.0) < 0.001
        print(f"  [OK] Backend '{nombre:<7}' -> Registrado y recuperado con éxito: {encontrado}")

        # Si es el Mock, auditamos que guardar() se haya ejecutado
        if isinstance(repo_backend, MockRepositorio):
            print(f"       Auditoría Mock: guardar() invocado {repo_backend.veces_guardar} vez/veces.")

        # Limpieza de archivos creados en el bucle
        if hasattr(repo_backend, "cerrar"):
            repo_backend.cerrar()
        if hasattr(repo_backend, "ruta") and os.path.exists(str(repo_backend.ruta)):
            try:
                os.remove(str(repo_backend.ruta))
            except OSError:
                pass

    print("\n" + "=" * 70)
    print("CONCLUSIÓN ARQUITECTÓNICA:")
    print("ServicioEstudiante permaneció inmutable (Open/Closed Principle).")
    print("Todos los repositorios cumplieron el contrato (Liskov Substitution Principle).")
    print("=" * 70)


if __name__ == "__main__":
    demo_actividad_3a()

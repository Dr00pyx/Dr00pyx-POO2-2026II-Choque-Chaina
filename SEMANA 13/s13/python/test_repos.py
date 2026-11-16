"""
test_repos.py — Prueba de Sustitución (Liskov Substitution Principle - LSP)
Semana 13 — Persistencia Multicapa

==============================================================================
RESPUESTA REFLEXIVA (Actividad 3A):
¿ServicioEstudiante cambió alguna línea al incorporar los diferentes repositorios?

RESPUESTA:
NO, ServicioEstudiante NO cambió absolutamente ninguna línea de código.

JUSTIFICACIÓN TEÓRICA Y DE DISEÑO DE SOFTWARE:
1. Principio de Sustitución de Liskov (LSP):
   Todas las implementaciones (RepositorioMemoria, RepositorioJSON, RepositorioCSV,
   RepositorioSQLite y MockRepositorio) respetan de forma estricta el contrato
   establecido por el protocolo IRepositorioEstudiante. Cualquier backend puede
   sustituir a otro sin que el cliente (ServicioEstudiante) note la diferencia ni
   se rompa la consistencia del dominio.

2. Principio de Inversión de Dependencias (DIP):
   ServicioEstudiante (módulo de alto nivel / controlador) no depende de los
   módulos de bajo nivel (mecanismos de persistencia I/O en disco o BD), sino
   de la abstracción común IRepositorioEstudiante.

3. Principio de Abierto / Cerrado (OCP):
   El sistema está abierto a la extensión (podemos agregar RepositorioParquet,
   RepositorioPostgres, RepositorioRedis, etc.) pero cerrado a la modificación
   (ServicioEstudiante permanece intocable y libre de regresiones).
==============================================================================
"""

import os
import pytest
from servicios import ServicioEstudiante
from estrategias import PromedioSimple
from estudiante import Estudiante
from repositorios import (
    RepositorioMemoria,
    RepositorioJSON,
    RepositorioCSV,
    RepositorioSQLite,
    MockRepositorio,  # ADICIONAL: 5° parámetro para auditar llamadas
)


@pytest.mark.parametrize("RepoClass,kwargs,cleanup", [
    (RepositorioMemoria, {}, None),
    (RepositorioJSON, {"ruta": "/tmp/t.json"}, "/tmp/t.json"),
    (RepositorioCSV, {"ruta": "/tmp/t.csv"}, "/tmp/t.csv"),
    (RepositorioSQLite, {"ruta": "/tmp/t.db"}, "/tmp/t.db"),
    (MockRepositorio, {}, None),  # ADICIONAL Actividad 3A: 5° backend
])
def test_servicio_con_cualquier_repo(RepoClass, kwargs, cleanup):
    repo = RepoClass(**kwargs)
    svc = ServicioEstudiante(repo, PromedioSimple())
    e1 = Estudiante(1001, "Ana", 0.0, [15.0, 18.0, 14.0])
    e2 = Estudiante(1002, "Juan", 0.0, [10.0, 12.0, 14.0])

    svc.registrar(e1)
    svc.registrar(e2)

    assert svc.buscar(1001).nombre == "Ana"
    assert svc.buscar(1002) is not None
    assert len(repo.listar()) == 2

    # Verificación ADICIONAL si es MockRepositorio:
    # Comprobar cuántas veces se llamó guardar()
    if isinstance(repo, MockRepositorio):
        assert repo.veces_guardar == 2, (
            f"MockRepositorio esperaba 2 llamadas a guardar(), pero recibió {repo.veces_guardar}"
        )

    # Cierre explícito para liberar locks de archivo en Windows (ej. SQLite)
    if hasattr(repo, "cerrar"):
        repo.cerrar()

    # Limpieza del archivo temporal
    if cleanup and os.path.exists(cleanup):
        try:
            os.remove(cleanup)
        except OSError:
            pass
    if hasattr(repo, "ruta") and os.path.exists(str(repo.ruta)):
        try:
            os.remove(str(repo.ruta))
        except OSError:
            pass

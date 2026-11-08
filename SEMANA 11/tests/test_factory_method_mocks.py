"""
Pruebas Unitarias con Mocks para el Patrón Factory Method (Capa de Repositorios).
Verifica que cada fábrica cree exactamente el tipo concreto correcto y que el
despachador cumpla con DIP y OCP mediante dobles de prueba (Mocks).
"""
from unittest.mock import MagicMock, patch
import pytest
from factory.modelo import Estudiante
from factory.repositorio import RepositorioEstudiantes
from factory.repo_memoria import RepositorioMemoria
from factory.repo_archivo import RepositorioArchivoJSON
from factory.repo_bd import RepositorioSQLite
from factory.creadores import (
    CreadorRepositorio,
    CreadorRepoMemoria,
    CreadorRepoArchivo,
    CreadorRepoSQLite
)
from factory.registro import RegistroFabricaRepositorios


def test_creador_memoria_retorna_tipo_correcto():
    creador = CreadorRepoMemoria()
    repo = creador.crear_repositorio()
    assert isinstance(repo, RepositorioMemoria)
    assert isinstance(repo, RepositorioEstudiantes)
    assert "Memoria" in repo.tipo_almacenamiento


def test_creador_archivo_retorna_tipo_correcto(tmp_path):
    ruta_json = tmp_path / "test_estudiantes.json"
    creador = CreadorRepoArchivo(ruta_archivo=str(ruta_json))
    repo = creador.crear_repositorio()
    assert isinstance(repo, RepositorioArchivoJSON)
    assert isinstance(repo, RepositorioEstudiantes)
    assert "JSON" in repo.tipo_almacenamiento


def test_creador_sqlite_retorna_tipo_correcto(tmp_path):
    ruta_db = tmp_path / "test_academico.db"
    creador = CreadorRepoSQLite(ruta_db=str(ruta_db))
    repo = creador.crear_repositorio()
    assert isinstance(repo, RepositorioSQLite)
    assert isinstance(repo, RepositorioEstudiantes)
    assert "SQLite" in repo.tipo_almacenamiento


def test_registro_fabrica_despacha_tipos_correctos(tmp_path):
    reg = RegistroFabricaRepositorios()
    # Inyectar rutas temporales limpias
    reg.registrar("archivo_tmp", lambda: CreadorRepoArchivo(str(tmp_path / "data.json")))
    reg.registrar("sqlite_tmp", lambda: CreadorRepoSQLite(str(tmp_path / "data.db")))

    repo_mem = reg.fabricar("memoria")
    repo_arc = reg.fabricar("archivo_tmp")
    repo_sql = reg.fabricar("sqlite_tmp")

    assert isinstance(repo_mem, RepositorioMemoria)
    assert isinstance(repo_arc, RepositorioArchivoJSON)
    assert isinstance(repo_sql, RepositorioSQLite)


def test_creador_con_mock_repositorio():
    """
    Verifica con Mock que una subclase de CreadorRepositorio invoque y
    utilice el producto según el contrato de Factory Method.
    """
    mock_repo = MagicMock(spec=RepositorioEstudiantes)
    
    class CreadorMock(CreadorRepositorio):
        def crear_repositorio(self) -> RepositorioEstudiantes:
            return mock_repo

    creador = CreadorMock()
    estudiantes_test = [
        Estudiante(codigo="2023999", nombre="Estudiante Test", carrera="Sistemas", promedio=16.0)
    ]
    resultado = creador.inicializar_con_semillas(estudiantes_test)

    assert resultado is mock_repo
    mock_repo.guardar.assert_called_once_with(estudiantes_test[0])


def test_repositorio_crud_completo(tmp_path):
    """Verifica operaciones CRUD idénticas a través del contrato polimórfico."""
    ruta_db = tmp_path / "crud.db"
    ruta_json = tmp_path / "crud.json"

    repositorios = [
        RepositorioMemoria(),
        RepositorioArchivoJSON(ruta_json),
        RepositorioSQLite(ruta_db),
    ]

    est = Estudiante(codigo="2026111", nombre="Alumno CRUD", carrera="Sistemas", promedio=17.0)

    for repo in repositorios:
        # Guardar
        assert repo.guardar(est) is True
        # Buscar
        encontrado = repo.buscar_por_codigo("2026111")
        assert encontrado is not None
        assert encontrado.nombre == "Alumno CRUD"
        assert encontrado.promedio == 17.0
        # Listar
        todos = repo.listar_todos()
        assert len(todos) >= 1
        # Eliminar
        assert repo.eliminar("2026111") is True
        assert repo.buscar_por_codigo("2026111") is None

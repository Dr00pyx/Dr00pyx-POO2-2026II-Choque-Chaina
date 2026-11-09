"""
Pruebas Unitarias para el Patrón Observer (Actividad 1A).
"""
import pytest
from estudiante import Estudiante
from repositorios import RepositorioMemoria
from observer import (
    RepositorioObservable,
    LoggerObservador,
    ConsolaObservador,
    EmailObservador,
    IObservador,
)
import logger


class ObservadorMock:
    """Observador espía para verificar invocaciones y payloads."""
    def __init__(self):
        self.llamadas = []

    def on_guardado(self, e: Estudiante) -> None:
        self.llamadas.append(e)


def test_repositorio_observable_notifica_a_todos_los_suscriptores(capsys):
    logger.limpiar()
    repo_base = RepositorioMemoria()
    repo_obs = RepositorioObservable(repo_base)

    spy1 = ObservadorMock()
    spy2 = ObservadorMock()
    obs_log = LoggerObservador()
    obs_consola = ConsolaObservador()
    obs_email = EmailObservador()

    repo_obs.suscribir(spy1)
    repo_obs.suscribir(spy2)
    repo_obs.suscribir(obs_log)
    repo_obs.suscribir(obs_consola)
    repo_obs.suscribir(obs_email)

    est = Estudiante(101, "Test Alumno", 17.5, [16.0, 18.0, 18.5])
    repo_obs.guardar(est)

    # Verificación de espías
    assert len(spy1.llamadas) == 1
    assert spy1.llamadas[0].codigo == 101
    assert len(spy2.llamadas) == 1
    assert spy2.llamadas[0].nombre == "Test Alumno"

    # Verificación de Logger
    entradas = logger.get_entradas()
    assert len(entradas) == 1
    assert "Guardado: [101] Test Alumno" in entradas[0]

    # Verificación de salida en consola (ConsolaObservador y EmailObservador)
    captured = capsys.readouterr()
    assert ">> Vista: [101] Test Alumno — PPA: 17.5" in captured.out
    assert "Enviando correo a Test Alumno" in captured.out


def test_repositorio_observable_desuscribir():
    repo_base = RepositorioMemoria()
    repo_obs = RepositorioObservable(repo_base)

    spy = ObservadorMock()
    repo_obs.suscribir(spy)
    assert len(repo_obs.observadores) == 1

    repo_obs.desuscribir(spy)
    assert len(repo_obs.observadores) == 0

    est = Estudiante(102, "Alumno Sin Observar", 15.0)
    repo_obs.guardar(est)
    assert len(spy.llamadas) == 0


def test_repositorio_observable_delegacion_buscar_listar():
    repo_base = RepositorioMemoria()
    repo_obs = RepositorioObservable(repo_base)

    e1 = Estudiante(201, "Alumno A", 14.0)
    e2 = Estudiante(202, "Alumno B", 18.0)

    repo_obs.guardar(e1)
    repo_obs.guardar(e2)

    assert repo_obs.buscar(201) == e1
    assert repo_obs.buscar(999) is None
    lista = repo_obs.listar()
    assert len(lista) == 2
    assert e1 in lista
    assert e2 in lista

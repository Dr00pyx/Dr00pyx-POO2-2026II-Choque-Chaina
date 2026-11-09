"""
Pruebas de Integración para el MVC Completo con Observer y Strategy (Actividad 3A).
"""
import pytest
from estudiante import Estudiante
from repositorios import RepositorioMemoria
from observer import RepositorioObservable, ConsolaObservador, LoggerObservador
from servicios import ServicioEstudiante
from estrategias import PromedioSimple, PromedioModerado
import logger


def test_mvc_flujo_completo_4_estudiantes(capsys):
    logger.limpiar()
    repo_base = RepositorioMemoria()
    repo_obs = RepositorioObservable(repo_base)

    vista = ConsolaObservador()
    log_obs = LoggerObservador()
    repo_obs.suscribir(vista)
    repo_obs.suscribir(log_obs)

    svc = ServicioEstudiante(repo_obs, PromedioSimple())

    estudiantes = [
        Estudiante(1001, "Ana Quispe", 0.0, [14.0, 18.0, 16.0]),
        Estudiante(1002, "Juan Mamani", 0.0, [12.0, 15.0, 10.0]),
        Estudiante(1003, "Rosa Quispe", 0.0, [18.0, 20.0, 19.0]),
    ]

    for e in estudiantes:
        svc.registrar(e)

    # Registro de 4to estudiante con notas [5.0, 5.0, 5.0]
    e4 = Estudiante(1004, "Carlos Ramos", 0.0, [5.0, 5.0, 5.0])
    svc.registrar(e4)

    assert pytest.approx(e4.ppa, 1e-4) == 5.0
    assert len(logger.get_entradas()) == 4

    # Verificar que el repositorio persistió los 4 estudiantes
    assert len(repo_obs.listar()) == 4
    assert repo_obs.buscar(1004).ppa == 5.0

    # Verificar salida en consola (cada estudiante genera 2 líneas: >> Vista y [LOG])
    out = capsys.readouterr().out
    assert ">> Vista: [1001] Ana Quispe — PPA: 16.0" in out
    assert ">> Vista: [1004] Carlos Ramos — PPA: 5.0" in out


def test_mvc_intercambio_estrategia_en_controlador():
    logger.limpiar()
    repo_base = RepositorioMemoria()
    repo_obs = RepositorioObservable(repo_base)
    svc = ServicioEstudiante(repo_obs, PromedioSimple())

    # Notas con extremos asimétricos: 5 y 20
    e_asym = Estudiante(1005, "Laura Choque", 0.0, [5.0, 14.0, 16.0, 20.0])
    svc.registrar(e_asym)
    # Simple: (5+14+16+20)/4 = 55/4 = 13.75
    assert pytest.approx(e_asym.ppa, 1e-4) == 13.75

    # Cambiamos a PromedioModerado
    svc.set_estrategia(PromedioModerado())
    e_asym2 = Estudiante(1006, "Pedro Condori", 0.0, [5.0, 14.0, 16.0, 20.0])
    svc.registrar(e_asym2)
    # Moderado: descarta 5 y 20 -> (14+16)/2 = 15.0
    assert pytest.approx(e_asym2.ppa, 1e-4) == 15.0

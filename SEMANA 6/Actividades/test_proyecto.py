# -*- coding: utf-8 -*-
"""
test_proyecto.py — Suite de pruebas automatizadas con pytest para Repositorio y Proyecto Integrador
"""
import pytest
from repositorio import Repositorio
from actividad3_python import ColaAtencion, ventana_deslizante
from proyecto_integrador import Docente, Administrativo, SistemaGestionUNAP

# ── Pruebas del Repositorio Genérico ──────────────────────────────────────────
def test_repositorio_crud():
    repo: Repositorio[Docente, str] = Repositorio(lambda d: d.dni)
    assert len(repo) == 0

    doc1 = Docente("11112222", "Juan", "Perez", "Auxiliar", 20, 1.0)
    repo.guardar(doc1)
    assert len(repo) == 1
    assert repo.existe("11112222")
    assert not repo.existe("99999999")

    # buscar
    recuperado = repo.buscar("11112222")
    assert recuperado is not None
    assert recuperado.nombre_completo == "Perez, Juan"

    # eliminar
    assert repo.eliminar("11112222")
    assert not repo.existe("11112222")
    assert len(repo) == 0
    assert not repo.eliminar("11112222")


def test_repositorio_consultas():
    repo: Repositorio[Docente, str] = Repositorio(lambda d: d.dni)
    repo.guardar(Docente("111", "A", "Doc1", "Auxiliar", 10, 1.0))
    repo.guardar(Docente("222", "B", "Doc2", "Asociado", 30, 1.4))
    repo.guardar(Docente("333", "C", "Doc3", "Principal", 40, 1.8))

    # contar
    assert repo.contar(lambda d: d.horas >= 30) == 2

    # primero
    primero = repo.primero(lambda d: d.categoria == "Principal")
    assert primero is not None
    assert primero.dni == "333"

    # filtrar
    filtrados = repo.filtrar(lambda d: d.horas > 20)
    assert len(filtrados) == 2

    # ordenar
    ordenados = repo.ordenar(key=lambda d: d.calcular_remuneracion(), reverse=True)
    assert ordenados[0].dni == "333"
    assert ordenados[-1].dni == "111"

    # acumular
    total_horas = repo.acumular(0, lambda acc, d: acc + d.horas)
    assert total_horas == 80


# ── Pruebas de ColaAtencion y Ventana Deslizante ──────────────────────────────
def test_cola_atencion_fifo():
    cola = ColaAtencion()
    assert len(cola) == 0
    assert not cola

    cola.encolar("Ticket1")
    cola.encolar("Ticket2")
    assert len(cola) == 2
    assert bool(cola) is True

    assert cola.atender() == "Ticket1"
    assert cola.atender() == "Ticket2"
    assert cola.atender() is None
    assert len(cola) == 0


def test_ventana_deslizante():
    datos = [10, 20, 30, 40, 50]
    ventanas = list(ventana_deslizante(datos, k=3))
    assert ventanas == [
        [10, 20, 30],
        [20, 30, 40],
        [30, 40, 50]
    ]

    with pytest.raises(ValueError):
        list(ventana_deslizante([1, 2], k=5))


# ── Pruebas del Sistema Integrador ───────────────────────────────────────────
def test_sistema_gestion_unap():
    sistema = SistemaGestionUNAP()
    sistema.registrar_docente(Docente("70112233", "Carlos", "Mamani", "Principal", 40, 1.8))
    sistema.registrar_docente(Docente("70223344", "Elena", "Flores", "Asociado", 35, 1.4))
    sistema.registrar_administrativo(Administrativo("80112233", "Rosa", "Quispe", "RRHH", 2800.0, 450.0))

    # Consultas
    assert len(sistema.docentes_tiempo_completo()) == 2
    assert len(sistema.administrativos_con_bono()) == 1
    assert sistema.total_planilla_docentes() == (40 * 75 * 1.8) + (35 * 75 * 1.4)

    # Cola de atención
    sistema.encolar_tramite("70112233")
    assert sistema.atender_tramite() == "70112233"
    assert sistema.atender_tramite() is None

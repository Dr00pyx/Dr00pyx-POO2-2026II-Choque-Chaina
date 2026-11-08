# test_estudiante.py — Pruebas unitarias con pytest para Estudiante
import pytest
import json
from dataclasses import asdict
from estudiante import Estudiante


def test_creacion_estudiante_valido():
    e = Estudiante(1001, "Ana Quispe", 15.5, 3)
    assert e.codigo == 1001
    assert e.nombre == "Ana Quispe"
    assert e.ppa == 15.5
    assert e.ciclo == 3
    assert e.notas == []
    assert e.es_aprobado() is True


def test_codigo_invalido():
    with pytest.raises(ValueError, match="Codigo debe ser positivo"):
        Estudiante(0, "Juan Perez", 14.0, 1)

    with pytest.raises(ValueError, match="Codigo debe ser positivo"):
        Estudiante(-5, "Juan Perez", 14.0, 1)


def test_nombre_invalido():
    with pytest.raises(ValueError, match="Nombre no puede estar vacio"):
        Estudiante(1002, "", 14.0, 1)

    with pytest.raises(ValueError, match="Nombre no puede estar vacio"):
        Estudiante(1002, "   ", 14.0, 1)


def test_ppa_invalido():
    with pytest.raises(ValueError, match="PPA debe estar entre 0 y 20"):
        Estudiante(1003, "Carlos Tito", -0.5, 2)

    with pytest.raises(ValueError, match="PPA debe estar entre 0 y 20"):
        Estudiante(1003, "Carlos Tito", 20.1, 2)


def test_agregar_notas_y_promedio():
    e = Estudiante(1004, "Elena Flores", 16.0, 4)
    # Promedio sin notas debe ser None
    assert e.calcular_promedio() is None

    # Agregar 5 notas
    notas = [14.0, 15.0, 16.0, 18.0, 17.0]
    for n in notas:
        e.agregar_nota(n)

    assert len(e.notas) == 5
    assert e.calcular_promedio() == pytest.approx(16.0, 0.01)


def test_agregar_nota_fuera_de_rango():
    e = Estudiante(1005, "Roberto Gomez", 12.0, 2)
    with pytest.raises(ValueError, match="fuera de rango"):
        e.agregar_nota(-1.0)

    with pytest.raises(ValueError, match="fuera de rango"):
        e.agregar_nota(20.5)


def test_es_aprobado():
    aprobado = Estudiante(1006, "Sofia Diaz", 11.0, 3)
    assert aprobado.es_aprobado() is True

    desaprobado = Estudiante(1007, "Lucas Mamani", 10.9, 3)
    assert desaprobado.es_aprobado() is False


def test_serializacion_json():
    e = Estudiante(1008, "Marcos Ruiz", 17.25, 6)
    e.agregar_nota(16.0)
    e.agregar_nota(19.0)

    datos = asdict(e)
    cadena_json = json.dumps(datos)
    
    assert "Marcos Ruiz" in cadena_json
    assert "17.25" in cadena_json
    assert "notas" in datos
    assert datos["notas"] == [16.0, 19.0]

import pytest
from gestor_academico import (
    Estudiante,
    RepositorioEstudiantes,
    ServicioAcademico,
    GeneradorReporteCSV,
)

def test_validacion_rango_nota():
    est = Estudiante("202601", "Juan Pérez")
    est.agregar_nota(15.0)
    assert len(est.notas) == 1
    
    with pytest.raises(ValueError):
        est.agregar_nota(25.0)

def test_calculo_promedio_y_estado():
    est = Estudiante("202602", "Maria Lopez")
    est.agregar_nota(12.0)
    est.agregar_nota(14.0)
    assert est.promedio == 13.0
    assert est.esta_aprobado is True

def test_servicio_academico_sin_io():
    repo = RepositorioEstudiantes()
    servicio = ServicioAcademico(repo)  # Usa AuditoriaNull por defecto
    
    servicio.registrar_estudiante("202603", "Carlos Gómez")
    servicio.agregar_nota_estudiante("202603", 18.0)
    
    est = repo.buscar_por_codigo("202603")
    assert est is not None
    assert est.nombre == "Carlos Gómez"
    assert est.promedio == 18.0

def test_generacion_reporte_csv():
    est1 = Estudiante("01", "Ana")
    est1.agregar_nota(15.0)
    
    lineas = GeneradorReporteCSV.generar_lineas([est1])
    assert len(lineas) == 2
    assert lineas[1] == "01,Ana,15.00,APROBADO"
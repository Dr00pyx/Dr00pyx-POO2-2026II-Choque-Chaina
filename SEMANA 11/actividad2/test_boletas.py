"""
Pruebas Unitarias para el sistema de Boletas Académicas (Factory Method + Registry).
Verifica:
1. Instanciación correcta de productos concretos a través de las fábricas.
2. Comportamiento del Template Method en GeneradorBoleta.
3. Cálculo exacto de créditos y promedio ponderado.
4. Cumplimiento de OCP mediante registro dinámico de nuevos formatos.
5. Manejo de excepciones ante formatos no registrados.
"""
from pathlib import Path
import pytest
from boletas import (
    BoletaNotas,
    BoletaTXT,
    BoletaCSV,
    BoletaHTML,
    GeneradorBoleta,
    GeneradorBoletaTXT,
    GeneradorBoletaCSV,
    GeneradorBoletaHTML,
    RegistroGeneradores,
)


@pytest.fixture
def registro_configurado():
    reg = RegistroGeneradores()
    reg.registrar("txt", GeneradorBoletaTXT)
    reg.registrar("csv", GeneradorBoletaCSV)
    reg.registrar("html", GeneradorBoletaHTML)
    return reg


@pytest.fixture
def notas_ejemplo():
    return [
        {"curso": "POO II", "creditos": 4, "nota": 18.0},
        {"curso": "Bases de Datos", "creditos": 4, "nota": 14.0},
        {"curso": "Algoritmos", "creditos": 2, "nota": 16.0},
    ]


def test_factory_method_instancia_tipos_correctos(registro_configurado):
    """Verifica que cada creador concreto genere su producto correspondiente."""
    gen_txt = registro_configurado.crear("txt")
    gen_csv = registro_configurado.crear("csv")
    gen_html = registro_configurado.crear("html")

    assert isinstance(gen_txt.crear_boleta(), BoletaTXT)
    assert isinstance(gen_csv.crear_boleta(), BoletaCSV)
    assert isinstance(gen_html.crear_boleta(), BoletaHTML)


def test_calculos_academicos():
    """Verifica el cálculo de créditos, promedio ponderado y estado académico."""
    boleta = BoletaTXT(estudiante="Carlos Mamani", codigo="2024001", semestre="2026-II")
    boleta.agregar_nota("Curso A", 16.0, 4)
    boleta.agregar_nota("Curso B", 12.0, 4)
    # Total creditos = 8. Promedio = (16*4 + 12*4) / 8 = 112 / 8 = 14.0
    assert boleta.total_creditos == 8
    assert boleta.promedio_ponderado == 14.0
    assert boleta.estado_final == "APROBADO"


def test_desaprobado():
    boleta = BoletaCSV(estudiante="Juan Perez", codigo="2024002", semestre="2026-II")
    boleta.agregar_nota("Curso A", 10.0, 4)
    boleta.agregar_nota("Curso B", 08.0, 4)
    assert boleta.promedio_ponderado == 9.0
    assert boleta.estado_final == "DESAPROBADO"


def test_template_method_generacion_archivos(tmp_path, registro_configurado, notas_ejemplo):
    """Verifica que el template method procese y cree los archivos en disco."""
    for fmt, ext in [("txt", ".txt"), ("csv", ".csv"), ("html", ".html")]:
        gen = registro_configurado.crear(fmt)
        contenido, ruta = gen.generar_y_enviar(
            estudiante="Ana Laura Ramos",
            codigo="2025110",
            semestre="2026-II",
            notas=notas_ejemplo,
            directorio_salida=tmp_path
        )
        assert ruta.exists()
        assert ruta.suffix == ext
        assert len(contenido) > 50
        assert "Ana Laura Ramos" in contenido


def test_formato_no_registrado_lanza_error(registro_configurado):
    """Verifica que solicitar un formato desconocido genere ValueError descriptivo."""
    with pytest.raises(ValueError, match="Formato de boleta no soportado: 'pdf'"):
        registro_configurado.crear("pdf")


def test_demostracion_ocp_con_nuevo_formato(registro_configurado):
    """Demuestra OCP: se añade formato JSON sin modificar ninguna clase existente."""
    import json

    class BoletaJSON(BoletaNotas):
        @property
        def extension(self) -> str:
            return ".json"

        @property
        def formato(self) -> str:
            return "JSON"

        def generar(self) -> str:
            return json.dumps({
                "estudiante": self.estudiante,
                "codigo": self.codigo,
                "semestre": self.semestre,
                "creditos_totales": self.total_creditos,
                "promedio": self.promedio_ponderado,
                "estado": self.estado_final
            })

    class GeneradorBoletaJSON(GeneradorBoleta):
        def crear_boleta(self) -> BoletaNotas:
            return BoletaJSON()

    # Registro dinámico
    registro_configurado.registrar("json", GeneradorBoletaJSON)
    gen_json = registro_configurado.crear("json")
    assert isinstance(gen_json.crear_boleta(), BoletaJSON)

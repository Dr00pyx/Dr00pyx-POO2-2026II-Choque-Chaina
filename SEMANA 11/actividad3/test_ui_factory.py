"""
Pruebas Unitarias para el patrón Abstract Factory (UI Multiplataforma).
Verifica:
1. Consistencia de familias: cada fábrica debe instanciar productos de su propia suite.
2. Comportamiento agnóstico del cliente FormularioBusqueda ante distintas familias.
3. Testeabilidad con Mocks para verificar DIP.
"""
from unittest.mock import MagicMock
import pytest
from ui_abstract_factory import (
    UIFactory,
    UIFactoryTkinter,
    UIFactoryPyQt5,
    VentanaPrincipal,
    VentanaTkinter,
    VentanaPyQt,
    MenuNavegacion,
    MenuTkinter,
    MenuPyQt,
    TablaResultados,
    TablaResultadosTkinter,
    TablaResultadosPyQt,
    FormularioBusqueda,
)


def test_consistencia_familia_tkinter():
    factory = UIFactoryTkinter()
    ventana = factory.crear_ventana()
    menu = factory.crear_menu()
    tabla = factory.crear_tabla()

    assert isinstance(ventana, VentanaTkinter)
    assert isinstance(menu, MenuTkinter)
    assert isinstance(tabla, TablaResultadosTkinter)
    assert "Tkinter" in factory.nombre_familia


def test_consistencia_familia_pyqt5():
    factory = UIFactoryPyQt5()
    ventana = factory.crear_ventana()
    menu = factory.crear_menu()
    tabla = factory.crear_tabla()

    assert isinstance(ventana, VentanaPyQt)
    assert isinstance(menu, MenuPyQt)
    assert isinstance(tabla, TablaResultadosPyQt)
    assert "PyQt5" in factory.nombre_familia


def test_formulario_busqueda_con_tkinter():
    factory = UIFactoryTkinter()
    form = FormularioBusqueda(factory)
    resultado = form.construir_interfaz(
        criterio="POO II",
        registros=[{"codigo": "2023001", "estudiante": "Juan Gomez"}]
    )

    assert "Tkinter" in resultado["familia"]
    assert "[Tkinter] root = tk.Tk()" in resultado["render_ventana"]
    assert "[Tkinter] menu_bar" in resultado["render_menu"]
    assert "tree.heading('Código'" in resultado["render_tabla"]


def test_formulario_busqueda_con_pyqt5():
    factory = UIFactoryPyQt5()
    form = FormularioBusqueda(factory)
    resultado = form.construir_interfaz(
        criterio="Algoritmos",
        registros=[{"codigo": "2023002", "estudiante": "Sara Silva"}]
    )

    assert "PyQt5" in resultado["familia"]
    assert "[PyQt5] main_window = QMainWindow()" in resultado["render_ventana"]
    assert "[PyQt5] menu_bar" in resultado["render_menu"]
    assert "table.setHorizontalHeaderLabels" in resultado["render_tabla"]


def test_cliente_con_mock_factory():
    """Demuestra la testeabilidad pura del cliente aislando las fábricas reales con Mock."""
    mock_factory = MagicMock(spec=UIFactory)
    mock_ventana = MagicMock(spec=VentanaPrincipal)
    mock_menu = MagicMock(spec=MenuNavegacion)
    mock_tabla = MagicMock(spec=TablaResultados)

    mock_factory.crear_ventana.return_value = mock_ventana
    mock_factory.crear_menu.return_value = mock_menu
    mock_factory.crear_tabla.return_value = mock_tabla
    mock_factory.nombre_familia = "MockSuite"

    form = FormularioBusqueda(mock_factory)
    form.construir_interfaz("Test", [{"codigo": "001"}])

    mock_ventana.configurar.assert_called_once()
    assert mock_menu.agregar_opcion.call_count == 3
    mock_tabla.set_columnas.assert_called_once()
    mock_tabla.agregar_fila.assert_called_once()

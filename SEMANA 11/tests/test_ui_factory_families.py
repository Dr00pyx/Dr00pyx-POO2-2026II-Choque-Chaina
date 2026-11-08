"""
Pruebas Unitarias para Abstract Factory (Capa UI).
Verifica que las familias de productos se instancien de manera consistente.
"""
from unittest.mock import MagicMock
import pytest
from ui_factory import (
    UIFactoryTkinter,
    UIFactoryPyQt5,
    VentanaTkinter,
    VentanaPyQt,
    MenuTkinter,
    MenuPyQt,
    TablaTkinter,
    TablaPyQt,
    VistaMatriculaGUI,
)
from factory.repositorio import RepositorioEstudiantes
from factory.modelo import Estudiante


def test_fabrica_tkinter_crea_familia_completa():
    factory = UIFactoryTkinter()
    assert isinstance(factory.crear_ventana(), VentanaTkinter)
    assert isinstance(factory.crear_menu(), MenuTkinter)
    assert isinstance(factory.crear_tabla(), TablaTkinter)


def test_fabrica_pyqt_crea_familia_completa():
    factory = UIFactoryPyQt5()
    assert isinstance(factory.crear_ventana(), VentanaPyQt)
    assert isinstance(factory.crear_menu(), MenuPyQt)
    assert isinstance(factory.crear_tabla(), TablaPyQt)


def test_vista_gui_con_mock_repositorio():
    mock_repo = MagicMock(spec=RepositorioEstudiantes)
    mock_repo.listar_todos.return_value = [
        Estudiante(codigo="2023001", nombre="Ana Test", carrera="Sistemas", promedio=16.5),
        Estudiante(codigo="2023002", nombre="Beto Test", carrera="Sistemas", promedio=14.0)
    ]
    mock_repo.tipo_almacenamiento = "MockStorage"

    gui = VistaMatriculaGUI(factory=UIFactoryTkinter(), repositorio=mock_repo)
    total = gui.sincronizar_tabla_con_repositorio()

    assert total == 2
    mock_repo.listar_todos.assert_called_once()
    render = gui.renderizar_completo()
    assert "Tkinter" in render["toolkit"]
    assert "Ana Test" not in render["menu"]  # Menu has options, table has data

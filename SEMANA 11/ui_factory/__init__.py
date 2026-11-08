"""
Módulo Abstract Factory para componentes de la interfaz de usuario.
"""
from .ui_interfaces import UIFactory, VentanaPrincipal, MenuNavegacion, TablaResultados
from .tkinter_factory import UIFactoryTkinter, VentanaTkinter, MenuTkinter, TablaTkinter
from .pyqt_factory import UIFactoryPyQt5, VentanaPyQt, MenuPyQt, TablaPyQt
from .cliente_gui import VistaMatriculaGUI

__all__ = [
    "UIFactory",
    "VentanaPrincipal",
    "MenuNavegacion",
    "TablaResultados",
    "UIFactoryTkinter",
    "VentanaTkinter",
    "MenuTkinter",
    "TablaTkinter",
    "UIFactoryPyQt5",
    "VentanaPyQt",
    "MenuPyQt",
    "TablaPyQt",
    "VistaMatriculaGUI",
]

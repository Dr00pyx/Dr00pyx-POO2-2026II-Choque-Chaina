"""
Familia Concreta: Componentes y Fábrica PyQt5.
"""
from typing import List, Tuple
from .ui_interfaces import UIFactory, VentanaPrincipal, MenuNavegacion, TablaResultados


class VentanaPyQt(VentanaPrincipal):
    def __init__(self) -> None:
        self.titulo = "Ventana PyQt5"
        self.dimensiones = (800, 600)

    def configurar(self, titulo: str, ancho: int, alto: int) -> None:
        self.titulo = titulo
        self.dimensiones = (ancho, alto)

    def mostrar(self) -> str:
        return f"[PyQt5] QMainWindow(title='{self.titulo}', size={self.dimensiones})"


class MenuPyQt(MenuNavegacion):
    def __init__(self) -> None:
        self.acciones: List[Tuple[str, str]] = []

    def agregar_comando(self, etiqueta: str, callback_nombre: str) -> None:
        self.acciones.append((etiqueta, callback_nombre))

    def renderizar(self) -> str:
        acts = ", ".join([f"QAction('{lbl}', triggered={cb})" for lbl, cb in self.acciones])
        return f"[PyQt5] QMenuBar() -> [{acts}]"


class TablaPyQt(TablaResultados):
    def __init__(self) -> None:
        self.cabeceras: List[str] = []
        self.filas: List[List[str]] = []

    def definir_cabeceras(self, columnas: List[str]) -> None:
        self.cabeceras = list(columnas)

    def insertar_fila(self, valores: List[str]) -> None:
        self.filas.append(list(valores))

    def renderizar(self) -> str:
        return f"[PyQt5] QTableWidget(headers={self.cabeceras}, rows={len(self.filas)})"


class UIFactoryPyQt5(UIFactory):
    def crear_ventana(self) -> VentanaPrincipal:
        return VentanaPyQt()

    def crear_menu(self) -> MenuNavegacion:
        return MenuPyQt()

    def crear_tabla(self) -> TablaResultados:
        return TablaPyQt()

    @property
    def nombre_toolkit(self) -> str:
        return "PyQt5 Modern Desktop"

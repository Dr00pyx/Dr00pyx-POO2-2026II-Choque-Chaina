"""
Familia Concreta: Componentes y Fábrica Tkinter.
"""
from typing import List, Tuple
from .ui_interfaces import UIFactory, VentanaPrincipal, MenuNavegacion, TablaResultados


class VentanaTkinter(VentanaPrincipal):
    def __init__(self) -> None:
        self.titulo = "Ventana Tkinter"
        self.dimensiones = "800x600"

    def configurar(self, titulo: str, ancho: int, alto: int) -> None:
        self.titulo = titulo
        self.dimensiones = f"{ancho}x{alto}"

    def mostrar(self) -> str:
        return f"[Tkinter] root = tk.Tk(); root.title('{self.titulo}'); root.geometry('{self.dimensiones}');"


class MenuTkinter(MenuNavegacion):
    def __init__(self) -> None:
        self.items: List[Tuple[str, str]] = []

    def agregar_comando(self, etiqueta: str, callback_nombre: str) -> None:
        self.items.append((etiqueta, callback_nombre))

    def renderizar(self) -> str:
        ops = ", ".join([f"'{lbl}': {cb}" for lbl, cb in self.items])
        return f"[Tkinter] Menu(root) con comandos: [{ops}]"


class TablaTkinter(TablaResultados):
    def __init__(self) -> None:
        self.columnas: List[str] = []
        self.filas: List[List[str]] = []

    def definir_cabeceras(self, columnas: List[str]) -> None:
        self.columnas = list(columnas)

    def insertar_fila(self, valores: List[str]) -> None:
        self.filas.append(list(valores))

    def renderizar(self) -> str:
        return f"[Tkinter] ttk.Treeview columnas={self.columnas} (Total filas: {len(self.filas)})"


class UIFactoryTkinter(UIFactory):
    def crear_ventana(self) -> VentanaPrincipal:
        return VentanaTkinter()

    def crear_menu(self) -> MenuNavegacion:
        return MenuTkinter()

    def crear_tabla(self) -> TablaResultados:
        return TablaTkinter()

    @property
    def nombre_toolkit(self) -> str:
        return "Tkinter Standard Desktop"

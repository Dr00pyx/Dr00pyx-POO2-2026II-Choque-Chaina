"""
Interfaces de Abstract Factory y Productos Abstractos para la GUI del Proyecto Final.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple


class VentanaPrincipal(ABC):
    """Producto Abstracto: Ventana de la interfaz."""
    @abstractmethod
    def configurar(self, titulo: str, ancho: int, alto: int) -> None:
        pass

    @abstractmethod
    def mostrar(self) -> str:
        pass


class MenuNavegacion(ABC):
    """Producto Abstracto: Menú de acciones."""
    @abstractmethod
    def agregar_comando(self, etiqueta: str, callback_nombre: str) -> None:
        pass

    @abstractmethod
    def renderizar(self) -> str:
        pass


class TablaResultados(ABC):
    """Producto Abstracto: Tabla o vista tabular de registros."""
    @abstractmethod
    def definir_cabeceras(self, columnas: List[str]) -> None:
        pass

    @abstractmethod
    def insertar_fila(self, valores: List[str]) -> None:
        pass

    @abstractmethod
    def renderizar(self) -> str:
        pass


class UIFactory(ABC):
    """Fábrica Abstracta para creación de familias completas de componentes UI."""

    @abstractmethod
    def crear_ventana(self) -> VentanaPrincipal:
        pass

    @abstractmethod
    def crear_menu(self) -> MenuNavegacion:
        pass

    @abstractmethod
    def crear_tabla(self) -> TablaResultados:
        pass

    @property
    @abstractmethod
    def nombre_toolkit(self) -> str:
        pass

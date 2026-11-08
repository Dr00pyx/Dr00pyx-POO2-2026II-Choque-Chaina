"""
Actividad 3: Patrón Abstract Factory - UI Multiplataforma (Tkinter y PyQt5)
Permite construir interfaces gráficas consistentes sin acoplar el código cliente
a un framework de ventanas específico.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List, Dict


# ==============================================================================
# 1. PRODUCTOS ABSTRACTOS
# ==============================================================================

class VentanaPrincipal(ABC):
    """Producto abstracto: Ventana contenedora principal."""
    def __init__(self) -> None:
        self.titulo: str = ""
        self.ancho: int = 800
        self.alto: int = 600
        self.componentes: List[str] = []

    @abstractmethod
    def configurar(self, titulo: str, ancho: int, alto: int) -> None:
        pass

    @abstractmethod
    def mostrar(self) -> str:
        """Simula el bucle de renderizado / visualización en pantalla."""
        pass


class MenuNavegacion(ABC):
    """Producto abstracto: Barra o menú de navegación de la interfaz."""
    def __init__(self) -> None:
        self.opciones: List[tuple[str, str]] = []

    def agregar_opcion(self, etiqueta: str, comando: str) -> None:
        self.opciones.append((etiqueta, comando))

    @abstractmethod
    def renderizar(self) -> str:
        pass


class TablaResultados(ABC):
    """Producto abstracto: Componente de cuadrícula o tabla para listar registros."""
    def __init__(self) -> None:
        self.columnas: List[str] = []
        self.filas: List[List[str]] = []

    def set_columnas(self, columnas: List[str]) -> None:
        self.columnas = list(columnas)

    def agregar_fila(self, valores: List[str]) -> None:
        self.filas.append(list(valores))

    @abstractmethod
    def renderizar(self) -> str:
        pass


# ==============================================================================
# 2. PRODUCTOS CONCRETOS — FAMILIA TKINTER
# ==============================================================================

class VentanaTkinter(VentanaPrincipal):
    def configurar(self, titulo: str, ancho: int, alto: int) -> None:
        self.titulo = titulo
        self.ancho = ancho
        self.alto = alto

    def mostrar(self) -> str:
        return (
            f"[Tkinter] root = tk.Tk()\n"
            f"[Tkinter] root.title('{self.titulo}')\n"
            f"[Tkinter] root.geometry('{self.ancho}x{self.alto}')\n"
            f"[Tkinter] ttk.Style().theme_use('clam')\n"
            f"[Tkinter] root.mainloop()"
        )


class MenuTkinter(MenuNavegacion):
    def renderizar(self) -> str:
        lineas = ["[Tkinter] menu_bar = tk.Menu(root)"]
        for label, cmd in self.opciones:
            lineas.append(f"[Tkinter] menu_bar.add_command(label='{label}', command={cmd})")
        lineas.append("[Tkinter] root.config(menu=menu_bar)")
        return "\n".join(lineas)


class TablaResultadosTkinter(TablaResultados):
    def renderizar(self) -> str:
        cols_repr = tuple(self.columnas)
        lineas = [
            f"[Tkinter] tree = ttk.Treeview(root, columns={cols_repr}, show='headings')",
        ]
        for col in self.columnas:
            lineas.append(f"[Tkinter] tree.heading('{col}', text='{col}')")
        for idx, fila in enumerate(self.filas):
            lineas.append(f"[Tkinter] tree.insert('', 'end', iid='item_{idx}', values={tuple(fila)})")
        return "\n".join(lineas)


# ==============================================================================
# 3. PRODUCTOS CONCRETOS — FAMILIA PYQT5
# ==============================================================================

class VentanaPyQt(VentanaPrincipal):
    def configurar(self, titulo: str, ancho: int, alto: int) -> None:
        self.titulo = titulo
        self.ancho = ancho
        self.alto = alto

    def mostrar(self) -> str:
        return (
            f"[PyQt5] app = QApplication(sys.argv)\n"
            f"[PyQt5] main_window = QMainWindow()\n"
            f"[PyQt5] main_window.setWindowTitle('{self.titulo}')\n"
            f"[PyQt5] main_window.resize({self.ancho}, {self.alto})\n"
            f"[PyQt5] main_window.show()\n"
            f"[PyQt5] sys.exit(app.exec_())"
        )


class MenuPyQt(MenuNavegacion):
    def renderizar(self) -> str:
        lineas = [
            "[PyQt5] menu_bar = main_window.menuBar()",
            "[PyQt5] menu_archivo = menu_bar.addMenu('&Acciones')"
        ]
        for label, cmd in self.opciones:
            lineas.append(f"[PyQt5] act = menu_archivo.addAction('{label}')")
            lineas.append(f"[PyQt5] act.triggered.connect({cmd})")
        return "\n".join(lineas)


class TablaResultadosPyQt(TablaResultados):
    def renderizar(self) -> str:
        lineas = [
            f"[PyQt5] table = QTableWidget({len(self.filas)}, {len(self.columnas)})",
            f"[PyQt5] table.setHorizontalHeaderLabels({self.columnas})"
        ]
        for r, fila in enumerate(self.filas):
            for c, val in enumerate(fila):
                lineas.append(f"[PyQt5] table.setItem({r}, {c}, QTableWidgetItem('{val}'))")
        return "\n".join(lineas)


# ==============================================================================
# 4. FÁBRICA ABSTRACTA Y FÁBRICAS CONCRETAS
# ==============================================================================

class UIFactory(ABC):
    """Interfaz de la Fábrica Abstracta para familias de widgets UI."""

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
    def nombre_familia(self) -> str:
        pass


class UIFactoryTkinter(UIFactory):
    """Fábrica Concreta para la suite gráfica Tkinter."""

    def crear_ventana(self) -> VentanaPrincipal:
        return VentanaTkinter()

    def crear_menu(self) -> MenuNavegacion:
        return MenuTkinter()

    def crear_tabla(self) -> TablaResultados:
        return TablaResultadosTkinter()

    @property
    def nombre_familia(self) -> str:
        return "Tkinter Standard Desktop"


class UIFactoryPyQt5(UIFactory):
    """Fábrica Concreta para la suite gráfica PyQt5."""

    def crear_ventana(self) -> VentanaPrincipal:
        return VentanaPyQt()

    def crear_menu(self) -> MenuNavegacion:
        return MenuPyQt()

    def crear_tabla(self) -> TablaResultados:
        return TablaResultadosPyQt()

    @property
    def nombre_familia(self) -> str:
        return "PyQt5 Modern Desktop"


# ==============================================================================
# 5. CÓDIGO CLIENTE: FormularioBusqueda
# ==============================================================================

class FormularioBusqueda:
    """
    Cliente de alto nivel.
    Construye y gestiona el flujo de interfaz de usuario interactuando
    EXCLUSIVAMENTE con la interfaz UIFactory y productos abstractos.
    Desconoce completamente si se utiliza Tkinter o PyQt5.
    """

    def __init__(self, factory: UIFactory) -> None:
        self.factory = factory
        # Instanciación desacoplada usando la fábrica abstracta
        self.ventana: VentanaPrincipal = self.factory.crear_ventana()
        self.menu: MenuNavegacion = self.factory.crear_menu()
        self.tabla: TablaResultados = self.factory.crear_tabla()

    def construir_interfaz(self, criterio: str, registros: List[Dict[str, str]]) -> Dict[str, str]:
        # 1. Configurar ventana
        self.ventana.configurar(
            titulo=f"Sistema Académico UNAP - Búsqueda: '{criterio}'",
            ancho=900,
            alto=600
        )

        # 2. Configurar opciones del menú
        self.menu.agregar_opcion("Buscar", "on_buscar_click")
        self.menu.agregar_opcion("Exportar PDF", "on_exportar_pdf")
        self.menu.agregar_opcion("Cerrar", "on_cerrar_click")

        # 3. Configurar tabla de resultados
        columnas = ["Código", "Estudiante", "Carrera", "Promedio", "Condición"]
        self.tabla.set_columnas(columnas)
        for reg in registros:
            self.tabla.agregar_fila([
                reg.get("codigo", ""),
                reg.get("estudiante", ""),
                reg.get("carrera", "Ing. de Sistemas"),
                str(reg.get("promedio", "0.0")),
                reg.get("condicion", "Regular")
            ])

        # 4. Generar especificación visual
        return {
            "familia": self.factory.nombre_familia,
            "render_menu": self.menu.renderizar(),
            "render_tabla": self.tabla.renderizar(),
            "render_ventana": self.ventana.mostrar(),
        }


if __name__ == "__main__":
    datos_prueba = [
        {"codigo": "2023001", "estudiante": "Mario Vargas", "carrera": "Sistemas", "promedio": "16.8", "condicion": "Invicto"},
        {"codigo": "2023002", "estudiante": "Lucia Flores", "carrera": "Sistemas", "promedio": "17.4", "condicion": "Tercio Sup"},
    ]

    print("=" * 60)
    print("PROBANDO CON FAMILIA TKINTER:")
    form_tk = FormularioBusqueda(UIFactoryTkinter())
    res_tk = form_tk.construir_interfaz("Sistemas", datos_prueba)
    print(res_tk["render_ventana"])
    print(res_tk["render_tabla"])

    print("\n" + "=" * 60)
    print("PROBANDO CON FAMILIA PYQT5:")
    form_qt = FormularioBusqueda(UIFactoryPyQt5())
    res_qt = form_qt.construir_interfaz("Sistemas", datos_prueba)
    print(res_qt["render_ventana"])
    print(res_qt["render_tabla"])

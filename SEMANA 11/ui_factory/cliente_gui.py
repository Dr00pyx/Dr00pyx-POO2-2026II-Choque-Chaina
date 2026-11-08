"""
Cliente GUI: VistaMatriculaGUI.
Orquesta los componentes visuales mediante Abstract Factory e interactúa
con el Repositorio de datos y el Logger mediante Inversión de Dependencias (DIP).
"""
from typing import List
from .ui_interfaces import UIFactory, VentanaPrincipal, MenuNavegacion, TablaResultados
from factory.modelo import Estudiante
from factory.repositorio import RepositorioEstudiantes
from singleton.logger import Logger


class VistaMatriculaGUI:
    """
    Controlador/Vista del cliente.
    Totalmente agnóstico al toolkit de interfaz gráfica y al medio de almacenamiento.
    """
    def __init__(self, factory: UIFactory, repositorio: RepositorioEstudiantes) -> None:
        self.factory = factory
        self.repositorio = repositorio
        self.logger = Logger()

        # Creación consistente mediante la Abstract Factory
        self.ventana: VentanaPrincipal = self.factory.crear_ventana()
        self.menu: MenuNavegacion = self.factory.crear_menu()
        self.tabla: TablaResultados = self.factory.crear_tabla()

        self._configurar_interfaz()

    def _configurar_interfaz(self) -> None:
        self.ventana.configurar("Sistema de Matrícula y Notas - UNAP", 960, 640)
        self.menu.agregar_comando("Registrar Estudiante", "on_registrar")
        self.menu.agregar_comando("Cargar Lista", "on_recargar")
        self.menu.agregar_comando("Salir", "on_salir")
        self.tabla.definir_cabeceras(["Código", "Nombre", "Carrera", "Promedio", "Semestre"])

    def sincronizar_tabla_con_repositorio(self) -> int:
        estudiantes: List[Estudiante] = self.repositorio.listar_todos()
        self.logger.info("GUI", f"Cargando {len(estudiantes)} registros desde {self.repositorio.tipo_almacenamiento}")
        
        for est in estudiantes:
            self.tabla.insertar_fila([
                est.codigo,
                est.nombre,
                est.carrera,
                f"{est.promedio:.2f}",
                est.semestre
            ])
        return len(estudiantes)

    def renderizar_completo(self) -> dict:
        return {
            "toolkit": self.factory.nombre_toolkit,
            "ventana": self.ventana.mostrar(),
            "menu": self.menu.renderizar(),
            "tabla": self.tabla.renderizar()
        }

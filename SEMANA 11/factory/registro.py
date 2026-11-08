"""
Registro Dinámico de Fábricas de Repositorios (Registry + Factory Method).
Desacopla la selección del medio de almacenamiento según el entorno (config).
"""
from typing import Callable, Dict
from .repositorio import RepositorioEstudiantes
from .creadores import (
    CreadorRepositorio,
    CreadorRepoMemoria,
    CreadorRepoArchivo,
    CreadorRepoSQLite
)


class RegistroFabricaRepositorios:
    """
    Registro desacoplado para resolver repositorios dinámicamente.
    Cumple con el principio Open/Closed (OCP).
    """

    def __init__(self) -> None:
        self._creadores: Dict[str, Callable[[], CreadorRepositorio]] = {}
        self._registrar_predeterminados()

    def _registrar_predeterminados(self) -> None:
        self.registrar("memoria", lambda: CreadorRepoMemoria())
        self.registrar("archivo", lambda: CreadorRepoArchivo("estudiantes.json"))
        self.registrar("sqlite", lambda: CreadorRepoSQLite("academico_unap.db"))

    def registrar(self, clave: str, factory_callable: Callable[[], CreadorRepositorio]) -> None:
        self._creadores[clave.lower().strip()] = factory_callable

    def obtener_creador(self, clave: str) -> CreadorRepositorio:
        c = clave.lower().strip()
        if c not in self._creadores:
            validos = ", ".join(self._creadores.keys())
            raise ValueError(f"Medio de repositorio '{clave}' no registrado. Opciones disponibles: [{validos}]")
        return self._creadores[c]()

    def fabricar(self, clave: str) -> RepositorioEstudiantes:
        creador = self.obtener_creador(clave)
        return creador.crear_repositorio()

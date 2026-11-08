"""
Fábrica de Repositorios mediante Factory Method.
Define el Creador Base abstracto y los Creadores Concretos.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from .repositorio import RepositorioEstudiantes
from .repo_memoria import RepositorioMemoria
from .repo_archivo import RepositorioArchivoJSON
from .repo_bd import RepositorioSQLite


class CreadorRepositorio(ABC):
    """
    Creador Base (Creator) del patrón Factory Method.
    Declara el método fábrica que devuelve un RepositorioEstudiantes.
    """

    @abstractmethod
    def crear_repositorio(self) -> RepositorioEstudiantes:
        """FACTORY METHOD: cada creador concreto instancia el tipo correspondiente."""
        pass

    def inicializar_con_semillas(self, estudiantes: list) -> RepositorioEstudiantes:
        """Template Method opcional que usa el producto creado."""
        repo = self.crear_repositorio()
        for e in estudiantes:
            repo.guardar(e)
        return repo


class CreadorRepoMemoria(CreadorRepositorio):
    """Creador concreto para persistencia en memoria."""
    def crear_repositorio(self) -> RepositorioEstudiantes:
        return RepositorioMemoria()


class CreadorRepoArchivo(CreadorRepositorio):
    """Creador concreto para persistencia en archivo JSON."""
    def __init__(self, ruta_archivo: str = "estudiantes.json") -> None:
        self.ruta_archivo = ruta_archivo

    def crear_repositorio(self) -> RepositorioEstudiantes:
        return RepositorioArchivoJSON(self.ruta_archivo)


class CreadorRepoSQLite(CreadorRepositorio):
    """Creador concreto para persistencia en SQLite."""
    def __init__(self, ruta_db: str = "academico_unap.db") -> None:
        self.ruta_db = ruta_db

    def crear_repositorio(self) -> RepositorioEstudiantes:
        return RepositorioSQLite(self.ruta_db)

"""
Módulo Factory Method para creación desacoplada de la capa de persistencia.
"""
from .modelo import Estudiante
from .repositorio import RepositorioEstudiantes
from .repo_memoria import RepositorioMemoria
from .repo_archivo import RepositorioArchivoJSON
from .repo_bd import RepositorioSQLite
from .creadores import (
    CreadorRepositorio,
    CreadorRepoMemoria,
    CreadorRepoArchivo,
    CreadorRepoSQLite
)
from .registro import RegistroFabricaRepositorios

__all__ = [
    "Estudiante",
    "RepositorioEstudiantes",
    "RepositorioMemoria",
    "RepositorioArchivoJSON",
    "RepositorioSQLite",
    "CreadorRepositorio",
    "CreadorRepoMemoria",
    "CreadorRepoArchivo",
    "CreadorRepoSQLite",
    "RegistroFabricaRepositorios",
]

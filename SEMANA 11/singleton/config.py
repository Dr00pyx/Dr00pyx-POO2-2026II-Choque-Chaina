"""
Singleton de Configuración del Sistema (Python 3.12+).
Thread-safe mediante Metaclase.
"""
from __future__ import annotations
from enum import Enum
import os
from pathlib import Path
from threading import Lock
from typing import Any, Dict


class SingletonMeta(type):
    """Metaclase que asegura una única instancia por tipo de clase de forma thread-safe."""
    _instancias: Dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instancias:
                instancia = super().__call__(*args, **kwargs)
                cls._instancias[cls] = instancia
        return cls._instancias[cls]

    @classmethod
    def reset(cls) -> None:
        with cls._lock:
            cls._instancias.clear()


class EntornoApp(Enum):
    DESARROLLO = "desarrollo"
    TESTING = "testing"
    PRODUCCION = "produccion"


class TipoRepositorio(Enum):
    MEMORIA = "memoria"
    ARCHIVO = "archivo"
    SQLITE = "sqlite"


class TipoUI(Enum):
    TKINTER = "tkinter"
    PYQT5 = "pyqt5"


class ConfiguracionSistema(metaclass=SingletonMeta):
    """
    Parámetros centrales de ejecución del sistema académico.
    """
    def __init__(self, ruta_env: str | Path | None = None) -> None:
        if hasattr(self, "_inicializado") and self._inicializado:
            return

        self._valores: dict[str, str] = {
            "ENTORNO": "desarrollo",
            "TIPO_REPOSITORIO": "memoria",
            "TIPO_UI": "tkinter",
            "RUTA_DB": "academico_unap.db",
            "RUTA_JSON": "estudiantes.json",
            "NIVEL_LOG": "INFO",
            "RUTA_LOG": "sistema_academico.log",
        }

        if ruta_env is not None:
            self._cargar_archivo(Path(ruta_env))
        else:
            env_local = Path(".env")
            if env_local.exists():
                self._cargar_archivo(env_local)

        self._inicializado = True

    def _cargar_archivo(self, ruta: Path) -> None:
        if not ruta.exists():
            return
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea and not linea.startswith("#") and "=" in linea:
                    k, v = linea.split("=", 1)
                    self._valores[k.strip().upper()] = v.strip()

    def set_override(self, clave: str, valor: str) -> None:
        """Permite a pruebas unitarias o inyección dinámica sobreescribir valores."""
        self._valores[clave.upper()] = valor

    @property
    def entorno(self) -> EntornoApp:
        val = self._valores.get("ENTORNO", "desarrollo").lower()
        try:
            return EntornoApp(val)
        except ValueError:
            return EntornoApp.DESARROLLO

    @property
    def tipo_repositorio(self) -> TipoRepositorio:
        val = self._valores.get("TIPO_REPOSITORIO", "memoria").lower()
        try:
            return TipoRepositorio(val)
        except ValueError:
            return TipoRepositorio.MEMORIA

    @property
    def tipo_ui(self) -> TipoUI:
        val = self._valores.get("TIPO_UI", "tkinter").lower()
        try:
            return TipoUI(val)
        except ValueError:
            return TipoUI.TKINTER

    @property
    def ruta_db(self) -> str:
        return self._valores.get("RUTA_DB", "academico_unap.db")

    @property
    def ruta_json(self) -> str:
        return self._valores.get("RUTA_JSON", "estudiantes.json")

    @property
    def ruta_log(self) -> str:
        return self._valores.get("RUTA_LOG", "sistema_academico.log")

    @property
    def nivel_log(self) -> str:
        return self._valores.get("NIVEL_LOG", "INFO").upper()

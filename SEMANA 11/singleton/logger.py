"""
Singleton de Logging Centralizado (Python 3.12+).
Thread-safe, con soporte para consola y archivo.
"""
from __future__ import annotations
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from threading import Lock
from typing import List
from .config import SingletonMeta


class NivelLog(Enum):
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40


class Logger(metaclass=SingletonMeta):
    """
    Logger centralizado de la aplicación.
    Garantiza que todos los módulos compartan el mismo canal de auditoría y traza.
    """
    def __init__(self, ruta_archivo: str = "sistema_academico.log", nivel_minimo: NivelLog = NivelLog.INFO) -> None:
        if hasattr(self, "_inicializado") and self._inicializado:
            return

        self.ruta_archivo = Path(ruta_archivo)
        self.nivel_minimo = nivel_minimo
        self._lock = Lock()
        self._entradas_memoria: List[str] = []
        self._inicializado = True

    def set_nivel_minimo(self, nivel: NivelLog) -> None:
        with self._lock:
            self.nivel_minimo = nivel

    def log(self, nivel: NivelLog, modulo: str, mensaje: str) -> str:
        if nivel.value < self.nivel_minimo.value:
            return ""

        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        entrada = f"[{ahora}] [{nivel.name:<5}] [{modulo}] {mensaje}"

        with self._lock:
            self._entradas_memoria.append(entrada)
            print(entrada)
            try:
                with open(self.ruta_archivo, "a", encoding="utf-8") as f:
                    f.write(entrada + "\n")
            except Exception:
                # Si no se tiene permiso de escritura a archivo local, el log persiste en memoria
                pass

        return entrada

    def debug(self, modulo: str, mensaje: str) -> str:
        return self.log(NivelLog.DEBUG, modulo, mensaje)

    def info(self, modulo: str, mensaje: str) -> str:
        return self.log(NivelLog.INFO, modulo, mensaje)

    def warn(self, modulo: str, mensaje: str) -> str:
        return self.log(NivelLog.WARN, modulo, mensaje)

    def error(self, modulo: str, mensaje: str) -> str:
        return self.log(NivelLog.ERROR, modulo, mensaje)

    @property
    def historial(self) -> List[str]:
        with self._lock:
            return list(self._entradas_memoria)

    def limpiar_historial(self) -> None:
        with self._lock:
            self._entradas_memoria.clear()

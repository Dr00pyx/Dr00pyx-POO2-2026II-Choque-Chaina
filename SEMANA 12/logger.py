"""
Módulo de Logging Centralizado.
Proporciona registro en memoria y salida en consola con formato [LOG] HH:MM:SS <mensaje>.
Compatible tanto con importación directa como objeto Logger.
"""
from datetime import datetime
from threading import Lock
from typing import List


class _LoggerCentral:
    _instancia = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instancia is None:
                cls._instancia = super().__new__(cls)
                cls._instancia._entradas = []
                cls._instancia._mutex = Lock()
        return cls._instancia

    def log(self, mensaje: str) -> str:
        ahora = datetime.now().strftime("%H:%M:%S")
        linea = f"[LOG] {ahora} {mensaje}"
        with self._mutex:
            self._entradas.append(linea)
        print(linea)
        return linea

    def get_entradas(self) -> List[str]:
        with self._mutex:
            return list(self._entradas)

    def limpiar(self) -> None:
        with self._mutex:
            self._entradas.clear()


_instancia_logger = _LoggerCentral()


def log(mensaje: str) -> str:
    """Registra un mensaje de log con timestamp HH:MM:SS."""
    return _instancia_logger.log(mensaje)


def get_entradas() -> List[str]:
    """Retorna todas las entradas registradas en memoria."""
    return _instancia_logger.get_entradas()


def limpiar() -> None:
    """Limpia las entradas de log acumuladas."""
    _instancia_logger.limpiar()


class Logger:
    """Clase estática / fachada para compatibilidad con llamadas tipo Logger.log()."""
    @staticmethod
    def log(mensaje: str) -> str:
        return _instancia_logger.log(mensaje)

    @staticmethod
    def get_entradas() -> List[str]:
        return _instancia_logger.get_entradas()

    @staticmethod
    def limpiar() -> None:
        _instancia_logger.limpiar()

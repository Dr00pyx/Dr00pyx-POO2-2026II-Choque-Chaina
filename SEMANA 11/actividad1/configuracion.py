"""
Módulo de Configuración Singleton utilizando Metaclase en Python 3.12+
Garantiza instancia única de configuración centralizada en entornos multihilo.
"""
from __future__ import annotations
from pathlib import Path
from threading import Lock
from typing import Any, Dict


class SingletonMeta(type):
    """
    Metaclase thread-safe para implementar el patrón Singleton de forma idiomática en Python.
    Controla la instanciación de clases mediante el método __call__ protegiendo el acceso
    con un Lock reentrante/estándar de subprocesamiento.
    """
    _instancias: Dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instancias:
                instancia = super().__call__(*args, **kwargs)
                cls._instancias[cls] = instancia
        return cls._instancias[cls]

    @classmethod
    def reset_instancias(cls) -> None:
        """Permite limpiar instancias registradas para propósitos de pruebas unitarias."""
        with cls._lock:
            cls._instancias.clear()


class ConfiguracionApp(metaclass=SingletonMeta):
    """
    Gestor de configuración central de la aplicación.
    Carga variables desde un archivo .env simulado y expone propiedades tipadas.
    """
    def __init__(self, ruta_env: str | Path | None = None) -> None:
        # Prevenir reinicialización destructiva si ya fue inicializado
        if hasattr(self, "_inicializado") and self._inicializado:
            return

        self._valores: dict[str, str] = {}
        
        if ruta_env is None:
            # Buscar .env en el directorio actual o en el directorio del script
            ruta_por_defecto = Path(__file__).resolve().parent / ".env"
            self.ruta_env = ruta_por_defecto if ruta_por_defecto.exists() else Path(".env")
        else:
            self.ruta_env = Path(ruta_env)

        self._cargar_env()
        self._inicializado = True

    def _cargar_env(self) -> None:
        """Parsea un archivo .env plano ignorando comentarios y líneas vacías."""
        if not self.ruta_env.exists():
            # Valores predeterminados seguros en caso de no hallar el archivo
            self._valores = {
                "DB_URL": "sqlite:///default.db",
                "MAX_CONEXIONES": "10",
                "AMBIENTE": "desarrollo",
                "DEBUG_MODE": "True",
                "PUERTO_SERVICIO": "8000",
                "TIMEOUT_SEGUNDOS": "15",
                "SECRET_KEY": "default_dev_secret"
            }
            return

        with open(self.ruta_env, "r", encoding="utf-8") as f:
            for linea in f:
                linea_limpia = linea.strip()
                if not linea_limpia or linea_limpia.startswith("#"):
                    continue
                if "=" in linea_limpia:
                    clave, valor = linea_limpia.split("=", 1)
                    self._valores[clave.strip()] = valor.strip()

    def get(self, clave: str, default: Any = None) -> Any:
        return self._valores.get(clave, default)

    def __getitem__(self, clave: str) -> str:
        return self._valores[clave]

    @property
    def db_url(self) -> str:
        return self.get("DB_URL", "sqlite:///default.db")

    @property
    def max_conexiones(self) -> int:
        return int(self.get("MAX_CONEXIONES", 10))

    @property
    def ambiente(self) -> str:
        return self.get("AMBIENTE", "desarrollo")

    @property
    def debug_mode(self) -> bool:
        return self.get("DEBUG_MODE", "False").lower() in ("true", "1", "yes")

    @property
    def puerto_servicio(self) -> int:
        return int(self.get("PUERTO_SERVICIO", 8080))

    @property
    def timeout_segundos(self) -> int:
        return int(self.get("TIMEOUT_SEGUNDOS", 30))

    @property
    def secret_key(self) -> str:
        return self.get("SECRET_KEY", "")


if __name__ == "__main__":
    c1 = ConfiguracionApp()
    c2 = ConfiguracionApp()
    print(f"¿c1 es exactamente c2 en memoria?: {c1 is c2}")
    print(f"ID c1: {id(c1)} | ID c2: {id(c2)}")
    print(f"Ambiente: {c1.ambiente}")
    print(f"DB URL: {c1.db_url}")
    print(f"Max Conexiones: {c1.max_conexiones}")
    print(f"Debug Mode: {c1.debug_mode}")

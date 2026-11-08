"""
Módulo Singleton: Componentes de infraestructura con garantía de instancia única.
Incluye Logger centralizado y Configuración global de la aplicación.
"""
from .logger import Logger, NivelLog
from .config import ConfiguracionSistema, SingletonMeta

__all__ = ["Logger", "NivelLog", "ConfiguracionSistema", "SingletonMeta"]

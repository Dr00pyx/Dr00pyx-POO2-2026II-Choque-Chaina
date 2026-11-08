"""
Pruebas de la capa Singleton (Logger y Configuración).
"""
import concurrent.futures
from singleton.config import ConfiguracionSistema, SingletonMeta
from singleton.logger import Logger, NivelLog


def test_configuracion_singleton_unicidad():
    c1 = ConfiguracionSistema()
    c2 = ConfiguracionSistema()
    assert c1 is c2
    assert id(c1) == id(c2)


def test_logger_singleton_unicidad():
    l1 = Logger()
    l2 = Logger()
    assert l1 is l2
    assert id(l1) == id(l2)


def test_logger_concurrencia_thread_safe():
    logger = Logger()
    logger.limpiar_historial()

    def enviar_log(i):
        logger.info("HiloTest", f"Mensaje hilo {i}")
        return True

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        resultados = list(ex.map(enviar_log, range(20)))

    assert all(resultados)
    assert len(logger.historial) >= 20

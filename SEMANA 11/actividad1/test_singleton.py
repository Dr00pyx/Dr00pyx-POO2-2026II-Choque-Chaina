"""
Pruebas Unitarias para Singleton ConfiguracionApp con pytest y assert.
Verifica:
1. Unicidad de instancia en memoria.
2. Carga correcta de variables de entorno desde .env.
3. Comportamiento thread-safe con acceso concurrente de múltiples hilos.
"""
import concurrent.futures
from pathlib import Path
import pytest
from configuracion import ConfiguracionApp, SingletonMeta


def test_singleton_misma_instancia():
    """Verifica que llamadas sucesivas devuelvan exactamente el mismo objeto."""
    c1 = ConfiguracionApp()
    c2 = ConfiguracionApp()
    
    assert c1 is c2, "Ambas referencias deben apuntar al mismo objeto en memoria"
    assert id(c1) == id(c2), "Los identificadores de memoria deben ser idénticos"


def test_carga_valores_env():
    """Verifica que los valores definidos en .env hayan sido cargados fielmente."""
    cfg = ConfiguracionApp()
    assert cfg.ambiente == "produccion"
    assert cfg.max_conexiones == 25
    assert "matricula_unap" in cfg.db_url
    assert cfg.puerto_servicio == 8080
    assert cfg.timeout_segundos == 30
    assert cfg.debug_mode is False


def test_singleton_thread_safety():
    """Verifica que múltiples hilos concurrentes obtengan exactamente la misma instancia única."""
    instancias = []

    def obtener_instancia():
        inst = ConfiguracionApp()
        return id(inst)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futuros = [executor.submit(obtener_instancia) for _ in range(50)]
        for f in concurrent.futures.as_completed(futuros):
            instancias.append(f.result())

    # Todas las IDs recolectadas deben ser exactamente iguales
    assert len(set(instancias)) == 1, "Debe existir un único ID de instancia entre todos los hilos"


def test_acceso_por_llave_e_inexistente():
    """Verifica acceso indexado por clave y valores por defecto."""
    cfg = ConfiguracionApp()
    assert cfg["AMBIENTE"] == "produccion"
    assert cfg.get("VARIABLE_INEXISTENTE", "fallback") == "fallback"

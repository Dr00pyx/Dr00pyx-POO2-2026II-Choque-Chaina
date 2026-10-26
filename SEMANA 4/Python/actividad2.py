import sys
from abc import ABC, abstractmethod
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ── Abstracciones ──────────────────────────────────────────────────────
class Exportador(ABC):
    @abstractmethod
    def exportar(self, contenido: str, ruta: str) -> None: ...

    @property
    @abstractmethod
    def extension(self) -> str: ...


class Firmador(ABC):
    @abstractmethod
    def firmar(self, ruta: str) -> str:
        """Retorna ruta del archivo firmado."""
        ...


# ── Implementaciones Concretas ─────────────────────────────────────────
class ExportadorCSV(Exportador):
    @property
    def extension(self) -> str:
        return ".csv"

    def exportar(self, contenido: str, ruta: str) -> None:
        print(f"[CSV] Exportando a {ruta}{self.extension}")


class ExportadorJSON(Exportador):
    @property
    def extension(self) -> str:
        return ".json"

    def exportar(self, contenido: str, ruta: str) -> None:
        print(f"[JSON] Exportando a {ruta}{self.extension}")


class FirmadorDigital(Firmador):
    def __init__(self, clave: str):
        self._clave = clave

    def firmar(self, ruta: str) -> str:
        ruta_firmada = ruta + ".signed"
        print(f"[FIRMA] Firmando {ruta} → {ruta_firmada}")
        return ruta_firmada


# ── Generador de Reportes (Inyección de Dependencias) ───────────────────
class GeneradorReporte:
    def __init__(self, exportador: Exportador, firmador: Firmador | None = None):
        self._exportador = exportador
        self._firmador = firmador

    def cambiar_exportador(self, exp: Exportador) -> None:
        self._exportador = exp

    def generar(self, datos: dict, nombre: str) -> str:
        contenido = self._formatear(datos)
        ruta_base = f"reportes/{nombre}"
        self._exportador.exportar(contenido, ruta_base)
        ruta_final = ruta_base + self._exportador.extension
        if self._firmador:
            ruta_final = self._firmador.firmar(ruta_final)
        return ruta_final

    def _formatear(self, datos: dict) -> str:
        return ", ".join(f"{k}={v}" for k, v in datos.items())


# ── Demostración ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    datos_planilla = {"total_personal": 45, "monto_total": 185000.50}

    # 1. Reporte CSV sin firma
    gen = GeneradorReporte(ExportadorCSV())
    ruta = gen.generar(datos_planilla, "planilla_agosto")
    print(f"Generado: {ruta}\n")

    # 2. Cambiar exportador en tiempo de ejecución
    gen.cambiar_exportador(ExportadorJSON())
    ruta = gen.generar(datos_planilla, "planilla_agosto")
    print(f"Generado: {ruta}\n")

    # 3. Reporte CSV con firma digital
    gen_firmado = GeneradorReporte(ExportadorCSV(), FirmadorDigital("clave_unap_2026"))
    ruta = gen_firmado.generar(datos_planilla, "planilla_firmada")
    print(f"Generado y firmado: {ruta}")
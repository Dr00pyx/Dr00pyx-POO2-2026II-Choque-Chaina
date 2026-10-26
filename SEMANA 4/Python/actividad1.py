import sys
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

# Configuración de codificación para evitar errores en terminales Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ── Interfaz pura con ABC ──────────────────────────────────────────────
class INotificador(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, mensaje: str) -> bool: ...

    @abstractmethod
    def es_disponible(self) -> bool: ...

    @property
    @abstractmethod
    def nombre(self) -> str: ...


# ── Interfaz con Protocol (duck typing estructural) ────────────────────
@runtime_checkable
class ProtocolNotificador(Protocol):
    def enviar(self, destinatario: str, mensaje: str) -> bool: ...
    def es_disponible(self) -> bool: ...


# ── Implementaciones Concretas ─────────────────────────────────────────
class NotificadorEmail(INotificador):
    def __init__(self, servidor_smtp: str, puerto: int = 587):
        self._servidor = servidor_smtp
        self._puerto = puerto
        self._activo = True

    @property
    def nombre(self) -> str:
        return f"Email ({self._servidor})"

    def es_disponible(self) -> bool:
        return self._activo

    def enviar(self, dest: str, msg: str) -> bool:
        print(f"[EMAIL → {dest}]: {msg[:50]}...")
        return True


class NotificadorSMS(INotificador):
    MAX_CHARS = 160

    def __init__(self, proveedor: str):
        self._proveedor = proveedor
        self._activo = True

    @property
    def nombre(self) -> str:
        return f"SMS ({self._proveedor})"

    def es_disponible(self) -> bool:
        return self._activo

    def enviar(self, dest: str, msg: str) -> bool:
        if len(msg) > self.MAX_CHARS:
            raise ValueError(f"SMS excede {self.MAX_CHARS} caracteres")
        print(f"[SMS → {dest}]: {msg}")
        return True


# ── Sistema de Alertas (Composición) ───────────────────────────────────
class SistemaAlertas:
    """Usa composición — depende de la abstracción INotificador."""
    def __init__(self, notificadores: list[INotificador]):
        if not notificadores:
            raise ValueError("Se requiere al menos un notificador")
        self._notificadores = list(notificadores)

    def agregar_notificador(self, n: INotificador) -> None:
        self._notificadores.append(n)

    def alertar(self, dest: str, mensaje: str) -> int:
        enviados = 0
        for n in self._notificadores:
            if n.es_disponible():
                try:
                    if n.enviar(dest, mensaje):
                        enviados += 1
                except Exception as e:
                    print(f"Error en {n.nombre}: {e}")
        return enviados


# ── Pruebas ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sistema = SistemaAlertas([
        NotificadorEmail("smtp.unap.edu.pe"),
        NotificadorSMS("Movistar"),
    ])

    enviados = sistema.alertar(
        "jmamani@unap.edu.pe",
        "ALERTA: Temperatura del Lago Titicaca supera 18°C"
    )
    print(f"\nAlerta enviada por {enviados} canales.")

    # Verificaciones
    assert isinstance(sistema._notificadores[0], INotificador)
    assert isinstance(sistema._notificadores[0], ProtocolNotificador)
    print("Verificaciones de Actividad 1 exitosas.")
"""
Módulo de Implementación del Patrón Observer.
Permite el desacoplamiento entre el Sujeto (RepositorioObservable) y los Observadores
(LoggerObservador, ConsolaObservador, EmailObservador).
"""
from __future__ import annotations
from typing import Any, List, Optional, Protocol
from estudiante import Estudiante
import logger as Logger


class IObservador(Protocol):
    """Protocolo abstracto para cualquier observador de eventos de estudiante."""
    def on_guardado(self, e: Estudiante) -> None:
        ...


class LoggerObservador:
    """Observador que registra el evento de guardado en el Logger del sistema."""
    def on_guardado(self, e: Estudiante) -> None:
        Logger.log(f"Guardado: [{e.codigo}] {e.nombre}")


class ConsolaObservador:
    """Observador que actúa como Vista de consola y muestra el estado del estudiante."""
    def on_guardado(self, e: Estudiante) -> None:
        print(f">> Vista: {e}")


class EmailObservador:
    """
    ADICIONAL Actividad 1A:
    Observador que simula el despacho de una notificación por correo electrónico.
    """
    def on_guardado(self, e: Estudiante) -> None:
        print(f"Enviando correo a {e.nombre}")


class RepositorioObservable:
    """
    Sujeto Observable (Subject).
    Envuelve una implementación de repositorio y notifica a los suscriptores
    cada vez que se almacena una entidad Estudiante.
    """
    def __init__(self, repo: Any) -> None:
        self._repo = repo
        self._obs: List[IObservador] = []

    def suscribir(self, o: IObservador) -> None:
        if o not in self._obs:
            self._obs.append(o)

    def desuscribir(self, o: IObservador) -> None:
        if o in self._obs:
            self._obs.remove(o)

    @property
    def observadores(self) -> List[IObservador]:
        return list(self._obs)

    def guardar(self, e: Estudiante) -> None:
        self._repo.guardar(e)
        for o in self._obs:
            o.on_guardado(e)

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._repo.buscar(cod)

    def listar(self) -> List[Estudiante]:
        return self._repo.listar()

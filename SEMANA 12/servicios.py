"""
Módulo de Servicios de Dominio / Controlador.
ServicioEstudiante orquesta el cálculo de métricas académicas (Strategy)
y la persistencia desacoplada (Repository / Observer).
"""
from __future__ import annotations
from typing import List, Optional
from estudiante import Estudiante
from estrategias import IEstrategiaCalculo
from repositorios import IRepositorioEstudiante


class ServicioEstudiante:
    """
    Controlador en la arquitectura MVC.
    Coordina la interacción entre el modelo de datos, la lógica de cálculo y la persistencia.
    """
    def __init__(self, repo: IRepositorioEstudiante, calc: IEstrategiaCalculo) -> None:
        self._repo = repo
        self._calc = calc

    def set_estrategia(self, calc: IEstrategiaCalculo) -> None:
        """Permite alternar la estrategia de cálculo en tiempo de ejecución."""
        self._calc = calc

    @property
    def estrategia(self) -> IEstrategiaCalculo:
        return self._calc

    def registrar(self, e: Estudiante) -> None:
        """
        Calcula el PPA utilizando la estrategia configurada
        y guarda el estudiante en el repositorio.
        Si el repositorio es observable, notificará a las vistas/observadores.
        """
        e.ppa = self._calc.calcular(e.notas)
        self._repo.guardar(e)

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._repo.buscar(cod)

    def listar(self) -> List[Estudiante]:
        return self._repo.listar()

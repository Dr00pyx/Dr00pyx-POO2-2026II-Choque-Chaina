from __future__ import annotations
from typing import List, Optional
from estudiante import Estudiante
from estrategias import IEstrategiaCalculo
from repositorios import IRepositorioEstudiante


class ServicioEstudiante:
    def __init__(self, repo: IRepositorioEstudiante, calc: IEstrategiaCalculo) -> None:
        self._repo = repo
        self._calc = calc

    def set_estrategia(self, calc: IEstrategiaCalculo) -> None:
        self._calc = calc

    @property
    def estrategia(self) -> IEstrategiaCalculo:
        return self._calc

    def registrar(self, e: Estudiante) -> None:
        e.ppa = self._calc.calcular(e.notas)
        self._repo.guardar(e)

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._repo.buscar(cod)

    def listar(self) -> List[Estudiante]:
        return self._repo.listar()

    def eliminar(self, cod: int) -> None:
        if hasattr(self._repo, "eliminar"):
            self._repo.eliminar(cod)

    def exportar_excel(self, ruta: str = "estudiantes.xlsx") -> str:
        from exportador_excel import exportar_a_excel
        return exportar_a_excel(self.listar(), ruta)

    def importar_excel(self, ruta: str) -> int:
        from exportador_excel import importar_de_excel
        estudiantes = importar_de_excel(ruta)
        for e in estudiantes:
            self.registrar(e)
        return len(estudiantes)

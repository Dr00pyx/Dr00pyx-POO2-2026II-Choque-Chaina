"""
Entidad de Dominio: Estudiante
"""
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Estudiante:
    codigo: str
    nombre: str
    carrera: str
    promedio: float
    semestre: str = "2026-II"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Estudiante":
        return cls(
            codigo=str(data["codigo"]),
            nombre=str(data["nombre"]),
            carrera=str(data.get("carrera", "Ingeniería de Sistemas")),
            promedio=float(data.get("promedio", 0.0)),
            semestre=str(data.get("semestre", "2026-II"))
        )

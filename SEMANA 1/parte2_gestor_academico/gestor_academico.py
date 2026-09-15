from dataclasses import dataclass, field
from typing import Protocol, List, Dict, Optional

class AuditoriaInterface(Protocol):
    def registrar(self, mensaje: str) -> None:
        ...

class AuditoriaArchivo:
    def __init__(self, ruta: str = "auditoria.txt") -> None:
        self._ruta = ruta

    def registrar(self, mensaje: str) -> None:
        with open(self._ruta, "a", encoding="utf-8") as f:
            f.write(f"{mensaje}\n")

class AuditoriaNull:
    """Implementación nula para pruebas unitarias sin I/O."""
    def registrar(self, mensaje: str) -> None:
        pass

@dataclass
class Estudiante:
    codigo: str
    nombre: str
    _notas: List[float] = field(default_factory=list, repr=False)

    def agregar_nota(self, nota: float) -> None:
        if not (0.0 <= nota <= 20.0):
            raise ValueError(f"La nota {nota} está fuera del rango permitido [0, 20].")
        self._notas.append(nota)

    @property
    def notas(self) -> List[float]:
        return list(self._notas)

    @property
    def promedio(self) -> float:
        if not self._notas:
            return 0.0
        return sum(self._notas) / len(self._notas)

    @property
    def esta_aprobado(self) -> bool:
        return self.promedio >= 10.5

class RepositorioEstudiantes:
    def __init__(self) -> None:
        self._estudiantes: Dict[str, Estudiante] = {}

    def guardar(self, estudiante: Estudiante) -> None:
        self._estudiantes[estudiante.codigo] = estudiante

    def buscar_por_codigo(self, codigo: str) -> Optional[Estudiante]:
        return self._estudiantes.get(codigo)

    def obtener_todos(self) -> List[Estudiante]:
        return list(self._estudiantes.values())

class GeneradorReporteCSV:
    @staticmethod
    def generar_lineas(estudiantes: List[Estudiante]) -> List[str]:
        lineas = ["codigo,nombre,promedio,estado"]
        for est in estudiantes:
            estado = "APROBADO" if est.esta_aprobado else "DESAPROBADO"
            lineas.append(f"{est.codigo},{est.nombre},{est.promedio:.2f},{estado}")
        return lineas

    @classmethod
    def exportar_archivo(cls, estudiantes: List[Estudiante], ruta: str = "reporte.csv") -> None:
        lineas = cls.generar_lineas(estudiantes)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas) + "\n")

class ServicioAcademico:
    def __init__(
        self, 
        repo: RepositorioEstudiantes, 
        auditoria: Optional[AuditoriaInterface] = None
    ) -> None:
        self._repo = repo
        self._auditoria = auditoria or AuditoriaNull()

    def registrar_estudiante(self, codigo: str, nombre: str) -> Estudiante:
        estudiante = Estudiante(codigo=codigo, nombre=nombre)
        self._repo.guardar(estudiante)
        self._auditoria.registrar(f"Estudiante registrado: {codigo} - {nombre}")
        return estudiante

    def agregar_nota_estudiante(self, codigo: str, nota: float) -> None:
        estudiante = self._repo.buscar_por_codigo(codigo)
        if not estudiante:
            raise KeyError(f"Estudiante con código {codigo} no encontrado.")
        estudiante.agregar_nota(nota)
        self._auditoria.registrar(f"Nota {nota} agregada a {codigo}")
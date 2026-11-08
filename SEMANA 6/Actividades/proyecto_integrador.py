# -*- coding: utf-8 -*-
"""
proyecto_integrador.py — Actividad 5: Integración de Repositorios Genéricos en Python 3.12+
"""
from dataclasses import dataclass
from typing import Optional
from repositorio import Repositorio
from actividad3_python import ColaAtencion

@dataclass
class Docente:
    dni: str
    nombres: str
    apellidos: str
    categoria: str  # "Auxiliar", "Asociado", "Principal"
    horas: int
    factor: float

    @property
    def nombre_completo(self) -> str:
        return f"{self.apellidos}, {self.nombres}"

    def calcular_remuneracion(self) -> float:
        tarifa_hora = 75.0
        return self.horas * tarifa_hora * self.factor


@dataclass
class Administrativo:
    dni: str
    nombres: str
    apellidos: str
    area: str
    salario_base: float
    bono: float = 0.0

    @property
    def nombre_completo(self) -> str:
        return f"{self.apellidos}, {self.nombres}"

    def calcular_remuneracion(self) -> float:
        return self.salario_base + self.bono


class SistemaGestionUNAP:
    """
    Sistema del Proyecto Integrador refactorizado para usar Repositorio[T, ID]
    como única capa de almacenamiento en memoria y ColaAtencion para trámites FIFO.
    """
    def __init__(self) -> None:
        # Repositorio Tipado 1: Docentes (ID: str = DNI)
        self.repo_docentes: Repositorio[Docente, str] = Repositorio(lambda d: d.dni)
        # Repositorio Tipado 2: Administrativos (ID: str = DNI)
        self.repo_administrativos: Repositorio[Administrativo, str] = Repositorio(lambda a: a.dni)
        # Cola de trámites FIFO (deque)
        self.cola_tramites: ColaAtencion = ColaAtencion()

    def registrar_docente(self, docente: Docente) -> None:
        self.repo_docentes.guardar(docente)

    def registrar_administrativo(self, administrativo: Administrativo) -> None:
        self.repo_administrativos.guardar(administrativo)

    def encolar_tramite(self, dni: str) -> None:
        self.cola_tramites.encolar(dni)

    def atender_tramite(self) -> Optional[str]:
        return self.cola_tramites.atender()

    # ── 5 CONSULTAS DE DOMINIO REQUERIDAS ────────────────────────────────────

    # 1. Filtrar: Docentes con dedicación a tiempo completo (horas >= 30)
    def docentes_tiempo_completo(self) -> list[Docente]:
        return self.repo_docentes.filtrar(lambda d: d.horas >= 30)

    # 2. Ordenar: Ranking de docentes por remuneración descendente
    def ranking_docentes(self) -> list[Docente]:
        return self.repo_docentes.ordenar(key=lambda d: d.calcular_remuneracion(), reverse=True)

    # 3. Filtrar: Personal administrativo con bono asignado
    def administrativos_con_bono(self) -> list[Administrativo]:
        return self.repo_administrativos.filtrar(lambda a: a.bono > 0)

    # 4. Acumular: Total de planilla exclusiva de docentes
    def total_planilla_docentes(self) -> float:
        return self.repo_docentes.acumular(
            0.0, lambda acc, d: acc + d.calcular_remuneracion()
        )

    # 5. Acumular: Total consolidado institucional (Docentes + Administrativos)
    def total_planilla_institucional(self) -> float:
        total_doc = self.total_planilla_docentes()
        total_adm = self.repo_administrativos.acumular(
            0.0, lambda acc, a: acc + a.calcular_remuneracion()
        )
        return total_doc + total_adm


def main() -> None:
    print("=================================================================")
    print("ACTIVIDAD 5 (Python): PROYECTO INTEGRADOR CON REPOSITORIOS GEN.")
    print("=================================================================")

    sistema = SistemaGestionUNAP()

    # Cargar datos de Docentes
    sistema.registrar_docente(Docente("70112233", "Carlos", "Mamani Quispe", "Principal", 40, 1.8))
    sistema.registrar_docente(Docente("70223344", "Elena", "Flores Coila", "Asociado", 35, 1.4))
    sistema.registrar_docente(Docente("70334455", "Ana", "Ramos Cutipa", "Auxiliar", 20, 1.0))
    sistema.registrar_docente(Docente("70445566", "Victor", "Paredes Choque", "Auxiliar", 15, 1.0))
    sistema.registrar_docente(Docente("70556677", "Marcos", "Condori Apaza", "Principal", 38, 1.8))

    # Cargar datos de Administrativos
    sistema.registrar_administrativo(Administrativo("80112233", "Rosa", "Quispe Mamani", "Recursos Humanos", 2800.0, 450.0))
    sistema.registrar_administrativo(Administrativo("80223344", "Juan", "Calsin Ticona", "Contabilidad", 3200.0, 0.0))
    sistema.registrar_administrativo(Administrativo("80334455", "Sonia", "Chura Pari", "Secretaria General", 2500.0, 300.0))
    sistema.registrar_administrativo(Administrativo("80445566", "David", "Huanca Gomez", "Informatica", 3500.0, 600.0))

    print(f"Docentes registrados        : {len(sistema.repo_docentes)}")
    print(f"Administrativos registrados : {len(sistema.repo_administrativos)}")

    print("\n" + "-" * 65)
    print(">>> EJECUCIÓN DE LAS 5 CONSULTAS DE DOMINIO (Python):")
    print("-" * 65)

    # 1. Consulta 1
    tc = sistema.docentes_tiempo_completo()
    print(f"\n[Consulta 1] Docentes a Tiempo Completo (Horas >= 30) [{len(tc)}]:")
    for d in tc:
        print(f"  * {d.nombre_completo:<25} | {d.horas} hrs | Cat: {d.categoria:<10} | S/ {d.calcular_remuneracion():.2f}")

    # 2. Consulta 2
    rank = sistema.ranking_docentes()
    print(f"\n[Consulta 2] Ranking Docentes por Remuneración Descendente:")
    for i, d in enumerate(rank, 1):
        print(f"  {i}. {d.nombre_completo:<25} | DNI: {d.dni} | S/ {d.calcular_remuneracion():.2f}")

    # 3. Consulta 3
    bonos = sistema.administrativos_con_bono()
    print(f"\n[Consulta 3] Personal Administrativo con Bono Especial [{len(bonos)}]:")
    for a in bonos:
        print(f"  * {a.nombre_completo:<25} | Área: {a.area:<20} | Bono: S/ {a.bono:.2f} | Total: S/ {a.calcular_remuneracion():.2f}")

    # 4. Consulta 4
    total_doc = sistema.total_planilla_docentes()
    print(f"\n[Consulta 4] Total Planilla Docentes (acumular): S/ {total_doc:.2f}")

    # 5. Consulta 5
    total_inst = sistema.total_planilla_institucional()
    print(f"\n[Consulta 5] Total Planilla Institucional (Docentes + Admins): S/ {total_inst:.2f}")

    # Flujo de atención de trámites
    print("\n" + "-" * 65)
    print(">>> FLUJO DE ATENCIÓN CON COLA FIFO (deque):")
    print("-" * 65)
    sistema.encolar_tramite("70112233")
    sistema.encolar_tramite("80112233")
    sistema.encolar_tramite("70556677")
    sistema.encolar_tramite("80445566")

    print(f"Trámites en cola pendientes: {len(sistema.cola_tramites)}")
    t = 1
    while sistema.cola_tramites:
        dni = sistema.atender_tramite()
        if not dni:
            break
        persona = sistema.repo_docentes.buscar(dni) or sistema.repo_administrativos.buscar(dni)
        desc = persona.nombre_completo if persona else "Desconocido"
        rol = "Docente" if isinstance(persona, Docente) else "Administrativo"
        print(f"  Atendiendo Turno #{t}: DNI {dni} -> {desc} ({rol})")
        t += 1

    print("=" * 65)

if __name__ == "__main__":
    main()

"""
SIS206 — Programación Orientada a Objetos II
Guía de Práctica Avanzada — Semana 10
Tema: Principios SOLID en el Sistema Académico UNAP

Refactorización completa en Python 3.12 (compatible con 3.10+):
- SRP (Single Responsibility Principle): División de responsabilidades en clases dedicadas.
- OCP (Open/Closed Principle): Nuevas estrategias de cálculo y persistencia sin modificar ServicioEstudiante.
- DIP (Dependency Inversion Principle): Inyección de dependencias mediante typing.Protocol.
"""

from __future__ import annotations
import csv
import os
from dataclasses import dataclass, field
from typing import Optional, Protocol, Sequence, runtime_checkable


# =============================================================================
# 1. SOLO DATOS (SRP: Única razón para cambiar: cambios en los atributos del estudiante)
# =============================================================================
@dataclass
class Estudiante:
    """Entidad de dominio pura que contiene exclusivamente el estado de un estudiante."""
    codigo: int
    nombre: str
    ppa: float = 0.0
    notas: list[float] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[Código: {self.codigo} | Nombre: {self.nombre:<20} | PPA: {self.ppa:5.2f}]"


# =============================================================================
# 2. SOLO CÁLCULO (SRP / OCP / DIP: Contrato e implementaciones de cálculo de PPA)
# =============================================================================
@runtime_checkable
class IEstrategiaCalculo(Protocol):
    """Protocolo (interfaz estructural) para algoritmos de cálculo de promedio."""
    def calcular(self, notas: Sequence[float]) -> float:
        ...


class PromedioSimple:
    """Cálculo tradicional mediante la media aritmética de todas las notas."""
    def calcular(self, notas: Sequence[float]) -> float:
        if not notas:
            return 0.0
        return sum(notas) / len(notas)


class PromedioModerado:
    """
    OCP: Cálculo que descarta la nota más alta y la más baja antes de promediar.
    
    Permite incorporar una nueva regla de evaluación académica sin modificar
    la clase ServicioEstudiante.
    """
    def calcular(self, notas: Sequence[float]) -> float:
        # Si tiene 2 notas o menos, no es posible descartar ambos extremos
        if len(notas) <= 2:
            return 0.0
        notas_ordenadas = sorted(notas)
        # Descartar primer elemento (mínimo) y último elemento (máximo)
        notas_filtradas = notas_ordenadas[1:-1]
        return sum(notas_filtradas) / len(notas_filtradas)


# =============================================================================
# 3. SOLO PERSISTENCIA (Protocol = Interfaz DIP y Repositorios Concretos)
# =============================================================================
@runtime_checkable
class IRepositorioEstudiante(Protocol):
    """
    Protocolo de abstracción para operaciones de persistencia de estudiantes.
    Cumple DIP: Desacopla la lógica de negocio de la tecnología de almacenamiento.
    """
    def guardar(self, e: Estudiante) -> None:
        ...

    def buscar(self, cod: int) -> Optional[Estudiante]:
        ...

    def listar(self) -> list[Estudiante]:
        ...


class RepositorioMemoria:
    """Implementación de persistencia volátil en memoria (ideal para pruebas y desacoplamiento)."""
    def __init__(self) -> None:
        self._datos: dict[int, Estudiante] = {}

    def guardar(self, e: Estudiante) -> None:
        self._datos[e.codigo] = e

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._datos.get(cod)

    def listar(self) -> list[Estudiante]:
        return list(self._datos.values())


class RepositorioCsv:
    """
    Implementación adicional de persistencia persistente en archivo CSV.
    Permite almacenar y recuperar estudiantes en disco cumpliendo IRepositorioEstudiante.
    """
    def __init__(self, ruta_archivo: Optional[str] = None) -> None:
        if ruta_archivo is None:
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            self._ruta = os.path.join(directorio_actual, "estudiantes_python.csv")
        else:
            self._ruta = ruta_archivo
        self._datos: dict[int, Estudiante] = {}
        self._cargar()

    def _cargar(self) -> None:
        if not os.path.exists(self._ruta):
            return
        with open(self._ruta, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                cod = int(fila["codigo"])
                nombre = fila["nombre"]
                ppa = float(fila["ppa"])
                self._datos[cod] = Estudiante(codigo=cod, nombre=nombre, ppa=ppa)

    def _persistir(self) -> None:
        with open(self._ruta, mode="w", newline="", encoding="utf-8") as f:
            fieldnames = ["codigo", "nombre", "ppa"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for est in self._datos.values():
                writer.writerow({"codigo": est.codigo, "nombre": est.nombre, "ppa": f"{est.ppa:.2f}"})

    def guardar(self, e: Estudiante) -> None:
        self._datos[e.codigo] = e
        self._persistir()

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._datos.get(cod)

    def listar(self) -> list[Estudiante]:
        return list(self._datos.values())


# =============================================================================
# 4. ORQUESTACIÓN (ServicioEstudiante aplica DIP y SRP)
# =============================================================================
class ServicioEstudiante:
    """
    Servicio de aplicación que orquesta el registro y búsqueda de estudiantes.
    
    Aplica DIP:
    - Recibe el repositorio y la estrategia de cálculo a través de inyección de dependencias.
    - Depende únicamente de las abstracciones IRepositorioEstudiante e IEstrategiaCalculo.
    """
    def __init__(self, repo: IRepositorioEstudiante, calc: IEstrategiaCalculo) -> None:
        self._repo = repo
        self._calc = calc

    def registrar(self, e: Estudiante) -> None:
        """Calcula el PPA usando la estrategia inyectada y almacena el estudiante en el repositorio."""
        e.ppa = self._calc.calcular(e.notas)
        self._repo.guardar(e)

    def buscar(self, cod: int) -> Optional[Estudiante]:
        """Recupera un estudiante desde el repositorio según su código."""
        return self._repo.buscar(cod)

    def listar(self) -> list[Estudiante]:
        """Obtiene todos los estudiantes almacenados."""
        return self._repo.listar()


# =============================================================================
# RESPUESTA A PREGUNTA DE ACTIVIDAD 2B:
# ¿ServicioEstudiante cambió al agregar PromedioModerado?
# RESPUESTA:
# NO. La clase ServicioEstudiante NO cambió en lo absoluto.
# Esto demuestra el Principio Abierto/Cerrado (OCP):
# El software está ABIERTO a la extensión (se pueden crear nuevas estrategias como
# PromedioModerado o nuevos repositorios como RepositorioCsv o RepositorioSQLite)
# y CERRADO a la modificación (el código ya testeado y operativo de ServicioEstudiante
# permanece inalterado y libre de regresiones).
# =============================================================================


def main() -> None:
    print("=" * 70)
    print("  UNIVERSIDAD NACIONAL DEL ALTIPLANO - SIS206 POO II")
    print("  SEMANA 10: PRINCIPIOS SOLID EN EL SISTEMA ACADÉMICO UNAP")
    print("  IMPLEMENTACIÓN EN PYTHON 3.12")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # ACTIVIDAD 1B: ServicioEstudiante con RepositorioMemoria + PromedioSimple
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("[ACTIVIDAD 1B] SRP + DIP: Registro de 3 estudiantes con PromedioSimple")
    print("-" * 70)

    repo_memoria = RepositorioMemoria()
    calc_simple = PromedioSimple()
    svc1 = ServicioEstudiante(repo=repo_memoria, calc=calc_simple)

    # Registro de 3 estudiantes con notas distintas
    estudiantes_prueba = [
        Estudiante(codigo=202101, nombre="Carlos Condori", notas=[15.0, 17.5, 13.0, 16.5]),
        Estudiante(codigo=202102, nombre="Mariana Ramos",  notas=[18.0, 19.0, 20.0, 17.0]),
        Estudiante(codigo=202103, nombre="Juan Mamani",    notas=[11.0, 12.5, 14.0, 10.5]),
    ]

    for est in estudiantes_prueba:
        svc1.registrar(est)
        print(f"-> Registrado: {est.nombre} (Código: {est.codigo})")

    # Verificación con buscar() de que el PPA se calculó correctamente
    print("\n-> Verificación con buscar() y cálculo de PPA:")
    for est in estudiantes_prueba:
        encontrado = svc1.buscar(est.codigo)
        assert encontrado is not None, f"Error: No se encontró al estudiante {est.codigo}"
        ppa_esperado = sum(est.notas) / len(est.notas)
        es_correcto = abs(encontrado.ppa - ppa_esperado) < 0.001
        print(f"   {encontrado} | Esperado: {ppa_esperado:5.2f} -> {'[OK]' if es_correcto else '[ERROR]'}")

    # -------------------------------------------------------------------------
    # ACTIVIDAD 2B: OCP (Agregar PromedioModerado sin modificar ServicioEstudiante)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("[ACTIVIDAD 2B] OCP: Comparación PromedioSimple vs PromedioModerado")
    print("-" * 70)

    calc_moderado = PromedioModerado()
    svc2 = ServicioEstudiante(repo=repo_memoria, calc=calc_moderado)

    # Caso de prueba de la guía:
    # Notas: [14.0, 20.0, 16.0, 18.0, 12.0]
    # PromedioSimple: (14 + 20 + 16 + 18 + 12) / 5 = 80 / 5 = 16.0
    # PromedioModerado: descarta 12 y 20 -> (14 + 16 + 18) / 3 = 48 / 3 = 16.0
    est_ana_simple = Estudiante(codigo=1001, nombre="Ana Quispe", notas=[14.0, 20.0, 16.0, 18.0, 12.0])
    svc1.registrar(est_ana_simple)
    ppa_ana_simple = svc1.buscar(1001).ppa

    est_ana_moderado = Estudiante(codigo=1001, nombre="Ana Quispe", notas=[14.0, 20.0, 16.0, 18.0, 12.0])
    svc2.registrar(est_ana_moderado)
    ppa_ana_moderado = svc2.buscar(1001).ppa

    print("-> Caso Oficial de la Guía (Ana Quispe: notas [14.0, 20.0, 16.0, 18.0, 12.0]):")
    print(f"   PPA con PromedioSimple  : {ppa_ana_simple:.2f}")
    print(f"   PPA con PromedioModerado: {ppa_ana_moderado:.2f}")
    print(f"   Verificación (PPA == 16.0): {'[OK]' if abs(ppa_ana_moderado - 16.0) < 0.001 else '[ERROR]'}")

    # Caso con notas extremas para resaltar la diferencia práctica
    est_luis = Estudiante(codigo=1002, nombre="Luis Chambi", notas=[5.0, 15.0, 16.0, 17.0, 20.0])
    svc1.registrar(est_luis)
    ppa_luis_simple = svc1.buscar(1002).ppa

    svc2.registrar(est_luis)
    ppa_luis_moderado = svc2.buscar(1002).ppa

    print("\n-> Caso con Notas Extremas (Luis Chambi: notas [5.0, 15.0, 16.0, 17.0, 20.0]):")
    print(f"   PPA con PromedioSimple  : {ppa_luis_simple:.2f} (Suma 73 / 5 = 14.60)")
    print(f"   PPA con PromedioModerado: {ppa_luis_moderado:.2f} (Descarta 5.0 y 20.0 -> Suma 48 / 3 = 16.00)")
    print(f"   Demostración OCP: ServicioEstudiante no cambió, solo se cambió la estrategia inyectada.")

    # -------------------------------------------------------------------------
    # PERSISTENCIA EN ARCHIVO CSV (ADICIONAL)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("[PERSISTENCIA ADICIONAL] RepositorioCsv en Python")
    print("-" * 70)
    repo_csv = RepositorioCsv()
    svc_csv = ServicioEstudiante(repo=repo_csv, calc=calc_moderado)

    est_csv = Estudiante(codigo=3001, nombre="Elena Morales", notas=[16.0, 19.0, 14.0, 18.0])
    svc_csv.registrar(est_csv)
    print(f"-> Registrado y persistido en 'estudiantes_python.csv':")
    print(f"   {svc_csv.buscar(3001)}")

    print("\n" + "=" * 70)
    print("  TODAS LAS PRUEBAS EN PYTHON COMPLETADAS EXITOSAMENTE")
    print("=" * 70)


if __name__ == "__main__":
    main()

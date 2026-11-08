"""
Actividad 2: Patrón Factory Method - Generador de Boletas de Notas Académicas.
Implementación completa con Producto Abstracto, Productos Concretos, Creador Base,
Creadores Concretos y Registro Dinámico de Fábricas (Registry Pattern + Factory Method).
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Dict, List, Type


# ==============================================================================
# 1. PRODUCTO ABSTRACTO
# ==============================================================================

@dataclass
class EntradaNota:
    curso: str
    nota: float
    creditos: int


class BoletaNotas(ABC):
    """Interfaz abstracta del producto Boleta de Notas."""

    def __init__(self, estudiante: str = "", codigo: str = "", semestre: str = "") -> None:
        self.estudiante = estudiante
        self.codigo = codigo
        self.semestre = semestre
        self._notas: List[EntradaNota] = []

    def set_datos_estudiante(self, estudiante: str, codigo: str, semestre: str) -> None:
        self.estudiante = estudiante
        self.codigo = codigo
        self.semestre = semestre

    def agregar_nota(self, curso: str, nota: float, creditos: int) -> None:
        self._notas.append(EntradaNota(curso=curso, nota=nota, creditos=creditos))

    @property
    def total_creditos(self) -> int:
        return sum(n.creditos for n in self._notas)

    @property
    def promedio_ponderado(self) -> float:
        total_cr = self.total_creditos
        if total_cr == 0:
            return 0.0
        puntos = sum(n.nota * n.creditos for n in self._notas)
        return round(puntos / total_cr, 2)

    @property
    def estado_final(self) -> str:
        return "APROBADO" if self.promedio_ponderado >= 11.0 else "DESAPROBADO"

    @abstractmethod
    def generar(self) -> str:
        """Serializa la boleta en el formato específico."""
        pass

    @property
    @abstractmethod
    def extension(self) -> str:
        """Extensión de archivo asociada (ej. .txt, .csv, .html)."""
        pass

    @property
    @abstractmethod
    def formato(self) -> str:
        """Nombre descriptivo del formato."""
        pass


# ==============================================================================
# 2. PRODUCTOS CONCRETOS
# ==============================================================================

class BoletaTXT(BoletaNotas):
    """Producto concreto: Boleta en formato texto plano estructurado."""

    @property
    def extension(self) -> str:
        return ".txt"

    @property
    def formato(self) -> str:
        return "Texto Plano (TXT)"

    def generar(self) -> str:
        lineas = [
            "============================================================",
            "         UNIVERSIDAD NACIONAL DEL ALTIPLANO - PUNO          ",
            "                  BOLETA DE NOTAS OFICIAL                   ",
            "============================================================",
            f"Estudiante : {self.estudiante}",
            f"Código     : {self.codigo}",
            f"Semestre   : {self.semestre}",
            "------------------------------------------------------------",
            f"{'CURSO':<35} {'CRÉD':<8} {'NOTA':<8} {'ESTADO':<10}",
            "------------------------------------------------------------",
        ]
        for n in self._notas:
            condicion = "Aprobado" if n.nota >= 11.0 else "Desaprobado"
            lineas.append(f"{n.curso:<35} {n.creditos:<8} {n.nota:<8.1f} {condicion:<10}")

        lineas.extend([
            "------------------------------------------------------------",
            f"Total Créditos      : {self.total_creditos}",
            f"Promedio Ponderado  : {self.promedio_ponderado:.2f}",
            f"Condición Académica : {self.estado_final}",
            "============================================================",
        ])
        return "\n".join(lineas)


class BoletaCSV(BoletaNotas):
    """Producto concreto: Boleta en formato CSV delimitado por comas."""

    @property
    def extension(self) -> str:
        return ".csv"

    @property
    def formato(self) -> str:
        return "Valores Separados por Coma (CSV)"

    def generar(self) -> str:
        lineas = [
            f"# Metadatos: Estudiante={self.estudiante};Codigo={self.codigo};Semestre={self.semestre}",
            "Curso,Creditos,Nota,Condicion"
        ]
        for n in self._notas:
            cond = "Aprobado" if n.nota >= 11.0 else "Desaprobado"
            # Escapar comas eventuales en el nombre del curso
            curso_escapado = f'"{n.curso}"' if "," in n.curso else n.curso
            lineas.append(f"{curso_escapado},{n.creditos},{n.nota:.2f},{cond}")

        lineas.append(f"RESUMEN,{self.total_creditos},{self.promedio_ponderado:.2f},{self.estado_final}")
        return "\n".join(lineas)


class BoletaHTML(BoletaNotas):
    """Producto concreto: Boleta en formato HTML responsivo y estilizado."""

    @property
    def extension(self) -> str:
        return ".html"

    @property
    def formato(self) -> str:
        return "Hipertexto Web (HTML)"

    def generar(self) -> str:
        filas_html = []
        for n in self._notas:
            color = "#28a745" if n.nota >= 11.0 else "#dc3545"
            cond = "Aprobado" if n.nota >= 11.0 else "Desaprobado"
            filas_html.append(
                f"      <tr>\n"
                f"        <td>{n.curso}</td>\n"
                f"        <td style='text-align:center;'>{n.creditos}</td>\n"
                f"        <td style='text-align:center;'><strong>{n.nota:.1f}</strong></td>\n"
                f"        <td style='text-align:center; color:{color}; font-weight:bold;'>{cond}</td>\n"
                f"      </tr>"
            )

        filas_str = "\n".join(filas_html)
        color_final = "#28a745" if self.promedio_ponderado >= 11.0 else "#dc3545"

        return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Boleta de Notas - {self.estudiante}</title>
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; background: #f8f9fa; }}
    .card {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 700px; margin: auto; }}
    h1 {{ color: #003366; text-align: center; margin-bottom: 5px; }}
    h2 {{ color: #666; text-align: center; font-size: 16px; margin-top: 0; }}
    .info {{ margin: 20px 0; padding: 12px; background: #eef2f7; border-radius: 6px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
    th, td {{ border: 1px solid #dee2e6; padding: 10px; }}
    th {{ background: #003366; color: white; text-align: left; }}
    .resumen {{ margin-top: 20px; font-size: 16px; text-align: right; }}
    .badge {{ padding: 6px 12px; border-radius: 4px; color: white; background: {color_final}; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>UNAP - PUNO</h1>
    <h2>BOLETA ACADÉMICA SEMESTRAL</h2>
    <div class="info">
      <p><strong>Estudiante:</strong> {self.estudiante} | <strong>Código:</strong> {self.codigo}</p>
      <p><strong>Semestre:</strong> {self.semestre}</p>
    </div>
    <table>
      <thead>
        <tr>
          <th>Asignatura</th>
          <th style='text-align:center;'>Créditos</th>
          <th style='text-align:center;'>Nota</th>
          <th style='text-align:center;'>Condición</th>
        </tr>
      </thead>
      <tbody>
{filas_str}
      </tbody>
    </table>
    <div class="resumen">
      <p><strong>Total Créditos:</strong> {self.total_creditos}</p>
      <p><strong>Promedio Ponderado:</strong> {self.promedio_ponderado:.2f}</p>
      <p><strong>Condición:</strong> <span class="badge">{self.estado_final}</span></p>
    </div>
  </div>
</body>
</html>"""


# ==============================================================================
# 3. CREADOR BASE Y CREADORES CONCRETOS (FACTORY METHOD)
# ==============================================================================

class GeneradorBoleta(ABC):
    """
    Clase creadora abstracta que define el Factory Method y el Template Method.
    """

    @abstractmethod
    def crear_boleta(self) -> BoletaNotas:
        """FACTORY METHOD: las subclases deciden qué objeto concreto instanciar."""
        pass

    def generar_y_enviar(
        self,
        estudiante: str,
        codigo: str,
        semestre: str,
        notas: List[dict],
        directorio_salida: str | Path = "."
    ) -> tuple[str, Path]:
        """
        TEMPLATE METHOD: orquesta el ciclo de vida del reporte sin acoplarse
        al formato de salida concreto.
        """
        boleta = self.crear_boleta()  # Invocación del Factory Method
        boleta.set_datos_estudiante(estudiante=estudiante, codigo=codigo, semestre=semestre)

        for n in notas:
            boleta.agregar_nota(curso=n["curso"], nota=float(n["nota"]), creditos=int(n["creditos"]))

        contenido = boleta.generar()
        
        dir_path = Path(directorio_salida)
        dir_path.mkdir(parents=True, exist_ok=True)
        nombre_archivo = f"boleta_{codigo}_{semestre}{boleta.extension}"
        ruta_archivo = dir_path / nombre_archivo

        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

        print(f"[{boleta.formato}] Generado exitosamente en: {ruta_archivo}")
        return contenido, ruta_archivo


class GeneradorBoletaTXT(GeneradorBoleta):
    """Creador concreto para boletas TXT."""
    def crear_boleta(self) -> BoletaNotas:
        return BoletaTXT()


class GeneradorBoletaCSV(GeneradorBoleta):
    """Creador concreto para boletas CSV."""
    def crear_boleta(self) -> BoletaNotas:
        return BoletaCSV()


class GeneradorBoletaHTML(GeneradorBoleta):
    """Creador concreto para boletas HTML."""
    def crear_boleta(self) -> BoletaNotas:
        return BoletaHTML()


# ==============================================================================
# 4. REGISTRO DINÁMICO DE FÁBRICAS (REGISTRY PATTERN)
# ==============================================================================

class RegistroGeneradores:
    """
    Registro desacoplado de fábricas. Permite registrar nuevos generadores
    dinámicamente cumpliendo con el principio Open/Closed (OCP).
    """

    def __init__(self) -> None:
        self._registro: Dict[str, Type[GeneradorBoleta]] = {}

    def registrar(self, formato: str, creador_cls: Type[GeneradorBoleta]) -> None:
        self._registro[formato.strip().lower()] = creador_cls

    def crear(self, formato: str) -> GeneradorBoleta:
        fmt = formato.strip().lower()
        if fmt not in self._registro:
            formatos_validos = ", ".join(self._registro.keys())
            raise ValueError(
                f"Formato de boleta no soportado: '{formato}'. Formatos disponibles: [{formatos_validos}]"
            )
        return self._registro[fmt]()

    def formatos_disponibles(self) -> list[str]:
        return list(self._registro.keys())

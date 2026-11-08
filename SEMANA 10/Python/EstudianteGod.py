"""
EstudianteGod.py — VIOLACIÓN FLAGRANTE DE SRP (Single Responsibility Principle)
Archivo ilustrativo de malas prácticas para comparación y análisis académico.
"""

import json
from dataclasses import dataclass, field


@dataclass
class EstudianteGod:
    """
    Clase "God" que acumula múltiples responsabilidades incompatibles:
    1. Datos de dominio del estudiante.
    2. Lógica de cálculo de promedios académicos (Negocio).
    3. Persistencia en disco (Acceso a datos).
    4. Serialización a formato JSON (Presentación/API).
    5. Notificación por correo electrónico (Comunicaciones externas).
    """
    codigo: int
    nombre: str
    ppa: float = 0.0
    notas: list[float] = field(default_factory=list)

    # Responsabilidad 1: Lógica de cálculo
    def calcular_ppa(self) -> float:
        if not self.notas:
            return 0.0
        return sum(self.notas) / len(self.notas)

    # Responsabilidad 2: Persistencia en archivo
    def guardar_en_archivo(self, ruta: str) -> None:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(f"{self.codigo},{self.nombre},{self.ppa}\n")

    # Responsabilidad 3: Serialización a JSON
    def to_json(self) -> str:
        return json.dumps({
            "codigo": self.codigo,
            "nombre": self.nombre,
            "ppa": self.ppa
        })

    # Responsabilidad 4: Notificación por correo
    def enviar_correo(self, destinatario: str) -> None:
        print(f"[EstudianteGod] Enviando correo electrónico a {destinatario}...")

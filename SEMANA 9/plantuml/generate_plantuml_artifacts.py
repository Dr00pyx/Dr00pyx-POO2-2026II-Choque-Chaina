# generate_plantuml_artifacts.py
import zlib
import os

plantuml_code = """@startuml SistemaAcademicoUNAP_S09
title Sistema Académico UNAP — Arquitectura Unidad II

package "Capa de Presentación" #D6E4F0 {
  component [GUIEstudiante] as GUI
  component [GUICurso] as GUICurso
  note right of GUI : Tkinter (S14)\\nPyQt5 (S14)
}

package "Capa de Servicios / Lógica" #E2EFDA {
  component [ServicioEstudiante] as SVC
  component [ServicioMatricula] as SVCM
  component [CalculadorPPA] as CALC
  component [NotificadorEmail] as NotificadorEmail
  interface IEstrategiaCalculo as IEST
  note right of SVC : SOLID (S10)\\nGoF (S11-S12)
}

package "Capa de Persistencia" #FCE4D6 {
  interface IRepositorioEstudiante as REPO
  component [RepositorioJSON] as JSON
  component [RepositorioSQLite] as SQLITE
  component [RepositorioSA] as SA
  note right of REPO : DIP (S10)\\nRepository (S13)\\nSQLAlchemy (S15)
}

package "C++17 Motor" #EAD1F5 {
  component [libcalculo.so] as LIB
  note right of LIB : extern C (S16)\\nctypes (S16)
}

GUI --> SVC
GUICurso --> SVCM
SVC --> REPO
SVC --> CALC
SVC --> NotificadorEmail : Observer (S12)
CALC .> IEST
CALC --> LIB : ctypes
REPO <|.. JSON
REPO <|.. SQLITE
REPO <|.. SA

@enduml
"""

# Guardar codigo PlantUML
puml_path = r"C:\Users\MELVIN\.gemini\antigravity\scratch\SEMANA 9\s09\plantuml\s09_arquitectura.puml"
with open(puml_path, "w", encoding="utf-8") as f:
    f.write(plantuml_code)
print("Archivo PUML guardado en:", puml_path)

# Codificacion oficial PlantUML (Deflate + 6-bit PlantUML alphabet)
def encode6bit(b):
    if b < 10:
        return chr(48 + b)
    b -= 10
    if b < 26:
        return chr(65 + b)
    b -= 26
    if b < 26:
        return chr(97 + b)
    b -= 26
    if b == 0:
        return '-'
    if b == 1:
        return '_'
    return '?'

def append3bytes(b1, b2, b3):
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return encode6bit(c1 & 0x3F) + encode6bit(c2 & 0x3F) + encode6bit(c3 & 0x3F) + encode6bit(c4 & 0x3F)

def plantuml_encode(text):
    z = zlib.compress(text.encode('utf-8'))[2:-4]
    res = ""
    i = 0
    while i < len(z):
        b1 = z[i]
        b2 = z[i+1] if i + 1 < len(z) else 0
        b3 = z[i+2] if i + 2 < len(z) else 0
        res += append3bytes(b1, b2, b3)
        i += 3
    return res

encoded = plantuml_encode(plantuml_code)
editor_url = f"https://www.plantuml.com/plantuml/uml/{encoded}"
png_url = f"https://www.plantuml.com/plantuml/png/{encoded}"
svg_url = f"https://www.plantuml.com/plantuml/svg/{encoded}"

url_file = r"C:\Users\MELVIN\.gemini\antigravity\scratch\SEMANA 9\s09\plantuml\enlaces_plantuml_online.txt"
with open(url_file, "w", encoding="utf-8") as f:
    f.write("ENLACES OFICIALES PLANTUML ONLINE - ACTIVIDAD 3A\n")
    f.write("==================================================\n\n")
    f.write(f"1. Ver y Editar Diagrama en PlantUML Web Editor:\n{editor_url}\n\n")
    f.write(f"2. Imagen PNG generada directamente por el servidor PlantUML:\n{png_url}\n\n")
    f.write(f"3. Imagen SVG vectorial generada directamente por el servidor PlantUML:\n{svg_url}\n")

print("Enlaces guardados en:", url_file)
print("URL Editor:", editor_url)

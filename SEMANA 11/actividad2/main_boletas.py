"""
Script principal de prueba para Actividad 2.
Carga configuración desde JSON e itera sobre los formatos generando boletas.
"""
import json
from pathlib import Path
from boletas import (
    RegistroGeneradores,
    GeneradorBoletaTXT,
    GeneradorBoletaCSV,
    GeneradorBoletaHTML,
)


def ejecutar_generacion():
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config_boletas.json"

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 1. Configurar Registro de Fábricas
    registro = RegistroGeneradores()
    registro.registrar("txt", GeneradorBoletaTXT)
    registro.registrar("csv", GeneradorBoletaCSV)
    registro.registrar("html", GeneradorBoletaHTML)

    formatos = config.get("formatos", ["txt", "csv", "html"])
    salida_dir = base_dir / config.get("directorio_salida", "salida_boletas")
    est = config["estudiante"]
    notas = config["notas"]

    print("=" * 65)
    print("  GENERACIÓN DE BOLETAS ACADÉMICAS CON FACTORY METHOD")
    print(f"  Estudiante: {est['nombre']} ({est['codigo']}) - Semestre: {est['semestre']}")
    print(f"  Formatos a procesar: {formatos}")
    print("=" * 65)

    archivos_generados = []
    for fmt in formatos:
        generador = registro.crear(fmt)
        _, archivo = generador.generar_y_enviar(
            estudiante=est["nombre"],
            codigo=est["codigo"],
            semestre=est["semestre"],
            notas=notas,
            directorio_salida=salida_dir
        )
        archivos_generados.append(archivo)

    print("=" * 65)
    print(f"Proceso finalizado. Total de archivos generados: {len(archivos_generados)}")
    for a in archivos_generados:
        print(f" -> {a.name} ({a.stat().st_size} bytes)")
    print("=" * 65)


if __name__ == "__main__":
    ejecutar_generacion()

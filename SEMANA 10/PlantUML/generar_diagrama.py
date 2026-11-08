"""
generar_diagrama.py — Renderizador automático de diagramas PlantUML a PNG
SIS206 — POO II | Semana 10

Lee el archivo .puml, lo codifica usando el algoritmo oficial de PlantUML (Deflate + 64-character mapping),
solicita la imagen renderizada al servidor oficial plantuml.com y la guarda localmente como PNG.
"""

import os
import zlib
import urllib.request


def plantuml_encode(text: str) -> str:
    """Codifica texto en formato PlantUML para la URL del servidor."""
    def encode6bit(b: int) -> str:
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

    def append3bytes(b1: int, b2: int, b3: int) -> str:
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        return encode6bit(c1 & 0x3F) + encode6bit(c2 & 0x3F) + encode6bit(c3 & 0x3F) + encode6bit(c4 & 0x3F)

    # Comprimir usando zlib raw deflate
    zlibbed = zlib.compress(text.encode('utf-8'))[2:-4]
    res = ''
    i = 0
    while i < len(zlibbed):
        b1 = zlibbed[i]
        b2 = zlibbed[i + 1] if i + 1 < len(zlibbed) else 0
        b3 = zlibbed[i + 2] if i + 2 < len(zlibbed) else 0
        res += append3bytes(b1, b2, b3)
        i += 3
    return res


def main():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_puml = os.path.join(directorio_actual, "s10_solid_diagrama.puml")

    if not os.path.exists(archivo_puml):
        print(f"Error: No se encontró {archivo_puml}")
        return

    with open(archivo_puml, "r", encoding="utf-8") as f:
        puml_content = f.read()

    encoded = plantuml_encode(puml_content)
    url_png = f"https://www.plantuml.com/plantuml/png/{encoded}"
    url_svg = f"https://www.plantuml.com/plantuml/svg/{encoded}"

    print(f"URL de visualización PlantUML (PNG): {url_png}")
    print(f"URL de visualización PlantUML (SVG): {url_svg}")

    # Descargar la imagen PNG renderizada
    req = urllib.request.Request(
        url_png,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    
    print("Descargando imagen renderizada desde PlantUML...")
    with urllib.request.urlopen(req) as resp:
        png_data = resp.read()

    # Guardar como s10_solid_apellido.png (solicitado en la guía de práctica)
    dest_apellido = os.path.join(directorio_actual, "s10_solid_apellido.png")
    with open(dest_apellido, "wb") as f:
        f.write(png_data)
    print(f"-> Guardado exitosamente: {dest_apellido} ({len(png_data)} bytes)")

    # Guardar también como s10_solid_diagrama.png para referencia clara
    dest_diagrama = os.path.join(directorio_actual, "s10_solid_diagrama.png")
    with open(dest_diagrama, "wb") as f:
        f.write(png_data)
    print(f"-> Guardado exitosamente: {dest_diagrama} ({len(png_data)} bytes)")


if __name__ == "__main__":
    main()

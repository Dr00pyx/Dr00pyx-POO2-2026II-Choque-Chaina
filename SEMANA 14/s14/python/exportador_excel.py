from __future__ import annotations
from typing import Sequence, List
from pathlib import Path
from estudiante import Estudiante


def exportar_a_excel(estudiantes: Sequence[Estudiante], ruta: str | Path = "estudiantes.xlsx") -> str:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Estudiantes UNAP"

    headers = ["Código", "Nombre", "PPA", "Notas", "Estado"]
    ws.append(headers)

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="0D47A1", end_color="0D47A1", fill_type="solid")
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")

    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9")
    )

    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    red_font = Font(name="Calibri", size=11, color="C00000", bold=True)
    normal_font = Font(name="Calibri", size=11)

    for row_idx, e in enumerate(estudiantes, start=2):
        estado = "Aprobado" if e.ppa >= 10.5 else "Desaprobado"
        notas_str = ", ".join(f"{n:.1f}" for n in e.notas) if e.notas else "Sin notas"

        c1 = ws.cell(row=row_idx, column=1, value=e.codigo)
        c1.alignment = center_align

        c2 = ws.cell(row=row_idx, column=2, value=e.nombre)
        c2.alignment = left_align

        c3 = ws.cell(row=row_idx, column=3, value=round(e.ppa, 2))
        c3.alignment = center_align
        c3.font = red_font if e.ppa < 10.5 else normal_font

        c4 = ws.cell(row=row_idx, column=4, value=notas_str)
        c4.alignment = left_align

        c5 = ws.cell(row=row_idx, column=5, value=estado)
        c5.alignment = center_align
        c5.font = red_font if e.ppa < 10.5 else normal_font

        for col_idx in range(1, 6):
            ws.cell(row=row_idx, column=col_idx).border = thin_border

    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    ruta_salida = str(Path(ruta).resolve())
    wb.save(ruta_salida)
    return ruta_salida


def importar_de_excel(ruta: str | Path) -> List[Estudiante]:
    import openpyxl

    wb = openpyxl.load_workbook(ruta, data_only=True)
    ws = wb.active
    estudiantes: list[Estudiante] = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or row[0] is None:
            continue
        try:
            cod = int(row[0])
            nom = str(row[1]).strip() if len(row) > 1 and row[1] is not None else ""
            if not nom:
                continue
            notas_raw = str(row[3]).strip() if len(row) > 3 and row[3] is not None else ""
            notas: list[float] = []
            if notas_raw and notas_raw.lower() != "sin notas":
                for x in notas_raw.replace(";", ",").split(","):
                    val = x.strip()
                    if val:
                        notas.append(float(val))
            estudiantes.append(Estudiante(cod, nom, 0.0, notas))
        except (ValueError, TypeError):
            continue

    return estudiantes

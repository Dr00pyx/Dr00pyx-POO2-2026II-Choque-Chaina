from __future__ import annotations
import os
import sys
import json
from pathlib import Path

from estudiante import Estudiante
from estrategias import PromedioSimple
from repositorios import RepositorioJSON
from servicios import ServicioEstudiante
from pyqt5_app import ModeloAcademico, VistaEstudiantes
from PyQt5.QtWidgets import QApplication


def demo_actividad_1_tkinter() -> None:
    print("=" * 60)
    print("DEMOSTRACION ACTIVIDAD 1A — TKINTER CRUD COMPLETO")
    print("=" * 60)

    ruta_json = "datos.json"
    if os.path.exists(ruta_json):
        os.remove(ruta_json)

    repo = RepositorioJSON(ruta_json)
    svc = ServicioEstudiante(repo, PromedioSimple())

    print("\n[1] Registrando 3 estudiantes...")
    estudiantes = [
        Estudiante(1001, "Juan Perez", 0.0, [15.0, 18.0, 14.0]),
        Estudiante(1002, "Maria Gomez", 0.0, [8.0, 9.5, 10.0]),
        Estudiante(1003, "Carlos Quispe", 0.0, [16.0, 17.0, 14.5])
    ]

    for e in estudiantes:
        svc.registrar(e)
        ppa_str = f"{e.ppa:.2f}" if e.notas else "sin notas"
        print(f"  -> Registrado: [{e.codigo:04d}] {e.nombre:<20} PPA: {ppa_str}")

    print("\n[2] Contenido de 'datos.json' tras registro:")
    with open(ruta_json, "r", encoding="utf-8") as f:
        print(json.dumps(json.load(f), indent=2))

    print("\n[3] Buscando estudiante con código 1001 (ADICIONAL):")
    encontrado = svc.buscar(1001)
    if encontrado:
        print(f"  -> Encontrado: [{encontrado.codigo:04d}] {encontrado.nombre} con PPA {encontrado.ppa:.2f}")

    print("\n[4] Eliminando estudiante 1002...")
    svc.eliminar(1002)
    print("  -> Estudiante 1002 eliminado.")

    print("\n[5] Lista de estudiantes tras eliminacion:")
    for e in svc.listar():
        print(f"  -> [{e.codigo:04d}] {e.nombre:<20} PPA: {e.ppa:.2f}")


def demo_actividad_2_pyqt5() -> None:
    print("\n" + "=" * 60)
    print("DEMOSTRACION ACTIVIDAD 2A — PYQT5 SIGNAL / SLOT (OBSERVER)")
    print("=" * 60)

    qt_app = QApplication.instance() or QApplication(sys.argv)
    ruta_json = "datos.json"

    repo = RepositorioJSON(ruta_json)
    svc = ServicioEstudiante(repo, PromedioSimple())
    modelo = ModeloAcademico(svc)

    vista = VistaEstudiantes(modelo)

    print("\n[1] Conexiones Observer Signal/Slot:")
    print("  -> modelo.estudiante_guardado -> vista._on_estudiante_guardado")
    print("  -> modelo.estudiante_eliminado -> vista._on_estudiante_eliminado")

    print("\n[2] Agregando estudiante desaprobado para verificar formato de color:")
    e_desaprobado = Estudiante(1004, "Ana Flores", 0.0, [7.0, 8.5, 9.0])
    modelo.registrar(e_desaprobado)
    print(f"  -> Registrado vía Modelo: [{e_desaprobado.codigo}] {e_desaprobado.nombre} PPA: {e_desaprobado.ppa:.2f}")

    print(f"  -> Filas en la tabla QTableWidget: {vista._tbl.rowCount()}")
    for row in range(vista._tbl.rowCount()):
        cod = vista._tbl.item(row, 0).text()
        nom = vista._tbl.item(row, 1).text()
        ppa_item = vista._tbl.item(row, 2)
        color = ppa_item.foreground().color().name().upper()
        print(f"     Fila {row}: Cod={cod}, Nombre={nom}, PPA={ppa_item.text()} (Color: {color})")

    print("\n[3] Eliminando estudiante vía botón 'Eliminar' (ADICIONAL):")
    vista._tbl.selectRow(vista._tbl.rowCount() - 1)
    vista._eliminar()
    print("  -> Estudiante eliminado mediante signal 'estudiante_eliminado'.")
    print(f"  -> Filas restantes en la tabla: {vista._tbl.rowCount()}")

    vista.close()


def demo_reto_exportacion_excel() -> None:
    print("\n" + "=" * 60)
    print("DEMOSTRACION RETO — EXPORTACION A ARCHIVO EXCEL (.XLSX)")
    print("=" * 60)

    ruta_json = "datos.json"
    repo = RepositorioJSON(ruta_json)
    svc = ServicioEstudiante(repo, PromedioSimple())

    svc.registrar(Estudiante(1005, "Manuel Choque", 0.0, [17.0, 18.0, 16.5]))
    svc.registrar(Estudiante(1006, "Diana Quispe", 0.0, [8.0, 9.0, 7.5]))

    ruta_excel = "estudiantes_exportados.xlsx"
    ruta_generada = svc.exportar_excel(ruta_excel)
    print(f"\n[1] Archivo Excel generado: {ruta_generada}")
    print(f"  -> Existe en disco: {os.path.exists(ruta_generada)}")
    print(f"  -> Tamaño del archivo: {os.path.getsize(ruta_generada)} bytes")

    import openpyxl
    wb = openpyxl.load_workbook(ruta_generada)
    ws = wb.active
    print(f"  -> Hoja activa: {ws.title}")
    print("  -> Contenido de las filas exportadas en Excel:")
    for row in ws.iter_rows(values_only=True):
        print(f"     {row}")


if __name__ == "__main__":
    demo_actividad_1_tkinter()
    demo_actividad_2_pyqt5()
    demo_reto_exportacion_excel()
    print("\n" + "=" * 60)
    print("TODAS LAS DEMOSTRACIONES FINALIZARON CON EXITO")
    print("=" * 60)

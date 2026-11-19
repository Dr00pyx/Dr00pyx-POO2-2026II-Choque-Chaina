from __future__ import annotations
import os
import sys
import unittest
from pathlib import Path
import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from estudiante import Estudiante
from estrategias import PromedioSimple
from repositorios import RepositorioJSON
from servicios import ServicioEstudiante
from app_tkinter import AppEstudiantes

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from pyqt5_app import ModeloAcademico, VistaEstudiantes


class TestSistemaAcademico(unittest.TestCase):
    def setUp(self) -> None:
        self.test_json = "test_datos.json"
        self.test_excel = "test_export.xlsx"
        self._limpiar_archivos()

    def tearDown(self) -> None:
        self._limpiar_archivos()

    def _limpiar_archivos(self) -> None:
        for f in [self.test_json, self.test_excel, "test_tk_excel.xlsx", "test_qt_excel.xlsx"]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except Exception:
                    pass

    def test_servicio_y_repositorio_json(self) -> None:
        repo = RepositorioJSON(self.test_json)
        calc = PromedioSimple()
        svc = ServicioEstudiante(repo, calc)

        e1 = Estudiante(1001, "Carlos Condori", 0.0, [15.0, 18.0, 14.0])
        svc.registrar(e1)
        self.assertAlmostEqual(e1.ppa, 15.6666666, places=2)

        e2 = Estudiante(1002, "Ana Mamani", 0.0, [8.0, 9.0, 10.0])
        svc.registrar(e2)
        self.assertAlmostEqual(e2.ppa, 9.0, places=2)

        estudiantes = svc.listar()
        self.assertEqual(len(estudiantes), 2)

        buscado = svc.buscar(1001)
        self.assertIsNotNone(buscado)
        self.assertEqual(buscado.nombre, "Carlos Condori")

        svc.eliminar(1001)
        self.assertEqual(len(svc.listar()), 1)
        self.assertIsNone(svc.buscar(1001))

    def test_actividad_1a_tkinter_crud_y_busqueda(self) -> None:
        app = AppEstudiantes(self.test_json)
        app.withdraw()

        app._ent_cod.insert(0, "1001")
        app._ent_nom.insert(0, "Juan Perez")
        app._ent_notas.insert(0, "15, 18, 14")
        app._registrar()

        app._ent_cod.insert(0, "1002")
        app._ent_nom.insert(0, "Maria Lopez")
        app._ent_notas.insert(0, "8, 9, 10")
        app._registrar()

        app._ent_cod.insert(0, "1003")
        app._ent_nom.insert(0, "Pedro Quispe")
        app._ent_notas.insert(0, "16, 17, 18")
        app._registrar()

        self.assertEqual(app._lb.size(), 3)
        item0 = app._lb.get(0)
        self.assertIn("1001", item0)
        self.assertIn("Juan Perez", item0)
        self.assertIn("15.67", item0)

        app._ent_buscar.insert(0, "1001")
        app._buscar()
        self.assertEqual(app._lb.size(), 1)
        self.assertIn("Juan Perez", app._lb.get(0))

        app._actualizar_lista()
        self.assertEqual(app._lb.size(), 3)

        app._lb.selection_set(0)
        app._eliminar()
        self.assertEqual(app._lb.size(), 2)
        self.assertIsNone(app._svc.buscar(1001))

        app._exportar_excel("test_tk_excel.xlsx")
        self.assertTrue(os.path.exists("test_tk_excel.xlsx"))

        app.destroy()

    def test_actividad_2a_pyqt5_signal_slot_y_eliminar(self) -> None:
        qt_app = QApplication.instance() or QApplication(sys.argv)

        repo = RepositorioJSON(self.test_json)
        svc = ServicioEstudiante(repo, PromedioSimple())
        modelo = ModeloAcademico(svc)

        senales_guardado = []
        senales_eliminado = []
        modelo.estudiante_guardado.connect(lambda e: senales_guardado.append(e))
        modelo.estudiante_eliminado.connect(lambda cod: senales_eliminado.append(cod))

        vista = VistaEstudiantes(modelo)

        estudiantes_data = [
            ("1001", "Lucia Flores", "15, 18, 14"),
            ("1002", "Raul Ramos", "8, 9, 10"),
            ("1003", "Elena Vargas", "16, 17, 18")
        ]

        for cod, nom, notas in estudiantes_data:
            vista._ed_cod.setText(cod)
            vista._ed_nom.setText(nom)
            vista._ed_notas.setText(notas)
            vista._registrar()

        self.assertEqual(len(senales_guardado), 3)
        self.assertEqual(vista._tbl.rowCount(), 3)

        item_ppa_aprobado = vista._tbl.item(0, 2)
        self.assertEqual(item_ppa_aprobado.text(), "15.67")

        item_ppa_desaprobado = vista._tbl.item(1, 2)
        self.assertEqual(item_ppa_desaprobado.text(), "9.00")
        color_rojo = item_ppa_desaprobado.foreground().color()
        self.assertEqual(color_rojo.name().upper(), "#C00000")

        vista._tbl.selectRow(1)
        vista._eliminar()

        self.assertEqual(len(senales_eliminado), 1)
        self.assertEqual(senales_eliminado[0], 1002)
        self.assertEqual(vista._tbl.rowCount(), 2)
        self.assertIsNone(modelo.buscar(1002))

        vista._exportar_excel("test_qt_excel.xlsx")
        self.assertTrue(os.path.exists("test_qt_excel.xlsx"))

        vista.close()

    def test_exportar_excel_formato_y_datos(self) -> None:
        repo = RepositorioJSON(self.test_json)
        svc = ServicioEstudiante(repo, PromedioSimple())

        svc.registrar(Estudiante(1001, "Estudiante Aprobado", 0.0, [15, 16, 17]))
        svc.registrar(Estudiante(1002, "Estudiante Desaprobado", 0.0, [6, 8, 9]))

        ruta_salida = svc.exportar_excel(self.test_excel)
        self.assertTrue(os.path.exists(ruta_salida))

        wb = openpyxl.load_workbook(ruta_salida)
        ws = wb.active
        self.assertEqual(ws.title, "Estudiantes UNAP")

        headers = [ws.cell(1, c).value for c in range(1, 6)]
        self.assertEqual(headers, ["Código", "Nombre", "PPA", "Notas", "Estado"])

        self.assertEqual(ws.cell(2, 1).value, 1001)
        self.assertEqual(ws.cell(2, 2).value, "Estudiante Aprobado")
        self.assertEqual(ws.cell(2, 5).value, "Aprobado")

        self.assertEqual(ws.cell(3, 1).value, 1002)
        self.assertEqual(ws.cell(3, 5).value, "Desaprobado")
        color_ppa = str(ws.cell(3, 3).font.color.rgb)
        self.assertTrue(color_ppa.endswith("C00000"))

    def test_separacion_mvc(self) -> None:
        qt_app = QApplication.instance() or QApplication(sys.argv)
        repo = RepositorioJSON(self.test_json)
        svc = ServicioEstudiante(repo, PromedioSimple())
        modelo = ModeloAcademico(svc)
        vista = VistaEstudiantes(modelo)

        self.assertFalse(hasattr(vista, "_repo"))
        self.assertTrue(hasattr(vista, "_mod"))
        self.assertFalse(hasattr(vista._mod, "_repo"))
        self.assertTrue(hasattr(vista._mod, "_svc"))
        self.assertTrue(hasattr(vista._mod._svc, "_repo"))
        vista.close()


if __name__ == "__main__":
    unittest.main()

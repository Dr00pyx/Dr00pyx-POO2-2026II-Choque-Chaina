from __future__ import annotations
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLineEdit,
    QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView,
    QFileDialog
)
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QColor
from estudiante import Estudiante


class ModeloAcademico(QObject):
    estudiante_guardado = pyqtSignal(object)
    estudiante_eliminado = pyqtSignal(int)

    def __init__(self, svc) -> None:
        super().__init__()
        self._svc = svc

    def registrar(self, e: Estudiante) -> None:
        self._svc.registrar(e)
        self.estudiante_guardado.emit(e)

    def eliminar(self, cod: int) -> None:
        self._svc.eliminar(cod)
        self.estudiante_eliminado.emit(cod)

    def listar(self):
        return self._svc.listar()

    def buscar(self, cod: int):
        return self._svc.buscar(cod)

    def exportar_excel(self, ruta: str = "estudiantes.xlsx") -> str:
        return self._svc.exportar_excel(ruta)


class VistaEstudiantes(QMainWindow):
    def __init__(self, modelo: ModeloAcademico) -> None:
        super().__init__()
        self._mod = modelo
        self.setWindowTitle("SIS206 — Sistema Académico UNAP")
        self.resize(860, 520)
        self._construir_ui()

        self._mod.estudiante_guardado.connect(self._on_estudiante_guardado)
        self._mod.estudiante_eliminado.connect(self._on_estudiante_eliminado)
        self._recargar_tabla()

    def _construir_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Código:"))
        self._ed_cod = QLineEdit()
        self._ed_cod.setMaximumWidth(80)
        hbox.addWidget(self._ed_cod)

        hbox.addWidget(QLabel("Nombre:"))
        self._ed_nom = QLineEdit()
        hbox.addWidget(self._ed_nom)

        hbox.addWidget(QLabel("Notas (,):"))
        self._ed_notas = QLineEdit()
        self._ed_notas.setMaximumWidth(140)
        hbox.addWidget(self._ed_notas)

        btn_reg = QPushButton("Registrar")
        btn_reg.clicked.connect(self._registrar)
        hbox.addWidget(btn_reg)

        btn_elim = QPushButton("Eliminar")
        btn_elim.clicked.connect(self._eliminar)
        hbox.addWidget(btn_elim)

        btn_excel = QPushButton("Exportar Excel")
        btn_excel.clicked.connect(self._exportar_excel)
        hbox.addWidget(btn_excel)

        layout.addLayout(hbox)

        self._tbl = QTableWidget(0, 4)
        self._tbl.setHorizontalHeaderLabels(["Código", "Nombre", "PPA", "Notas"])
        self._tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self._tbl)

    def _registrar(self) -> None:
        try:
            cod = int(self._ed_cod.text())
            nom = self._ed_nom.text().strip()
            if not nom:
                raise ValueError("Nombre vacío")
            raw = self._ed_notas.text().strip()
            notas = [float(x) for x in raw.split(",") if x.strip()] if raw else []
            self._mod.registrar(Estudiante(cod, nom, 0.0, notas))
            self._ed_cod.clear()
            self._ed_nom.clear()
            self._ed_notas.clear()
        except ValueError as ex:
            QMessageBox.critical(self, "Error", str(ex))

    def _eliminar(self) -> None:
        row = self._tbl.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Seleccione un estudiante")
            return
        cod_item = self._tbl.item(row, 0)
        if cod_item:
            cod = int(cod_item.text())
            self._mod.eliminar(cod)

    def _exportar_excel(self, ruta: str | None = None) -> str | None:
        mostrar_dialogo = False
        if not ruta:
            mostrar_dialogo = True
            ruta, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar a Excel",
                "estudiantes.xlsx",
                "Archivos Excel (*.xlsx)"
            )
        if ruta:
            try:
                ruta_res = self._mod.exportar_excel(ruta)
                if mostrar_dialogo:
                    QMessageBox.information(self, "Éxito", f"Estudiantes exportados exitosamente a:\n{ruta_res}")
                return ruta_res
            except Exception as ex:
                if mostrar_dialogo:
                    QMessageBox.critical(self, "Error", f"No se pudo exportar a Excel:\n{str(ex)}")
                else:
                    raise ex
        return None

    def _on_estudiante_guardado(self, e: Estudiante) -> None:
        self._recargar_tabla()

    def _on_estudiante_eliminado(self, cod: int) -> None:
        self._recargar_tabla()

    def _recargar_tabla(self) -> None:
        self._tbl.setRowCount(0)
        for e in self._mod.listar():
            r = self._tbl.rowCount()
            self._tbl.insertRow(r)
            self._tbl.setItem(r, 0, QTableWidgetItem(str(e.codigo)))
            self._tbl.setItem(r, 1, QTableWidgetItem(e.nombre))
            ppa_item = QTableWidgetItem(f"{e.ppa:.2f}")
            if e.ppa < 10.5:
                ppa_item.setForeground(QColor("#C00000"))
            self._tbl.setItem(r, 2, ppa_item)
            self._tbl.setItem(r, 3, QTableWidgetItem(str(e.notas)))


if __name__ == "__main__":
    from servicios import ServicioEstudiante
    from estrategias import PromedioSimple
    from repositorios import RepositorioJSON

    app = QApplication(sys.argv)
    svc = ServicioEstudiante(RepositorioJSON("datos.json"), PromedioSimple())
    mod = ModeloAcademico(svc)
    vista = VistaEstudiantes(mod)
    vista.show()
    sys.exit(app.exec_())

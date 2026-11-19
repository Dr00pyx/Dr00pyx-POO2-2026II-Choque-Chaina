from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from servicios import ServicioEstudiante
from estrategias import PromedioSimple
from repositorios import RepositorioJSON
from estudiante import Estudiante


class AppEstudiantes(tk.Tk):
    def __init__(self, ruta_json: str = "datos.json") -> None:
        super().__init__()
        self.title("SIS206 — Sistema Académico UNAP")
        self.geometry("860x520")
        self.resizable(True, True)

        self._svc = ServicioEstudiante(
            RepositorioJSON(ruta_json),
            PromedioSimple()
        )
        self._construir_ui()
        self._actualizar_lista()

    def _construir_ui(self) -> None:
        frm_top = ttk.LabelFrame(self, text="Registrar Estudiante", padding=8)
        frm_top.pack(fill="x", padx=8, pady=4)

        ttk.Label(frm_top, text="Código:").grid(row=0, column=0, sticky="e")
        self._ent_cod = ttk.Entry(frm_top, width=8)
        self._ent_cod.grid(row=0, column=1, padx=4)

        ttk.Label(frm_top, text="Nombre:").grid(row=0, column=2, sticky="e")
        self._ent_nom = ttk.Entry(frm_top, width=24)
        self._ent_nom.grid(row=0, column=3, padx=4)

        ttk.Label(frm_top, text="Notas (,):").grid(row=0, column=4, sticky="e")
        self._ent_notas = ttk.Entry(frm_top, width=16)
        self._ent_notas.grid(row=0, column=5, padx=4)

        ttk.Button(frm_top, text="Registrar", command=self._registrar).grid(row=0, column=6, padx=4)
        ttk.Button(frm_top, text="Eliminar", command=self._eliminar).grid(row=0, column=7, padx=4)
        ttk.Button(frm_top, text="Exportar Excel", command=self._exportar_excel).grid(row=0, column=8, padx=4)

        frm_search = ttk.Frame(self, padding=4)
        frm_search.pack(fill="x", padx=8, pady=2)
        ttk.Label(frm_search, text="Buscar por Código:").pack(side="left", padx=4)
        self._ent_buscar = ttk.Entry(frm_search, width=10)
        self._ent_buscar.pack(side="left", padx=4)
        ttk.Button(frm_search, text="Buscar", command=self._buscar).pack(side="left", padx=4)
        ttk.Button(frm_search, text="Restablecer", command=self._actualizar_lista).pack(side="left", padx=4)

        frm_bot = ttk.LabelFrame(self, text="Estudiantes", padding=4)
        frm_bot.pack(fill="both", expand=True, padx=8, pady=4)

        self._lb = tk.Listbox(frm_bot, font=("Courier New", 11), selectmode=tk.SINGLE)
        sb = ttk.Scrollbar(frm_bot, orient="vertical", command=self._lb.yview)
        self._lb.configure(yscrollcommand=sb.set)
        self._lb.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    def _registrar(self) -> None:
        try:
            cod = int(self._ent_cod.get())
            nom = self._ent_nom.get().strip()
            if not nom:
                raise ValueError("Nombre vacío")
            raw = self._ent_notas.get().strip()
            notas = [float(x) for x in raw.split(",") if x.strip()] if raw else []
            e = Estudiante(cod, nom, 0.0, notas)
            self._svc.registrar(e)
            self._actualizar_lista()
            self._ent_cod.delete(0, "end")
            self._ent_nom.delete(0, "end")
            self._ent_notas.delete(0, "end")
        except ValueError as ex:
            messagebox.showerror("Error", str(ex))

    def _eliminar(self) -> None:
        sel = self._lb.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un estudiante")
            return
        texto = self._lb.get(sel[0])
        cod = int(texto[1:5])
        self._svc.eliminar(cod)
        self._actualizar_lista()

    def _buscar(self) -> None:
        raw_cod = self._ent_buscar.get().strip()
        if not raw_cod:
            self._actualizar_lista()
            return
        try:
            cod = int(raw_cod)
            e = self._svc.buscar(cod)
            self._lb.delete(0, "end")
            if e:
                ppa_str = f"{e.ppa:.2f}" if e.notas else "sin notas"
                self._lb.insert("end", f"[{e.codigo:04d}] {e.nombre:<28} PPA: {ppa_str}")
            else:
                messagebox.showinfo("Búsqueda", f"No se encontró estudiante con código {cod}")
                self._actualizar_lista()
        except ValueError:
            messagebox.showerror("Error", "El código debe ser un número entero")

    def _actualizar_lista(self) -> None:
        self._lb.delete(0, "end")
        for e in self._svc.listar():
            ppa_str = f"{e.ppa:.2f}" if e.notas else "sin notas"
            self._lb.insert("end", f"[{e.codigo:04d}] {e.nombre:<28} PPA: {ppa_str}")

    def _exportar_excel(self, ruta: str | None = None) -> str | None:
        mostrar_dialogo = False
        if not ruta:
            mostrar_dialogo = True
            ruta = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos Excel", "*.xlsx")],
                initialfile="estudiantes.xlsx"
            )
        if ruta:
            try:
                ruta_res = self._svc.exportar_excel(ruta)
                if mostrar_dialogo:
                    messagebox.showinfo("Éxito", f"Estudiantes exportados exitosamente a:\n{ruta_res}")
                return ruta_res
            except Exception as ex:
                if mostrar_dialogo:
                    messagebox.showerror("Error", f"No se pudo exportar a Excel:\n{str(ex)}")
                else:
                    raise ex
        return None


if __name__ == "__main__":
    AppEstudiantes().mainloop()

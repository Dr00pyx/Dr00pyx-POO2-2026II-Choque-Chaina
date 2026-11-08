"""
Producto Concreto 2: Repositorio en Archivo Plano JSON.
Persistencia en formato estructurado para backups o entornos locales.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from .modelo import Estudiante
from .repositorio import RepositorioEstudiantes


class RepositorioArchivoJSON(RepositorioEstudiantes):
    def __init__(self, ruta_archivo: str | Path = "estudiantes.json") -> None:
        self.ruta_archivo = Path(ruta_archivo)
        self._asegurar_archivo()

    def _asegurar_archivo(self) -> None:
        if not self.ruta_archivo.exists():
            try:
                with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                    json.dump([], f)
            except Exception:
                pass

    def _leer_todos(self) -> Dict[str, Estudiante]:
        if not self.ruta_archivo.exists():
            return {}
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {item["codigo"]: Estudiante.from_dict(item) for item in data}
        except Exception:
            return {}

    def _escribir_todos(self, estudiantes: Dict[str, Estudiante]) -> bool:
        try:
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                data = [est.to_dict() for est in estudiantes.values()]
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def guardar(self, estudiante: Estudiante) -> bool:
        items = self._leer_todos()
        items[estudiante.codigo] = estudiante
        return self._escribir_todos(items)

    def buscar_por_codigo(self, codigo: str) -> Optional[Estudiante]:
        items = self._leer_todos()
        return items.get(codigo)

    def listar_todos(self) -> List[Estudiante]:
        items = self._leer_todos()
        return list(items.values())

    def eliminar(self, codigo: str) -> bool:
        items = self._leer_todos()
        if codigo in items:
            del items[codigo]
            return self._escribir_todos(items)
        return False

    @property
    def tipo_almacenamiento(self) -> str:
        return f"Archivo JSON ({self.ruta_archivo.name})"

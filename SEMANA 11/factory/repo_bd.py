"""
Producto Concreto 3: Repositorio en Base de Datos Relacional SQLite.
Persistencia ACID estándar para entornos de producción o integración.
"""
from pathlib import Path
import sqlite3
from typing import List, Optional
from .modelo import Estudiante
from .repositorio import RepositorioEstudiantes


class RepositorioSQLite(RepositorioEstudiantes):
    def __init__(self, ruta_db: str | Path = "academico_unap.db") -> None:
        self.ruta_db = str(ruta_db)
        self._inicializar_tabla()

    def _conectar(self) -> sqlite3.Connection:
        return sqlite3.connect(self.ruta_db)

    def _inicializar_tabla(self) -> None:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estudiantes (
                    codigo TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    carrera TEXT NOT NULL,
                    promedio REAL NOT NULL,
                    semestre TEXT NOT NULL
                );
            """)
            conn.commit()

    def guardar(self, estudiante: Estudiante) -> bool:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO estudiantes (codigo, nombre, carrera, promedio, semestre)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(codigo) DO UPDATE SET
                    nombre=excluded.nombre,
                    carrera=excluded.carrera,
                    promedio=excluded.promedio,
                    semestre=excluded.semestre;
            """, (estudiante.codigo, estudiante.nombre, estudiante.carrera, estudiante.promedio, estudiante.semestre))
            conn.commit()
            return True

    def buscar_por_codigo(self, codigo: str) -> Optional[Estudiante]:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, nombre, carrera, promedio, semestre FROM estudiantes WHERE codigo = ?", (codigo,))
            row = cursor.fetchone()
            if row:
                return Estudiante(codigo=row[0], nombre=row[1], carrera=row[2], promedio=row[3], semestre=row[4])
        return None

    def listar_todos(self) -> List[Estudiante]:
        resultado = []
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, nombre, carrera, promedio, semestre FROM estudiantes")
            for row in cursor.fetchall():
                resultado.append(Estudiante(codigo=row[0], nombre=row[1], carrera=row[2], promedio=row[3], semestre=row[4]))
        return resultado

    def eliminar(self, codigo: str) -> bool:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM estudiantes WHERE codigo = ?", (codigo,))
            conn.commit()
            return cursor.rowcount > 0

    @property
    def tipo_almacenamiento(self) -> str:
        return f"Base de Datos SQLite ({Path(self.ruta_db).name})"

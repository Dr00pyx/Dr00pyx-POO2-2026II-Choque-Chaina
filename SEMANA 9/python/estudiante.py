# estudiante.py — Clase Estudiante con Python 3.12+ y @dataclass
from dataclasses import dataclass, field, asdict
import json
from typing import Optional


@dataclass
class Estudiante:
    codigo: int
    nombre: str
    ppa: float
    ciclo: int
    notas: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.codigo <= 0:
            raise ValueError("Codigo debe ser positivo")
        if not self.nombre.strip():
            raise ValueError("Nombre no puede estar vacio")
        if not (0.0 <= self.ppa <= 20.0):
            raise ValueError("PPA debe estar entre 0 y 20")

    def agregar_nota(self, nota: float) -> None:
        if not (0.0 <= nota <= 20.0):
            raise ValueError(f"Nota {nota} fuera de rango")
        self.notas.append(nota)

    def calcular_promedio(self) -> Optional[float]:
        if not self.notas:
            return None
        return sum(self.notas) / len(self.notas)

    def es_aprobado(self) -> bool:
        """Determina si el estudiante esta aprobado segun su PPA (>= 11.0)."""
        return self.ppa >= 11.0

    def __str__(self) -> str:
        return f"[{self.codigo}] {self.nombre} - PPA: {self.ppa} - Ciclo: {self.ciclo}"


def ejecutar_casos_de_prueba_assert():
    """Ejecuta los 3 casos de prueba con assert solicitados en la Actividad 2B."""
    print("\n--- Ejecutando 3 casos de prueba con assert (validaciones) ---")

    # Caso 1: Codigo invalido (<= 0)
    codigo_fallo = False
    try:
        Estudiante(codigo=0, nombre="Pedro Castillo", ppa=14.0, ciclo=2)
    except ValueError as e:
        assert str(e) == "Codigo debe ser positivo", f"Mensaje inesperado: {e}"
        codigo_fallo = True
    assert codigo_fallo, "Fallo: deberia haber lanzado ValueError por codigo no positivo"
    print("[OK] Caso de prueba 1 superado: Codigo <= 0 lanza ValueError correctamente.")

    # Caso 2: Nombre vacio o con solo espacios
    nombre_fallo = False
    try:
        Estudiante(codigo=1002, nombre="   ", ppa=15.0, ciclo=3)
    except ValueError as e:
        assert str(e) == "Nombre no puede estar vacio", f"Mensaje inesperado: {e}"
        nombre_fallo = True
    assert nombre_fallo, "Fallo: deberia haber lanzado ValueError por nombre vacio"
    print("[OK] Caso de prueba 2 superado: Nombre vacio lanza ValueError correctamente.")

    # Caso 3: PPA invalido (< 0 o > 20)
    ppa_fallo = False
    try:
        Estudiante(codigo=1003, nombre="Lucia Mendez", ppa=21.5, ciclo=4)
    except ValueError as e:
        assert str(e) == "PPA debe estar entre 0 y 20", f"Mensaje inesperado: {e}"
        ppa_fallo = True
    assert ppa_fallo, "Fallo: deberia haber lanzado ValueError por PPA fuera de rango"
    print("[OK] Caso de prueba 3 superado: PPA > 20 lanza ValueError correctamente.")

    print("=> TODOS LOS ASSERTS PASARON SATISFACTORIAMENTE.")


# Uso y ejecucion principal:
if __name__ == "__main__":
    print("=== SIS206 - POO II | Practica S09: Python 3.12+ ===")
    
    # 1. Ejemplo original de la guia de practica (Pagina 6)
    print("\n--- Salida Original de la Guia ---")
    e = Estudiante(1001, "Ana Quispe", 15.5, 3)
    for nota in [14.0, 16.0, 18.0]:
        e.agregar_nota(nota)
    print(e)
    print(f"Promedio semestral: {e.calcular_promedio():.1f}")
    
    # Prueba de validacion original
    try:
        Estudiante(-1, "X", 5.0, 1)
    except ValueError as ex:
        print(f"Error esperado: {ex}")

    # 2. Requerimiento Actividad 2B: Agregar 5 notas distintas y mostrar promedio con 2 decimales
    print("\n--- Actividad 2B: 5 notas distintas y promedio con 2 decimales ---")
    estudiante2 = Estudiante(1005, "Manuel Condori", 16.8, 5)
    notas_distintas = [13.5, 15.0, 17.5, 18.0, 16.25]
    for n in notas_distintas:
        estudiante2.agregar_nota(n)

    promedio_2dec = estudiante2.calcular_promedio()
    print(f"Estudiante: {estudiante2}")
    print(f"Notas agregadas ({len(notas_distintas)}): {estudiante2.notas}")
    print(f"Promedio semestral con 2 decimales: {promedio_2dec:.2f}")

    # 3. Requerimiento Actividad 2B: 3 casos de prueba con assert
    ejecutar_casos_de_prueba_assert()

    # 4. Requerimiento ADICIONAL Actividad 2B: Serializacion a JSON con dataclasses.asdict()
    print("\n--- Requerimiento ADICIONAL: Serializacion JSON con dataclasses.asdict() ---")
    # Serializamos a 'e' (Ana Quispe) y a 'estudiante2'
    diccionario_estudiante = asdict(e)
    json_serializado = json.dumps(diccionario_estudiante, indent=4, ensure_ascii=False)
    print("Objeto Ana Quispe serializado en JSON:")
    print(json_serializado)

    print("\nObjeto Manuel Condori serializado en JSON:")
    print(json.dumps(asdict(estudiante2), indent=4, ensure_ascii=False))

    print("\n[FIN ACTIVIDAD 2B - PYTHON COMPLETADO EXITOSAMENTE]")

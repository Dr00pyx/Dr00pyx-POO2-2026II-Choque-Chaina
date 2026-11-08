"""
test_solid.py — Pruebas unitarias automatizadas para la refactorización SOLID en Python
"""

import unittest
from solid_s10 import (
    Estudiante,
    PromedioSimple,
    PromedioModerado,
    RepositorioMemoria,
    RepositorioCsv,
    ServicioEstudiante,
)


class TestSolidPracticaS10(unittest.TestCase):

    def setUp(self):
        self.repo_mem = RepositorioMemoria()
        self.calc_simple = PromedioSimple()
        self.calc_moderado = PromedioModerado()

    def test_promedio_simple(self):
        notas = [14.0, 20.0, 16.0, 18.0, 12.0]
        # (14 + 20 + 16 + 18 + 12) / 5 = 80 / 5 = 16.0
        self.assertAlmostEqual(self.calc_simple.calcular(notas), 16.0, places=3)

    def test_promedio_simple_vacio(self):
        self.assertEqual(self.calc_simple.calcular([]), 0.0)

    def test_promedio_moderado_oficial(self):
        # Caso de la guía: Ana Quispe
        notas = [14.0, 20.0, 16.0, 18.0, 12.0]
        # Ordenado: 12, 14, 16, 18, 20 -> descarta 12 y 20 -> (14 + 16 + 18)/3 = 16.0
        self.assertAlmostEqual(self.calc_moderado.calcular(notas), 16.0, places=3)

    def test_promedio_moderado_diferencia_extremos(self):
        notas = [5.0, 15.0, 16.0, 17.0, 20.0]
        # Promedio simple: 73 / 5 = 14.6
        # Promedio moderado: descarta 5 y 20 -> (15+16+17)/3 = 16.0
        self.assertAlmostEqual(self.calc_simple.calcular(notas), 14.6, places=3)
        self.assertAlmostEqual(self.calc_moderado.calcular(notas), 16.0, places=3)

    def test_promedio_moderado_pocos_elementos(self):
        self.assertEqual(self.calc_moderado.calcular([15.0]), 0.0)
        self.assertEqual(self.calc_moderado.calcular([15.0, 18.0]), 0.0)

    def test_servicio_estudiante_con_memoria(self):
        svc = ServicioEstudiante(self.repo_mem, self.calc_simple)
        est = Estudiante(codigo=202101, nombre="Carlos Condori", notas=[15.0, 17.5, 13.0, 16.5])
        svc.registrar(est)

        recuperado = svc.buscar(202101)
        self.assertIsNotNone(recuperado)
        self.assertEqual(recuperado.codigo, 202101)
        self.assertEqual(recuperado.nombre, "Carlos Condori")
        self.assertAlmostEqual(recuperado.ppa, 15.5, places=3)

    def test_servicio_estudiante_ocp(self):
        # Demostrar que podemos cambiar de PromedioSimple a PromedioModerado
        # sin modificar ServicioEstudiante
        svc_mod = ServicioEstudiante(self.repo_mem, self.calc_moderado)
        est = Estudiante(codigo=1001, nombre="Ana Quispe", notas=[14.0, 20.0, 16.0, 18.0, 12.0])
        svc_mod.registrar(est)

        recuperado = svc_mod.buscar(1001)
        self.assertIsNotNone(recuperado)
        self.assertAlmostEqual(recuperado.ppa, 16.0, places=3)

    def test_repositorio_csv(self):
        repo_csv = RepositorioCsv("test_estudiantes.csv")
        svc_csv = ServicioEstudiante(repo_csv, self.calc_simple)
        est = Estudiante(codigo=9999, nombre="Test Persistencia", notas=[18.0, 20.0])
        svc_csv.registrar(est)

        # Leer con otra instancia del repositorio para verificar lectura de disco
        repo_csv_recarga = RepositorioCsv("test_estudiantes.csv")
        recuperado = repo_csv_recarga.buscar(9999)
        self.assertIsNotNone(recuperado)
        self.assertEqual(recuperado.nombre, "Test Persistencia")
        self.assertAlmostEqual(recuperado.ppa, 19.0, places=2)


if __name__ == "__main__":
    unittest.main()

"""
Prueba de Persistencia Real para RepositorioJSON.
Verifica que los datos persistan a través del ciclo de vida de múltiples instancias y reinicios.
Actividad 1 y 1A — Semana 13
"""
import os
import pathlib
from repositorio_json import RepositorioJSON
from estudiante import Estudiante

RUTA = "/tmp/estudiantes_test.json"


def test_persistencia_entre_instancias():
    """Verifica que los datos guardados en r1 sean legibles desde r2."""
    # Primera instancia: guardar dos estudiantes
    r1 = RepositorioJSON(RUTA)
    r1.guardar(Estudiante(1001, "Ana Quispe", 15.5, [14.0, 18.0, 14.5]))
    r1.guardar(Estudiante(1002, "Juan Mamani", 12.0, [10.0, 12.0, 14.0]))

    # Segunda instancia: verificar que los datos persisten desde disco
    r2 = RepositorioJSON(RUTA)
    ana = r2.buscar(1001)
    assert ana is not None
    assert ana.nombre == "Ana Quispe"
    assert abs(ana.ppa - 15.5) < 0.01

    juan = r2.buscar(1002)
    assert juan is not None
    assert len(r2.listar()) == 2

    # Limpiar archivo de prueba
    if os.path.exists(RUTA):
        os.remove(RUTA)
    if os.path.exists(r1.ruta):
        os.remove(r1.ruta)


def test_eliminar_actualiza_archivo():
    """
    ADICIONAL Actividad 1A:
    Verifica que el método eliminar(cod) remueva la entidad y actualice el archivo en disco.
    """
    ruta_test = "/tmp/estudiantes_eliminar_test.json"
    r1 = RepositorioJSON(ruta_test)
    r1.guardar(Estudiante(2001, "Carlos Condori", 16.0, [16.0, 16.0]))
    r1.guardar(Estudiante(2002, "Elena Ramos", 14.0, [14.0, 14.0]))
    assert len(r1.listar()) == 2

    # Eliminar estudiante 2001
    r1.eliminar(2001)
    assert r1.buscar(2001) is None
    assert len(r1.listar()) == 1

    # Crear nueva instancia para comprobar que el cambio se escribió físicamente en disco
    r2 = RepositorioJSON(ruta_test)
    assert r2.buscar(2001) is None
    assert r2.buscar(2002) is not None
    assert len(r2.listar()) == 1

    # Limpieza
    if os.path.exists(ruta_test):
        os.remove(ruta_test)
    if os.path.exists(r1.ruta):
        os.remove(r1.ruta)


if __name__ == "__main__":
    test_persistencia_entre_instancias()
    test_eliminar_actualiza_archivo()
    print("RepositorioJSON: persistencia verificada ✓")
    print("RepositorioJSON: eliminación y sincronización con disco verificada ✓")

"""
Prueba de Integración End-to-End: Los 3 Patrones Trabajando en Armonía
(Singleton + Factory Method + Abstract Factory)
"""
from singleton import Logger, ConfiguracionSistema
from factory import (
    Estudiante,
    RegistroFabricaRepositorios,
    CreadorRepoMemoria,
    RepositorioEstudiantes
)
from ui_factory import UIFactoryPyQt5, VistaMatriculaGUI


def test_integracion_completa_tres_patrones():
    # 1. Singleton: Configuración y Logger
    config = ConfiguracionSistema()
    logger = Logger()
    logger.limpiar_historial()

    # 2. Factory Method: Registrar y fabricar repositorio
    registro = RegistroFabricaRepositorios()
    repo = registro.fabricar("memoria")
    assert isinstance(repo, RepositorioEstudiantes)

    repo.guardar(Estudiante(codigo="999", nombre="Integracion OK", carrera="Sistemas", promedio=19.5))

    # 3. Abstract Factory: Construir GUI con PyQt5
    factory_ui = UIFactoryPyQt5()
    gui = VistaMatriculaGUI(factory=factory_ui, repositorio=repo)
    cargados = gui.sincronizar_tabla_con_repositorio()

    assert cargados == 1
    render = gui.renderizar_completo()
    assert "PyQt5" in render["toolkit"]
    assert len(logger.historial) >= 1
    assert any("Integracion OK" in entrada or "Cargando 1 registros" in entrada for entrada in logger.historial)

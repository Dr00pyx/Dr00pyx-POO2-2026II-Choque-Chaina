"""
Sistema de Matrícula Integrado - Proyecto Final (Actividad 5).
Integra armoniosamente los 3 patrones GoF y principios SOLID:
1. SINGLETON: Logger y Configuración global.
2. FACTORY METHOD: Creación desacoplada del repositorio (Memoria, Archivo JSON, SQLite).
3. ABSTRACT FACTORY: Familia consistente de widgets de UI (Tkinter o PyQt5).
"""
import sys
from pathlib import Path

from singleton import Logger, NivelLog, ConfiguracionSistema
from factory import (
    Estudiante,
    RegistroFabricaRepositorios,
    RepositorioEstudiantes
)
from ui_factory import (
    UIFactoryTkinter,
    UIFactoryPyQt5,
    VistaMatriculaGUI
)


def ejecutar_sistema():
    print("=" * 70)
    print("   SISTEMA DE GESTIÓN ACADÉMICA Y MATRÍCULA - UNAP (POO II)")
    print("       Integración Arquitectural: Singleton + Factory + Abstract Factory")
    print("=" * 70)

    # 1. SINGLETON: Cargar Configuración y Logger
    config = ConfiguracionSistema()
    logger = Logger()
    logger.info("Bootstrap", f"Iniciando aplicación en entorno [{config.entorno.value}]")
    logger.info("Bootstrap", f"Repositorio configurado: [{config.tipo_repositorio.value}]")
    logger.info("Bootstrap", f"Framework UI configurado: [{config.tipo_ui.value}]")

    # 2. FACTORY METHOD: Crear Repositorio según Configuración
    registro_repos = RegistroFabricaRepositorios()
    # Registramos SQLite con la ruta de la config
    from factory.creadores import CreadorRepoSQLite, CreadorRepoArchivo
    registro_repos.registrar("sqlite", lambda: CreadorRepoSQLite(config.ruta_db))
    registro_repos.registrar("archivo", lambda: CreadorRepoArchivo(config.ruta_json))

    repo: RepositorioEstudiantes = registro_repos.fabricar(config.tipo_repositorio.value)
    logger.info("Bootstrap", f"Repositorio instanciado: {repo.tipo_almacenamiento}")

    # Sembrar datos de prueba
    estudiantes_iniciales = [
        Estudiante(codigo="20230001", nombre="Ana Lucia Chambi", carrera="Ing. de Sistemas", promedio=17.8),
        Estudiante(codigo="20230002", nombre="Joel Quispe Mamani", carrera="Ing. de Sistemas", promedio=15.4),
        Estudiante(codigo="20230003", nombre="Rosa Flores Condori", carrera="Ing. de Sistemas", promedio=18.2),
    ]
    for est in estudiantes_iniciales:
        repo.guardar(est)
        logger.debug("Datos", f"Estudiante insertado/actualizado: {est.nombre}")

    # 3. ABSTRACT FACTORY: Crear Familia de UI según Configuración
    if config.tipo_ui.value == "pyqt5":
        ui_factory = UIFactoryPyQt5()
    else:
        ui_factory = UIFactoryTkinter()

    logger.info("Bootstrap", f"Fábrica de UI seleccionada: {ui_factory.nombre_toolkit}")

    # Construir y sincronizar GUI (Cliente desacoplado mediante DIP)
    gui = VistaMatriculaGUI(factory=ui_factory, repositorio=repo)
    total_cargados = gui.sincronizar_tabla_con_repositorio()
    
    render = gui.renderizar_completo()
    print("\n--- ESPECIFICACIÓN DE INTERFAZ RENDERIZADA ---")
    print(f"Toolkit: {render['toolkit']}")
    print(f"Ventana: {render['ventana']}")
    print(f"Menú:    {render['menu']}")
    print(f"Tabla:   {render['tabla']}")
    print("----------------------------------------------")
    logger.info("Sistema", f"Sistema en ejecución exitosa. Total estudiantes mostrados: {total_cargados}")
    print("\n[OK] Sistema ejecutado y verificado correctamente.")


if __name__ == "__main__":
    ejecutar_sistema()

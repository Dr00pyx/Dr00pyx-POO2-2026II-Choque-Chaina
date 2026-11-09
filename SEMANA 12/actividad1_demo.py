"""
Actividad 1A: Demostración del Patrón Observer en Python 3.12+.
- Configura RepositorioObservable con LoggerObservador y ConsolaObservador.
- Incorpora el observador adicional: EmailObservador ("Enviando correo a {nombre}").
- Registra 2 estudiantes y verifica la notificación a todos los suscriptores.
"""
from estudiante import Estudiante
from repositorios import RepositorioMemoria
from observer import (
    RepositorioObservable,
    LoggerObservador,
    ConsolaObservador,
    EmailObservador,
)
from servicios import ServicioEstudiante
from estrategias import PromedioSimple
import logger


def main():
    print("=" * 70)
    print("ACTIVIDAD 1A — PATRÓN OBSERVER (PYTHON 3.12+)")
    print("=" * 70)

    # 1. Instanciar Repositorio base y envoltorio Observable (Subject)
    repo_base = RepositorioMemoria()
    repo_obs = RepositorioObservable(repo_base)

    # 2. Crear observadores
    obs_logger = LoggerObservador()
    obs_consola = ConsolaObservador()
    obs_email = EmailObservador()  # Requisito adicional

    # 3. Suscribir observadores
    repo_obs.suscribir(obs_consola)
    repo_obs.suscribir(obs_logger)
    repo_obs.suscribir(obs_email)

    # 4. Crear Servicio (Controlador) con Repositorio Observable y PromedioSimple
    svc = ServicioEstudiante(repo_obs, PromedioSimple())

    print(f"\nObservadores suscritos: {len(repo_obs.observadores)}")
    print("Suscriptores activos:")
    for o in repo_obs.observadores:
        print(f" - {type(o).__name__}")

    # 5. Registrar 2 estudiantes según especificación
    print("\nRegistrando Estudiante 1...")
    e1 = Estudiante(2001, "Carlos Fuentes", 0.0, [15.0, 16.0, 17.0])
    svc.registrar(e1)

    print("\nRegistrando Estudiante 2...")
    e2 = Estudiante(2002, "Mariana Rios", 0.0, [18.0, 19.0, 20.0])
    svc.registrar(e2)

    # 6. Comprobaciones de logs y persistencia
    entradas = logger.get_entradas()
    print("\n" + "=" * 70)
    print(f"Verificación: Entradas registradas en Logger: {len(entradas)}")
    for entrada in entradas:
        print(f"  * {entrada}")

    print("\nVerificación de persistencia en Repositorio:")
    for est in repo_obs.listar():
        print(f"  * Guardado: {est}")
    print("=" * 70)


if __name__ == "__main__":
    main()

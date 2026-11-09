# main_mvc.py — wiring MVC completo
from repositorios import RepositorioMemoria
from observer import RepositorioObservable, ConsolaObservador, LoggerObservador
from servicios import ServicioEstudiante
from estrategias import PromedioSimple, PromedioModerado
from estudiante import Estudiante
import logger

# 1. Modelo
repo_base = RepositorioMemoria()
repo_obs = RepositorioObservable(repo_base)

# 2. Vista (observadora)
vista = ConsolaObservador()
log_obs = LoggerObservador()
repo_obs.suscribir(vista)
repo_obs.suscribir(log_obs)

# 3. Controlador
svc = ServicioEstudiante(repo_obs, PromedioSimple())

# 4. Usar el sistema (3 estudiantes iniciales de la guía)
estudiantes = [
    Estudiante(1001, "Ana Quispe", 0.0, [14.0, 18.0, 16.0]),
    Estudiante(1002, "Juan Mamani", 0.0, [12.0, 15.0, 10.0]),
    Estudiante(1003, "Rosa Quispe", 0.0, [18.0, 20.0, 19.0]),
]

print("--- REGISTRO INICIAL (3 ESTUDIANTES - PromedioSimple) ---")
for e in estudiantes:
    svc.registrar(e)
    # Output esperado por estudiante:
    # >> Vista: [1001] Ana Quispe — PPA: 16.0
    # [LOG] HH:MM:SS Guardado: [1001] Ana Quispe

print("Entradas de log tras registro inicial:", len(logger.get_entradas()))

# =============================================================================
# ACTIVIDAD 3A: PASOS ADICIONALES REQUERIDOS
# =============================================================================

# Paso 1: Agregar un 4° estudiante con notas [5.0, 5.0, 5.0] y verificar PPA = 5.0
print("\n--- ACTIVIDAD 3A: REGISTRO DEL 4° ESTUDIANTE ---")
e4 = Estudiante(1004, "Pedro Ramos", 0.0, [5.0, 5.0, 5.0])
svc.registrar(e4)
print(f">> Verificación PPA del 4° estudiante: {e4.ppa:.1f} (Esperado: 5.0)")
assert abs(e4.ppa - 5.0) < 1e-6, "El PPA del 4° estudiante debe ser 5.0"

print("Entradas de log con 4° estudiante:", len(logger.get_entradas()))

# Paso 2: Cambiar PromedioSimple a PromedioModerado en svc y registrar de nuevo
print("\n--- ACTIVIDAD 3A: CAMBIO DE ESTRATEGIA A PromedioModerado EN svc ---")
svc.set_estrategia(PromedioModerado())
print("Estrategia del controlador actualizada a:", type(svc.estrategia).__name__)

# Registramos estudiantes bajo la nueva estrategia (ejemplo con notas extremas para verificar)
estudiantes_moderados = [
    Estudiante(1005, "Diana Vargas", 0.0, [5.0, 14.0, 16.0, 20.0]),
    Estudiante(1006, "Mario Mamani", 0.0, [10.0, 15.0, 18.0, 20.0, 12.0]),
]

for e in estudiantes_moderados:
    svc.registrar(e)

print("\nEntradas totales de log registradas:", len(logger.get_entradas()))

# =============================================================================
# RESPUESTA A LA PREGUNTA REFLEXIVA DE ACTIVIDAD 3A:
# ¿El código de ConsolaObservador o de RepositorioObservable cambió?
# =============================================================================
print("\n" + "=" * 70)
print("RESPUESTA A PREGUNTA DE ACTIVIDAD 3A:")
print("¿El código de ConsolaObservador o de RepositorioObservable cambió?")
print("RESPUESTA:")
print("NO. Ninguno de los dos componentes sufrió la más mínima modificación.")
print("Justificación:")
print("1. Gracias al patrón OBSERVER, el Sujeto (RepositorioObservable) y la Vista")
print("   (ConsolaObservador) están completamente desacoplados del Controlador")
print("   (ServicioEstudiante) y del algoritmo de cálculo (Strategy).")
print("2. El Sujeto únicamente se encarga de guardar y notificar el evento 'on_guardado'")
print("   a través de la abstracción IObservador, sin saber qué estrategia calculó el PPA.")
print("3. La Vista (ConsolaObservador) solo reacciona al evento renderizando los datos")
print("   del Estudiante, sin depender de cómo ni cuándo se calculó dicho promedio.")
print("Esto demuestra la máxima vigencia de los principios OCP (Open/Closed Principle)")
print("y SRP (Single Responsibility Principle) en una arquitectura MVC.")
print("=" * 70)

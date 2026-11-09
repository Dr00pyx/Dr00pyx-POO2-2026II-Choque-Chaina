#include "Estudiante.h"
#include "Logger.h"
#include "RepositorioMemoria.h"
#include "ServicioEstudiante.h"
#include "estrategias.h"
#include "observer.h"
#include <cassert>
#include <cmath>
#include <iostream>
#include <memory>
#include <vector>

int main() {
    std::cout << "======================================================================\n";
    std::cout << "ACTIVIDAD 3A — MVC COMPLETO CON OBSERVER Y STRATEGY (C++17)\n";
    std::cout << "======================================================================\n";

    // 1. Modelo
    RepositorioMemoria repoBase;
    RepositorioObservable repoObs(repoBase);

    // 2. Vista (observadora)
    ConsolaObserver vista;
    LoggerObserver logObs;
    repoObs.suscribir(&vista);
    repoObs.suscribir(&logObs);

    // 3. Controlador
    ServicioEstudiante svc(repoObs, std::make_unique<PromedioSimple>());

    // 4. Usar el sistema (3 estudiantes iniciales de la guía)
    std::vector<Estudiante> estudiantes = {
        Estudiante(1001, "Ana Quispe", 0.0f, {14.0f, 18.0f, 16.0f}),
        Estudiante(1002, "Juan Mamani", 0.0f, {12.0f, 15.0f, 10.0f}),
        Estudiante(1003, "Rosa Quispe", 0.0f, {18.0f, 20.0f, 19.0f}),
    };

    std::cout << "\n--- REGISTRO INICIAL (3 ESTUDIANTES - PromedioSimple) ---\n";
    for (auto& e : estudiantes) {
        svc.registrar(e);
        // Output esperado por estudiante:
        // >> Vista: [1001] Ana Quispe — PPA: 16.0
        // [LOG] HH:MM:SS Guardado: [1001] Ana Quispe
    }

    std::cout << "Entradas de log tras registro inicial: "
              << Logger::getInstance().get_entradas().size() << "\n";
    assert(Logger::getInstance().get_entradas().size() == 3);

    // =========================================================================
    // ACTIVIDAD 3A: PASOS ADICIONALES REQUERIDOS
    // =========================================================================

    // Paso 1: Agregar un 4° estudiante con notas [5.0, 5.0, 5.0] y verificar PPA = 5.0
    std::cout << "\n--- ACTIVIDAD 3A: REGISTRO DEL 4° ESTUDIANTE ---\n";
    Estudiante e4(1004, "Pedro Ramos", 0.0f, {5.0f, 5.0f, 5.0f});
    svc.registrar(e4);
    std::cout << ">> Verificación PPA del 4° estudiante: " << e4.ppa() << " (Esperado: 5.0)\n";
    assert(std::fabs(e4.ppa() - 5.0f) < 1e-4f);
    assert(Logger::getInstance().get_entradas().size() == 4);

    // Paso 2: Cambiar PromedioSimple a PromedioModerado en svc y registrar de nuevo
    std::cout << "\n--- ACTIVIDAD 3A: CAMBIO DE ESTRATEGIA A PromedioModerado EN svc ---\n";
    svc.set_estrategia(std::make_unique<PromedioModerado>());
    std::cout << "Estrategia del controlador actualizada a: " << svc.estrategia()->nombre() << "\n";

    std::vector<Estudiante> estudiantesModerados = {
        Estudiante(1005, "Diana Vargas", 0.0f, {5.0f, 14.0f, 16.0f, 20.0f}),
        Estudiante(1006, "Mario Mamani", 0.0f, {10.0f, 15.0f, 18.0f, 20.0f, 12.0f}),
    };

    for (auto& e : estudiantesModerados) {
        svc.registrar(e);
    }

    std::cout << "\nEntradas totales de log registradas: "
              << Logger::getInstance().get_entradas().size() << "\n";
    assert(Logger::getInstance().get_entradas().size() == 6);

    // =========================================================================
    // RESPUESTA A LA PREGUNTA REFLEXIVA DE ACTIVIDAD 3A:
    // ¿El código de ConsolaObservador o de RepositorioObservable cambió?
    // =========================================================================
    std::cout << "\n======================================================================\n";
    std::cout << "RESPUESTA A PREGUNTA DE ACTIVIDAD 3A:\n";
    std::cout << "¿El código de ConsolaObservador o de RepositorioObservable cambió?\n";
    std::cout << "RESPUESTA:\n";
    std::cout << "NO. Ninguno de los dos componentes sufrió la más mínima modificación.\n";
    std::cout << "Justificación:\n";
    std::cout << "1. Gracias al patrón OBSERVER, el Sujeto (RepositorioObservable) y la Vista\n";
    std::cout << "   (ConsolaObserver) están completamente desacoplados del Controlador\n";
    std::cout << "   (ServicioEstudiante) y del algoritmo de cálculo (Strategy).\n";
    std::cout << "2. El Sujeto únicamente se encarga de guardar y notificar el evento 'on_guardado'\n";
    std::cout << "   a través de la abstracción IObserverEstudiante, sin saber qué estrategia calculó el PPA.\n";
    std::cout << "3. La Vista (ConsolaObserver) solo reacciona al evento renderizando los datos\n";
    std::cout << "   del Estudiante, sin depender de cómo ni cuándo se calculó dicho promedio.\n";
    std::cout << "Esto demuestra la máxima vigencia de los principios OCP (Open/Closed Principle)\n";
    std::cout << "y SRP (Single Responsibility Principle) en una arquitectura MVC.\n";
    std::cout << "======================================================================\n";

    return 0;
}

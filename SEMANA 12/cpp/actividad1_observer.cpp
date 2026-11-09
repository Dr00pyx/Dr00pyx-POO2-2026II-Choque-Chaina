#include "Estudiante.h"
#include "Logger.h"
#include "RepositorioMemoria.h"
#include "ServicioEstudiante.h"
#include "estrategias.h"
#include "observer.h"
#include <cassert>
#include <iostream>
#include <memory>

int main() {
    std::cout << "======================================================================\n";
    std::cout << "ACTIVIDAD 1A — PATRÓN OBSERVER EN C++17\n";
    std::cout << "======================================================================\n";

    // 1. Instanciar Repositorio Base y Sujeto Observable
    RepositorioMemoria repoBase;
    RepositorioObservable repoObs(repoBase);

    // 2. Instanciar Observadores (Consola, Logger, y el Adicional: Email)
    ConsolaObserver obsConsola;
    LoggerObserver obsLogger;
    EmailObserver obsEmail;

    // 3. Suscripción
    repoObs.suscribir(&obsConsola);
    repoObs.suscribir(&obsLogger);
    repoObs.suscribir(&obsEmail);

    assert(repoObs.observadores().size() == 3);

    // 4. Servicio / Controlador
    ServicioEstudiante svc(repoObs, std::make_unique<PromedioSimple>());

    std::cout << "\nObservadores suscritos: " << repoObs.observadores().size() << "\n";

    // 5. Registrar 2 estudiantes
    std::cout << "\n--- Registrando Estudiante 1 ---\n";
    Estudiante e1(2001, "Carlos Fuentes", 0.0f, {15.0f, 16.0f, 17.0f});
    svc.registrar(e1);

    std::cout << "\n--- Registrando Estudiante 2 ---\n";
    Estudiante e2(2002, "Mariana Rios", 0.0f, {18.0f, 19.0f, 20.0f});
    svc.registrar(e2);

    // 6. Verificaciones
    auto entradas = Logger::getInstance().get_entradas();
    std::cout << "\n======================================================================\n";
    std::cout << "Verificación: Entradas registradas en Logger: " << entradas.size() << "\n";
    for (const auto& entrada : entradas) {
        std::cout << "  * " << entrada << "\n";
    }
    assert(entradas.size() == 2);

    auto listado = repoObs.listar();
    assert(listado.size() == 2);
    std::cout << "\nVerificación de Persistencia:\n";
    for (const auto& est : listado) {
        std::cout << "  * Guardado: " << est.to_string() << "\n";
    }

    return 0;
}

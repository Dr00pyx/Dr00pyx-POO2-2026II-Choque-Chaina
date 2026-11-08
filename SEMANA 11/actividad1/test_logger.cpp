#include "logger.hpp"
#include <cassert>
#include <thread>
#include <vector>

void testSingletonIdentity() {
    Logger& l1 = Logger::instancia("test_app.log");
    Logger& l2 = Logger::instancia("test_app.log");
    
    // Verificación 1: Misma dirección de memoria
    assert(&l1 == &l2);
    std::cout << "[PASS] Verificacion de direccion unica: &l1 == &l2 (" << &l1 << ")\n";
}

void testConcurrentLogging() {
    Logger& logger = Logger::instancia("test_app.log");
    logger.info("Test", "Iniciando prueba de concurrencia con 8 hilos...");

    std::vector<std::thread> hilos;
    for (int i = 0; i < 8; ++i) {
        hilos.emplace_back([i]() {
            Logger& l = Logger::instancia();
            for (int j = 0; j < 5; ++j) {
                l.debug("Hilo-" + std::to_string(i), "Mensaje " + std::to_string(j));
            }
        });
    }

    for (auto& h : hilos) {
        if (h.joinable()) {
            h.join();
        }
    }

    logger.info("Test", "Prueba de concurrencia finalizada con exito.");
    std::cout << "[PASS] Acceso concurrente thread-safe completado.\n";
}

int main() {
    std::cout << "=========================================\n";
    std::cout << "  PRUEBAS UNITARIAS: SINGLETON LOGGER C++\n";
    std::cout << "=========================================\n";
    
    testSingletonIdentity();
    testConcurrentLogging();
    
    Logger::instancia().warn("Main", "Prueba de advertencia");
    Logger::instancia().error("Main", "Prueba de error critico");

    std::cout << "\nTODAS LAS PRUEBAS EN C++ PASARON CORRECTAMENTE (assert validado).\n";
    return 0;
}

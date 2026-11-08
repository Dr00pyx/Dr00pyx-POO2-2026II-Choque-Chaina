#include "conexion_mejorada.hpp"
#include <cassert>
#include <thread>
#include <vector>

// Mock de Logger para verificar que DIP permite testeo unitario
class MockLogger : public ILogger {
public:
    std::vector<std::string> mensajes;
    std::mutex mtx;

    void info(const std::string& modulo, const std::string& mensaje) override {
        std::lock_guard<std::mutex> lock(mtx);
        mensajes.push_back("[" + modulo + "] " + mensaje);
    }
};

void testInyeccionYMock() {
    auto mockLog = std::make_shared<MockLogger>();
    auto db = std::make_shared<ConexionSQLite>("sqlite:///test_estudiantes.db", mockLog);

    db->ejecutar("SELECT * FROM estudiantes WHERE promedio >= 11;");
    
    assert(mockLog->mensajes.size() == 1);
    assert(mockLog->mensajes[0].find("SELECT * FROM estudiantes") != std::string::npos);
    std::cout << "[PASS] Inyeccion de dependencias y MockLogger validados con exito.\n";
}

void testSingletonThreadSafe() {
    auto& s1 = GestorConexionSingleton::instancia();
    auto& s2 = GestorConexionSingleton::instancia();

    assert(&s1 == &s2);
    std::cout << "[PASS] GestorConexionSingleton retorna exactamente la misma direccion de memoria.\n";

    std::vector<std::thread> hilos;
    for (int i = 0; i < 5; ++i) {
        hilos.emplace_back([i]() {
            auto db = GestorConexionSingleton::instancia().conexion();
            db->ejecutar("INSERT INTO log_conexiones VALUES (" + std::to_string(i) + ");");
        });
    }

    for (auto& h : hilos) {
        if (h.joinable()) h.join();
    }
    std::cout << "[PASS] Ejecucion concurrente de consultas SQL completada con exito.\n";
}

int main() {
    std::cout << "=============================================\n";
    std::cout << "  PRUEBAS ACTIVIDAD 4: CONEXION MEJORADA C++ \n";
    std::cout << "=============================================\n";
    testInyeccionYMock();
    testSingletonThreadSafe();
    std::cout << "TODAS LAS VERIFICACIONES DE LA ACTIVIDAD 4 PASARON.\n";
    return 0;
}

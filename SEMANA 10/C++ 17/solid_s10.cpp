/**
 * SIS206 — Programación Orientada a Objetos II
 * Guía de Práctica Avanzada — Semana 10
 * Tema: Principios SOLID en el Sistema Académico UNAP
 * 
 * Implementación completa en C++17 que demuestra:
 * - SRP: Separación de la clase God en 4 componentes especializados.
 * - DIP: Inversión de dependencias en ServicioEstudiante vía interfaces virtuales puras.
 * - OCP: Incorporación de PromedioModerado y RepositorioArchivo sin modificar ServicioEstudiante.
 */

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <optional>
#include <algorithm>
#include <numeric>
#include <fstream>
#include <sstream>
#include <unordered_map>

#include "Estudiante.h"
#include "IEstrategiaCalculo.h"
#include "PromedioSimple.h"
#include "PromedioModerado.h"
#include "IRepositorioEstudiante.h"
#include "RepositorioMemoria.h"
#include "RepositorioArchivo.h"
#include "ServicioEstudiante.h"

// Función auxiliar para imprimir detalles de un estudiante
void imprimirEstudiante(const std::string& titulo, const std::optional<Estudiante>& optEst) {
    std::cout << std::left << std::setw(28) << titulo << ": ";
    if (optEst.has_value()) {
        std::cout << "[Código: " << optEst->codigo()
                  << " | Nombre: " << std::setw(20) << optEst->nombre()
                  << " | PPA: " << std::fixed << std::setprecision(2) << optEst->ppa() << "]\n";
    } else {
        std::cout << "Estudiante no encontrado.\n";
    }
}

int main() {
    std::cout << "====================================================================\n";
    std::cout << "  UNIVERSIDAD NACIONAL DEL ALTIPLANO - SIS206 POO II\n";
    std::cout << "  SEMANA 10: PRINCIPIOS SOLID EN EL SISTEMA ACADÉMICO UNAP\n";
    std::cout << "====================================================================\n\n";

    // =========================================================================
    // PARTE 1: ACTIVIDAD 1A — SRP + DIP con RepositorioMemoria y PromedioSimple
    // =========================================================================
    std::cout << "--------------------------------------------------------------------\n";
    std::cout << "[ACTIVIDAD 1A] SRP + DIP (PromedioSimple + RepositorioMemoria)\n";
    std::cout << "--------------------------------------------------------------------\n";

    RepositorioMemoria repoMemoria;
    PromedioSimple calcSimple;
    ServicioEstudiante servicioMemoria(repoMemoria, calcSimple);

    // Registro de estudiantes con notas distintas
    std::cout << "-> Registrando estudiantes en memoria...\n";
    
    Estudiante e1{202101, "Carlos Condori", 0.0f};
    std::vector<float> notas1 = {15.0f, 17.5f, 13.0f, 16.5f};
    servicioMemoria.registrar(e1, notas1);

    Estudiante e2{202102, "Mariana Ramos", 0.0f};
    std::vector<float> notas2 = {18.0f, 19.0f, 20.0f, 17.0f};
    servicioMemoria.registrar(e2, notas2);

    Estudiante e3{202103, "Juan Mamani", 0.0f};
    std::vector<float> notas3 = {11.0f, 12.5f, 14.0f, 10.5f};
    servicioMemoria.registrar(e3, notas3);

    // Búsqueda y verificación
    std::cout << "-> Verificando calculo de PPA mediante buscar():\n";
    imprimirEstudiante("Estudiante 202101", servicioMemoria.buscar(202101));
    imprimirEstudiante("Estudiante 202102", servicioMemoria.buscar(202102));
    imprimirEstudiante("Estudiante 202103", servicioMemoria.buscar(202103));

    // =========================================================================
    // PARTE 2: ACTIVIDAD 1A (ADICIONAL) — RepositorioArchivo (CSV con std::ofstream)
    // =========================================================================
    std::cout << "\n--------------------------------------------------------------------\n";
    std::cout << "[ACTIVIDAD 1A - ADICIONAL] Persistencia en CSV (RepositorioArchivo)\n";
    std::cout << "--------------------------------------------------------------------\n";

    const std::string rutaCsv = "estudiantes_cpp.csv";
    RepositorioArchivo repoArchivo(rutaCsv);
    // ServicioEstudiante NO cambia, se le inyecta RepositorioArchivo gracias a DIP
    ServicioEstudiante servicioArchivo(repoArchivo, calcSimple);

    Estudiante eCsv1{202201, "Beatriz Flores", 0.0f};
    servicioArchivo.registrar(eCsv1, {16.0f, 18.0f, 17.0f});

    Estudiante eCsv2{202202, "David Quispe", 0.0f};
    servicioArchivo.registrar(eCsv2, {14.0f, 15.0f, 16.0f});

    std::cout << "-> Guardados en archivo CSV: " << rutaCsv << "\n";
    imprimirEstudiante("Estudiante 202201 (CSV)", servicioArchivo.buscar(202201));
    imprimirEstudiante("Estudiante 202202 (CSV)", servicioArchivo.buscar(202202));

    // Verificar lectura directa del archivo CSV generado
    std::cout << "-> Contenido del archivo CSV en disco:\n";
    {
        std::ifstream f(rutaCsv);
        std::string linea;
        while (std::getline(f, linea)) {
            std::cout << "   " << linea << "\n";
        }
    }

    // =========================================================================
    // PARTE 3: ACTIVIDAD 2A — OCP (Agregar PromedioModerado sin tocar ServicioEstudiante)
    // =========================================================================
    std::cout << "\n--------------------------------------------------------------------\n";
    std::cout << "[ACTIVIDAD 2A] OCP - Comparación PromedioSimple vs PromedioModerado\n";
    std::cout << "--------------------------------------------------------------------\n";

    // Caso de prueba oficial de la guía:
    // Notas: {14.0, 20.0, 16.0, 18.0, 12.0}
    // PromedioSimple:   (14 + 20 + 16 + 18 + 12) / 5 = 80 / 5 = 16.00
    // PromedioModerado: descarta 12.0 y 20.0 -> (14 + 16 + 18) / 3 = 48 / 3 = 16.00
    std::vector<float> notasOficial = {14.0f, 20.0f, 16.0f, 18.0f, 12.0f};

    // Caso 2 con efecto visible de diferencia de extremos:
    // Notas: {05.0, 15.0, 16.0, 17.0, 20.0}
    // PromedioSimple:   (5 + 15 + 16 + 17 + 20) / 5 = 73 / 5 = 14.60
    // PromedioModerado: descarta 5 y 20 -> (15 + 16 + 17) / 3 = 48 / 3 = 16.00
    std::vector<float> notasExtremas = {5.0f, 15.0f, 16.0f, 17.0f, 20.0f};

    RepositorioMemoria repoOCP;

    // 1. Instanciación con PromedioSimple
    PromedioSimple calcSimpleOCP;
    ServicioEstudiante svcSimple(repoOCP, calcSimpleOCP);

    Estudiante anaSimple{1001, "Ana Quispe", 0.0f};
    svcSimple.registrar(anaSimple, notasOficial);

    Estudiante luisSimple{1002, "Luis Chambi", 0.0f};
    svcSimple.registrar(luisSimple, notasExtremas);

    // 2. Instanciación con PromedioModerado
    // ¡OCP en acción!: Solo cambia la estrategia inyectada, ServicioEstudiante permanece intacto.
    PromedioModerado calcModeradoOCP;
    ServicioEstudiante svcModerado(repoOCP, calcModeradoOCP);

    Estudiante anaModerado{1001, "Ana Quispe", 0.0f};
    svcModerado.registrar(anaModerado, notasOficial);

    std::cout << "-> Caso de la guia (Ana Quispe con notas 14, 20, 16, 18, 12):\n";
    auto resAna = svcModerado.buscar(1001);
    imprimirEstudiante("Ana Quispe (Moderado)", resAna);
    std::cout << "   Esperado: 16.00 | Obtenido: " << resAna->ppa() 
              << " -> " << (resAna->ppa() == 16.0f ? "CORRECTO [OK]" : "ERROR") << "\n\n";

    std::cout << "-> Caso con distorsión de notas extremas (Luis Chambi con notas 05, 15, 16, 17, 20):\n";
    svcSimple.registrar(luisSimple, notasExtremas);
    auto resLuisSimple = svcSimple.buscar(1002);
    std::cout << "   Con PromedioSimple  : PPA = " << resLuisSimple->ppa() 
              << " (afectado negativamente por el 05)\n";

    Estudiante luisModerado{1002, "Luis Chambi", 0.0f};
    svcModerado.registrar(luisModerado, notasExtremas);
    auto resLuisModerado = svcModerado.buscar(1002);
    std::cout << "   Con PromedioModerado: PPA = " << resLuisModerado->ppa() 
              << " (descarta 05 y 20 -> promedio de 15, 16, 17 = 16.00)\n";

    std::cout << "\n====================================================================\n";
    std::cout << "  TODAS LAS PRUEBAS EN C++17 COMPLETADAS EXITOSAMENTE\n";
    std::cout << "====================================================================\n";

    return 0;
}

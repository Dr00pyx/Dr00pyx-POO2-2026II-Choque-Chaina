#include "estrategias.h"
#include "strategy.h"
#include "Logger.h"
#include <cassert>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <memory>
#include <vector>

int main() {
    std::cout << "======================================================================\n";
    std::cout << "ACTIVIDAD 2A — PATRÓN STRATEGY CON CONTEXTO EXPLÍCITO EN C++17\n";
    std::cout << "======================================================================\n";

    // 1. Caso base de la guía: [10.0, 15.0, 18.0, 20.0, 12.0]
    std::vector<float> notasGuia = {10.0f, 15.0f, 18.0f, 20.0f, 12.0f};

    ContextoCalculoPPA ctx(std::make_unique<PromedioSimple>());
    float ppaSimple = ctx.calcular(notasGuia); // = 15.0
    std::cout << "\n[1] Caso base de la guía:\n";
    std::cout << "PPA con PromedioSimple: " << std::fixed << std::setprecision(1) << ppaSimple << "\n";

    // Intercambio dinámico a PromedioModerado con std::unique_ptr
    ctx.setEstrategia(std::make_unique<PromedioModerado>());
    float ppaMod = ctx.calcular(notasGuia); // descarta 10.0 y 20.0 -> 15.0
    std::cout << "PPA con PromedioModerado: " << std::fixed << std::setprecision(1) << ppaMod << "\n";
    std::cout << "Simple=" << ppaSimple << " Moderado=" << ppaMod << "\n";
    assert(std::fabs(ppaSimple - 15.0f) < 1e-4f);
    assert(std::fabs(ppaMod - 15.0f) < 1e-4f);

    // 2. Caso con notas extremas asimétricas para evidenciar la divergencia
    std::vector<float> notasAsimetricas = {5.0f, 14.0f, 15.0f, 16.0f, 20.0f};
    std::cout << "\n[2] Verificación con notas extremas asimétricas:\n";
    std::cout << "Notas: [5.0, 14.0, 15.0, 16.0, 20.0]\n";

    ctx.setEstrategia(std::make_unique<PromedioSimple>());
    float ppaSimAsym = ctx.calcular(notasAsimetricas); // (5+14+15+16+20)/5 = 70/5 = 14.0

    ctx.setEstrategia(std::make_unique<PromedioModerado>());
    float ppaModAsym = ctx.calcular(notasAsimetricas); // descarta 5 y 20 -> (14+15+16)/3 = 45/3 = 15.0

    std::cout << "Promedio Simple   : " << ppaSimAsym << " (suma=70 / 5 = 14.0)\n";
    std::cout << "Promedio Moderado : " << ppaModAsym << " (descarta 5.0 y 20.0 -> suma=45 / 3 = 15.0)\n";
    std::cout << "Diferencia comprobada: " << std::fabs(ppaSimAsym - ppaModAsym) << " puntos\n";
    assert(std::fabs(ppaSimAsym - 14.0f) < 1e-4f);
    assert(std::fabs(ppaModAsym - 15.0f) < 1e-4f);

    // 3. Requerimiento ADICIONAL: Promedio Geométrico
    std::cout << "\n[3] ADICIONAL: Promedio Geométrico (raíz n-ésima del producto):\n";
    ctx.setEstrategia(std::make_unique<PromedioGeometrico>());
    float ppaGeo = ctx.calcular(notasAsimetricas);
    std::cout << "Promedio Geométrico: " << std::setprecision(2) << ppaGeo << "\n";

    // Verificación de entradas de Logger por cambio de estrategia
    auto logs = Logger::getInstance().get_entradas();
    std::cout << "\nAuditoría en Logger por cambios de estrategia (" << logs.size() << " eventos):\n";
    for (const auto& l : logs) {
        std::cout << "  * " << l << "\n";
    }
    assert(logs.size() >= 3);

    return 0;
}

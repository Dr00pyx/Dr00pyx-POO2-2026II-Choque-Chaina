// main.cpp — Uso de la clase Estudiante en C++17
#include "estudiante.h"
#include <iostream>
#include <iomanip>

int main() {
    std::cout << "=== SIS206 - POO II | Practica S09: C++17 ===" << std::endl;
    
    std::cout << "\n--- Salida Original de la Guia (3 lineas esperadas) ---" << std::endl;
    Estudiante e{1001, "Ana Quispe", 15.5f, 3};
    e.agregar_nota(14.0f);
    e.agregar_nota(16.0f);
    e.agregar_nota(18.0f);

    std::cout << e.to_string() << std::endl;

    if (auto prom = e.calcular_promedio(); prom.has_value()) {
        std::cout << "Promedio semestral: " << prom.value() << std::endl;
    }

    // Prueba de validacion original
    try {
        Estudiante invalido{-1, "X", 5.0f, 1};
    } catch (const std::invalid_argument& ex) {
        std::cout << "Error esperado: " << ex.what() << std::endl;
    }

    // --- 2. Requerimiento Actividad 2A: Agregar nota de 20.0 y verificar cambio de promedio ---
    std::cout << "\n--- Actividad 2A: Agregar nota de 20.0 y verificar promedio ---" << std::endl;
    auto prom_anterior = e.calcular_promedio().value_or(0.0f);
    std::cout << "Promedio anterior (14, 16, 18): " << prom_anterior << std::endl;
    
    e.agregar_nota(20.0f);
    auto prom_nuevo = e.calcular_promedio().value_or(0.0f);
    std::cout << "Se agrego nota: 20.0" << std::endl;
    std::cout << "Nuevo promedio semestral (14, 16, 18, 20): " << prom_nuevo << std::endl;
    if (prom_nuevo != prom_anterior) {
        std::cout << "=> VERIFICADO: El promedio cambio exitosamente de " 
                  << prom_anterior << " a " << prom_nuevo << std::endl;
    }

    // --- 3. Requerimiento ADICIONAL Actividad 2A: Metodo es_aprobado() -> bool (PPA >= 11) ---
    std::cout << "\n--- Requerimiento ADICIONAL: Metodo es_aprobado() (PPA >= 11) ---" << std::endl;
    std::cout << "Estudiante: " << e.nombre() << " | PPA: " << e.ppa() 
              << " | es_aprobado(): " << (e.es_aprobado() ? "true (APROBADO)" : "false (DESAPROBADO)") 
              << std::endl;

    Estudiante e_desaprobado{1002, "Carlos Ramos", 9.5f, 2};
    std::cout << "Estudiante: " << e_desaprobado.nombre() << " | PPA: " << e_desaprobado.ppa() 
              << " | es_aprobado(): " << (e_desaprobado.es_aprobado() ? "true (APROBADO)" : "false (DESAPROBADO)") 
              << std::endl;

    // Pruebas adicionales de validacion en C++17
    std::cout << "\n--- Pruebas de validacion de limites en C++17 ---" << std::endl;
    try {
        Estudiante sin_nombre{1003, "", 14.0f, 1};
    } catch (const std::invalid_argument& ex) {
        std::cout << "Validacion nombre vacio: " << ex.what() << std::endl;
    }

    try {
        Estudiante ppa_invalido{1004, "Marcos Tito", 21.0f, 1};
    } catch (const std::out_of_range& ex) {
        std::cout << "Validacion PPA > 20: " << ex.what() << std::endl;
    }

    try {
        e.agregar_nota(25.0f);
    } catch (const std::out_of_range& ex) {
        std::cout << "Validacion Nota fuera de rango (25.0): " << ex.what() << std::endl;
    }

    return 0;
}

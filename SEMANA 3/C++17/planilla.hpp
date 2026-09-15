#pragma once
#include "PersonalUniversitario.hpp"
#include <vector>
#include <memory>
#include <iostream>
#include <iomanip>

inline void planilla(const std::vector<std::unique_ptr<PersonalUniversitario>>& p) {
    float total = 0.0f;
    std::cout << std::string(60, '=') << "\n";
    std::cout << "PLANILLA PERSONAL UNIVERSITARIO — UNAP PUNO\n";
    std::cout << std::string(60, '=') << "\n";
    for (const auto& persona : p) {
        std::cout << std::fixed << std::setprecision(2)
                  << persona->identificarse()
                  << " S/ " << persona->calcularRemuneracion() << "\n";
        total += persona->calcularRemuneracion();
    }
    std::cout << std::string(60, '-') << "\n";
    std::cout << "TOTAL: S/ " << total << "\n";
}

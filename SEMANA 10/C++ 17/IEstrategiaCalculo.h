#pragma once

#include <vector>

/**
 * @struct IEstrategiaCalculo
 * @brief Interfaz de estrategia de cálculo de notas (SRP / OCP / DIP).
 * 
 * Define el contrato abstracto para cualquier algoritmo de cálculo de PPA.
 */
struct IEstrategiaCalculo {
    virtual float calcular(const std::vector<float>& notas) const = 0;
    virtual ~IEstrategiaCalculo() = default;
};

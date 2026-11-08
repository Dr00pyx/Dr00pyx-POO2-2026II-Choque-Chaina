#pragma once

#include "IEstrategiaCalculo.h"
#include <numeric>

/**
 * @struct PromedioSimple
 * @brief Implementación de cálculo mediante promedio aritmético tradicional.
 */
struct PromedioSimple : public IEstrategiaCalculo {
    float calcular(const std::vector<float>& notas) const override {
        if (notas.empty()) return 0.0f;
        float suma = 0.0f;
        for (float nota : notas) {
            suma += nota;
        }
        return suma / static_cast<float>(notas.size());
    }
};

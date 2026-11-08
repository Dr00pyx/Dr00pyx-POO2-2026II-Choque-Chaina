#pragma once

#include "IEstrategiaCalculo.h"
#include <vector>
#include <algorithm>
#include <numeric>

/**
 * @struct PromedioModerado
 * @brief Implementación de cálculo que descarta la nota más alta y la más baja (OCP).
 * 
 * Cumple con el Principio Abierto/Cerrado (OCP): Se extiende el sistema
 * incorporando una nueva regla de negocio sin alterar el código fuente
 * de ServicioEstudiante ni de las clases preexistentes.
 */
struct PromedioModerado : public IEstrategiaCalculo {
    float calcular(const std::vector<float>& notas) const override {
        // Si hay 2 o menos notas, no se pueden descartar extremos
        if (notas.size() <= 2) return 0.0f;

        auto sorted = notas;
        std::sort(sorted.begin(), sorted.end());

        // Sumar excluyendo el primer elemento (mínimo) y el último (máximo)
        float suma = std::accumulate(sorted.begin() + 1, sorted.end() - 1, 0.0f);
        return suma / static_cast<float>(sorted.size() - 2);
    }
};

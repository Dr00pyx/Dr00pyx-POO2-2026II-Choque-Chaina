#pragma once

#include <algorithm>
#include <cmath>
#include <numeric>
#include <string>
#include <vector>

/**
 * @struct IEstrategiaCalculo
 * @brief Interfaz para estrategias de cálculo de PPA (Patrón Strategy).
 */
struct IEstrategiaCalculo {
    virtual float calcular(const std::vector<float>& notas) const = 0;
    virtual std::string nombre() const = 0;
    virtual ~IEstrategiaCalculo() = default;
};

/**
 * @struct PromedioSimple
 * @brief Media aritmética clásica de todas las notas.
 */
struct PromedioSimple : public IEstrategiaCalculo {
    float calcular(const std::vector<float>& notas) const override {
        if (notas.empty()) return 0.0f;
        float suma = std::accumulate(notas.begin(), notas.end(), 0.0f);
        return suma / static_cast<float>(notas.size());
    }

    std::string nombre() const override {
        return "PromedioSimple";
    }
};

/**
 * @struct PromedioModerado
 * @brief Descarta la nota más baja y la más alta antes de promediar.
 */
struct PromedioModerado : public IEstrategiaCalculo {
    float calcular(const std::vector<float>& notas) const override {
        if (notas.empty()) return 0.0f;
        if (notas.size() <= 2) {
            float suma = std::accumulate(notas.begin(), notas.end(), 0.0f);
            return suma / static_cast<float>(notas.size());
        }

        std::vector<float> ordenadas = notas;
        std::sort(ordenadas.begin(), ordenadas.end());

        // Descartar ordenadas.front() y ordenadas.back()
        float suma = 0.0f;
        for (size_t i = 1; i < ordenadas.size() - 1; ++i) {
            suma += ordenadas[i];
        }
        return suma / static_cast<float>(ordenadas.size() - 2);
    }

    std::string nombre() const override {
        return "PromedioModerado";
    }
};

/**
 * @struct PromedioGeometrico
 * @brief ADICIONAL Actividad 2A: Raíz n-ésima del producto de calificaciones.
 */
struct PromedioGeometrico : public IEstrategiaCalculo {
    float calcular(const std::vector<float>& notas) const override {
        if (notas.empty()) return 0.0f;
        double producto = 1.0;
        for (float n : notas) {
            producto *= static_cast<double>(n);
        }
        if (producto < 0.0) return 0.0f;
        return static_cast<float>(std::pow(producto, 1.0 / static_cast<double>(notas.size())));
    }

    std::string nombre() const override {
        return "PromedioGeometrico";
    }
};

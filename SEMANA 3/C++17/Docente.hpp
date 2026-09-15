#pragma once
#include "PersonalUniversitario.hpp"
#include <stdexcept>

class Docente : public PersonalUniversitario {
    int horas_;
    float tarifa_ = 75.0f;
    float factor_;

    static float resolverFactor(const std::string& cat) {
        if (cat == "Auxiliar") return 1.0f;
        if (cat == "Asociado") return 1.4f;
        if (cat == "Principal") return 1.8f;
        throw std::invalid_argument("Categoría inválida: " + cat);
    }
public:
    Docente(std::string dni, std::string nombres, std::string apellidos,
            int horas, const std::string& categoria)
        : PersonalUniversitario(std::move(dni), std::move(nombres), std::move(apellidos)),
          horas_(horas), factor_(resolverFactor(categoria)) {
        if (horas <= 0 || horas > 40)
            throw std::invalid_argument("Horas fuera de rango [1,40]");
    }

    float calcularRemuneracion() const override {
        return horas_ * tarifa_ * factor_;
    }
};

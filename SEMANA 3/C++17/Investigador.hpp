#pragma once
#include "PersonalUniversitario.hpp"
#include <stdexcept>

class Investigador : public PersonalUniversitario {
    int proyectos_;
    static constexpr float REMUNERACION_PROYECTO = 1500.0f;
public:
    Investigador(std::string dni, std::string nombres, std::string apellidos,
                 int proyectos)
        : PersonalUniversitario(std::move(dni), std::move(nombres), std::move(apellidos)),
          proyectos_(proyectos) {
        if (proyectos < 1)
            throw std::invalid_argument("Debe tener al menos 1 proyecto activo");
    }

    float calcularRemuneracion() const override {
        return proyectos_ * REMUNERACION_PROYECTO;
    }
};

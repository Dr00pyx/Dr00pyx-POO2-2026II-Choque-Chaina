#pragma once
#include "PersonalUniversitario.hpp"
#include <stdexcept>

class Administrativo : public PersonalUniversitario {
    float salarioBase_;
    float bono_;
public:
    Administrativo(std::string dni, std::string nombres, std::string apellidos,
                   float salarioBase, float bono = 0.0f)
        : PersonalUniversitario(std::move(dni), std::move(nombres), std::move(apellidos)),
          salarioBase_(salarioBase), bono_(bono) {
        if (salarioBase_ <= 0)
            throw std::invalid_argument("Salario base debe ser positivo");
    }

    float calcularRemuneracion() const override {
        return salarioBase_ + bono_;
    }
};

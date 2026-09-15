#pragma once
#include <string>

class PersonalUniversitario {
protected:
    std::string dni_;
    std::string nombres_;
    std::string apellidos_;
public:
    PersonalUniversitario(std::string dni, std::string nombres, std::string apellidos)
        : dni_(std::move(dni)), nombres_(std::move(nombres)), apellidos_(std::move(apellidos)) {}

    virtual ~PersonalUniversitario() = default; // destructor virtual obligatorio

    virtual float calcularRemuneracion() const = 0; // método virtual puro

    virtual std::string identificarse() const {
        return apellidos_ + ", " + nombres_ + " (DNI: " + dni_ + ")";
    }
};

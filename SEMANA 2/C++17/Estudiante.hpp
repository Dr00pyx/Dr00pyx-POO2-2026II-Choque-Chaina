#pragma once
#include <string>
#include <vector>
#include "Curso.hpp"

class Estudiante {
    std::string dni_;
    std::string nombre_;
    std::vector<Curso> cursosInscritos_; // composición: HAS-A

public:
    Estudiante(std::string dni, std::string nombre)
        : dni_(std::move(dni)), nombre_(std::move(nombre)) {}

    void inscribirCurso(const Curso& c) {
        cursosInscritos_.push_back(c);
    }

    std::string getNombre() const { return nombre_; }
    std::string getDni() const { return dni_; }

    void mostrarCursos() const {
        for (const auto& c : cursosInscritos_) {
            std::cout << c << std::endl;
        }
    }
};

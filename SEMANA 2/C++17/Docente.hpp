#pragma once
#include <string>
#include <vector>
#include "Curso.hpp"

class Docente {
    std::string dni_;
    std::string nombre_;
    std::vector<Curso> cursosAsignados_; // composición: HAS-A

public:
    Docente(std::string dni, std::string nombre)
        : dni_(std::move(dni)), nombre_(std::move(nombre)) {}

    void asignarCurso(const Curso& c) {
        cursosAsignados_.push_back(c);
    }

    std::string getNombre() const { return nombre_; }
    std::string getDni() const { return dni_; }

    void mostrarCursos() const {
        for (const auto& c : cursosAsignados_) {
            std::cout << c << std::endl;
        }
    }
};

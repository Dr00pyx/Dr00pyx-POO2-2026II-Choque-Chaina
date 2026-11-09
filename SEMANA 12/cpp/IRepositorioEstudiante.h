#pragma once

#include "Estudiante.h"
#include <optional>
#include <vector>

/**
 * @struct IRepositorioEstudiante
 * @brief Interfaz de abstracción para la persistencia (Principio DIP).
 */
struct IRepositorioEstudiante {
    virtual void guardar(const Estudiante& e) = 0;
    virtual std::optional<Estudiante> buscar(int cod) = 0;
    virtual std::vector<Estudiante> listar() const = 0;
    virtual ~IRepositorioEstudiante() = default;
};

#pragma once

#include "Estudiante.h"
#include <optional>
#include <vector>

/**
 * @struct IRepositorioEstudiante
 * @brief Interfaz de abstracción de persistencia (SRP y DIP).
 * 
 * Cumple con el Principio de Inversión de Dependencias (DIP):
 * Los módulos de alto nivel (ServicioEstudiante) no dependen de detalles de bajo nivel
 * (almacenamiento en memoria, archivos o bases de datos), sino de esta abstracción.
 */
struct IRepositorioEstudiante {
    virtual void guardar(const Estudiante& e) = 0;
    virtual std::optional<Estudiante> buscar(int codigo) const = 0;
    virtual std::vector<Estudiante> listar() const = 0;
    virtual ~IRepositorioEstudiante() = default;
};

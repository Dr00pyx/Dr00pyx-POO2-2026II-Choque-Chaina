#pragma once

#include "IRepositorioEstudiante.h"
#include <map>

/**
 * @class RepositorioMemoria
 * @brief Implementación en memoria para almacenamiento de estudiantes.
 */
class RepositorioMemoria : public IRepositorioEstudiante {
public:
    void guardar(const Estudiante& e) override {
        datos_[e.codigo()] = e;
    }

    std::optional<Estudiante> buscar(int cod) override {
        auto it = datos_.find(cod);
        if (it != datos_.end()) {
            return it->second;
        }
        return std::nullopt;
    }

    [[nodiscard]] std::vector<Estudiante> listar() const override {
        std::vector<Estudiante> resultado;
        resultado.reserve(datos_.size());
        for (const auto& [cod, est] : datos_) {
            resultado.push_back(est);
        }
        return resultado;
    }

private:
    std::map<int, Estudiante> datos_;
};

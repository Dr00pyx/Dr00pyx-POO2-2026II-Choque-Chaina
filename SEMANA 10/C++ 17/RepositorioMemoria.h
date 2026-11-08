#pragma once

#include "IRepositorioEstudiante.h"
#include <unordered_map>
#include <vector>

/**
 * @class RepositorioMemoria
 * @brief Implementación en memoria de IRepositorioEstudiante.
 * Ideal para pruebas unitarias, prototipado y ejecución rápida sin efectos secundarios en disco.
 */
class RepositorioMemoria : public IRepositorioEstudiante {
public:
    void guardar(const Estudiante& e) override {
        datos_[e.codigo()] = e;
    }

    std::optional<Estudiante> buscar(int codigo) const override {
        auto it = datos_.find(codigo);
        if (it != datos_.end()) {
            return it->second;
        }
        return std::nullopt;
    }

    std::vector<Estudiante> listar() const override {
        std::vector<Estudiante> lista;
        lista.reserve(datos_.size());
        for (const auto& [cod, est] : datos_) {
            lista.push_back(est);
        }
        return lista;
    }

private:
    std::unordered_map<int, Estudiante> datos_;
};

#pragma once

#include "Estudiante.h"
#include "IRepositorioEstudiante.h"
#include "estrategias.h"
#include <memory>
#include <optional>
#include <utility>
#include <vector>

/**
 * @class ServicioEstudiante
 * @brief Controlador en la arquitectura MVC. Orquesta cálculo y persistencia.
 */
class ServicioEstudiante {
public:
    ServicioEstudiante(IRepositorioEstudiante& repo, std::unique_ptr<IEstrategiaCalculo> calc)
        : repo_(repo), calc_(std::move(calc)) {}

    void set_estrategia(std::unique_ptr<IEstrategiaCalculo> calc) {
        calc_ = std::move(calc);
    }

    [[nodiscard]] const IEstrategiaCalculo* estrategia() const {
        return calc_.get();
    }

    void registrar(Estudiante& e) {
        if (calc_) {
            e.set_ppa(calc_->calcular(e.notas()));
        }
        repo_.guardar(e);
    }

    std::optional<Estudiante> buscar(int cod) {
        return repo_.buscar(cod);
    }

    [[nodiscard]] std::vector<Estudiante> listar() const {
        return repo_.listar();
    }

private:
    IRepositorioEstudiante& repo_;
    std::unique_ptr<IEstrategiaCalculo> calc_;
};

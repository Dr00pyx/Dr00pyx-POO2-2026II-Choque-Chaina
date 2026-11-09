#pragma once

#include "estrategias.h"
#include "Logger.h"
#include <memory>
#include <utility>
#include <vector>

/**
 * @class ContextoCalculoPPA
 * @brief Contexto de cálculo que almacena y gestiona la estrategia activa mediante std::unique_ptr.
 */
class ContextoCalculoPPA {
public:
    explicit ContextoCalculoPPA(std::unique_ptr<IEstrategiaCalculo> est)
        : est_(std::move(est)) {}

    void setEstrategia(std::unique_ptr<IEstrategiaCalculo> est) {
        if (est) {
            Logger::getInstance().log("Estrategia cambiada a " + est->nombre());
            est_ = std::move(est);
        }
    }

    [[nodiscard]] const IEstrategiaCalculo* getEstrategia() const {
        return est_.get();
    }

    [[nodiscard]] float calcular(const std::vector<float>& notas) const {
        if (!est_) return 0.0f;
        return est_->calcular(notas);
    }

private:
    std::unique_ptr<IEstrategiaCalculo> est_;
};

#pragma once
#include <vector>
#include <algorithm>
#include <memory>
#include <utility>

template<typename PersonalT>
class PlanillaIterador {
private:
    std::shared_ptr<std::vector<PersonalT>> ordenados_;
    typename std::vector<PersonalT>::iterator actual_;

public:
    explicit PlanillaIterador(std::vector<PersonalT> personal)
        : ordenados_(std::make_shared<std::vector<PersonalT>>(std::move(personal))) {
        std::sort(ordenados_->begin(), ordenados_->end(),
            [](const PersonalT& a, const PersonalT& b) {
                return a.calcularRemuneracion() > b.calcularRemuneracion();
            });
        actual_ = ordenados_->begin();
    }

    // Los operadores requeridos para range-for de C++
    PlanillaIterador& begin() {
        actual_ = ordenados_->begin();
        return *this;
    }

    PlanillaIterador end() {
        PlanillaIterador e(*this);
        e.actual_ = e.ordenados_->end();
        return e;
    }

    const PersonalT& operator*() const {
        return *actual_;
    }

    PlanillaIterador& operator++() {
        ++actual_;
        return *this;
    }

    bool operator!=(const PlanillaIterador& o) const {
        return actual_ != o.actual_;
    }
};

#pragma once
#include <unordered_map>
#include <vector>
#include <optional>
#include <functional>
#include <algorithm>
#include <numeric>
#include <stdexcept>
#include <cstddef>

/**
 * Template: Repositorio<Entidad, TipoID>
 * 
 * Capa de persistencia desacoplada en memoria mediante std::unordered_map.
 * Inyección de dependencia de la función extractora del ID en el constructor.
 */
template<typename Entidad, typename TipoID>
class Repositorio {
private:
    std::unordered_map<TipoID, Entidad> datos_;
    std::function<TipoID(const Entidad&)> fn_id_;

public:
    // Constructor: inyección de la función extractora de ID
    explicit Repositorio(std::function<TipoID(const Entidad&)> fn)
        : fn_id_(std::move(fn)) {}

    // ── CRUD Básico ──────────────────────────────────────────────────────────
    void guardar(Entidad entidad) {
        datos_[fn_id_(entidad)] = std::move(entidad);
    }

    std::optional<Entidad> buscar(const TipoID& id) const {
        auto it = datos_.find(id);
        if (it == datos_.end()) return std::nullopt;
        return it->second;
    }

    bool eliminar(const TipoID& id) {
        return datos_.erase(id) > 0;
    }

    // ── Consultas Principales ────────────────────────────────────────────────
    std::vector<Entidad> todos() const {
        std::vector<Entidad> resultado;
        resultado.reserve(datos_.size());
        for (const auto& [id, ent] : datos_) {
            resultado.push_back(ent);
        }
        return resultado;
    }

    template<typename Pred>
    std::vector<Entidad> filtrar(Pred pred) const {
        auto todos_ = todos();
        std::vector<Entidad> resultado;
        std::copy_if(todos_.begin(), todos_.end(), std::back_inserter(resultado), pred);
        return resultado;
    }

    template<typename Comp>
    std::vector<Entidad> ordenar(Comp comp) const {
        auto resultado = todos();
        std::sort(resultado.begin(), resultado.end(), comp);
        return resultado;
    }

    template<typename U, typename F>
    U acumular(U init, F f) const {
        return std::accumulate(datos_.begin(), datos_.end(), init,
            [&f](U acc, const auto& par) { return f(acc, par.second); });
    }

    std::size_t tamaño() const noexcept { return datos_.size(); }
    bool vacio() const noexcept { return datos_.empty(); }

    // ── Métodos Adicionales Requeridos en Actividad 1 ─────────────────────────
    template<typename Pred>
    std::size_t contar(Pred pred) const {
        auto v = todos();
        return static_cast<std::size_t>(std::count_if(v.begin(), v.end(), pred));
    }

    bool existe(const TipoID& id) const {
        return datos_.find(id) != datos_.end();
    }

    template<typename Pred>
    std::optional<Entidad> primero(Pred pred) const {
        auto v = todos();
        auto it = std::find_if(v.begin(), v.end(), pred);
        if (it != v.end()) {
            return *it;
        }
        return std::nullopt;
    }
};

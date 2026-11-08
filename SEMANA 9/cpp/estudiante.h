// estudiante.h — Clase Estudiante con C++17
#pragma once
#include <string>
#include <stdexcept>
#include <vector>
#include <numeric>
#include <optional>

class Estudiante {
public:
    Estudiante(int codigo, std::string nombre, float ppa, int ciclo)
        : codigo_(codigo), nombre_(std::move(nombre)), ppa_(ppa), ciclo_(ciclo) {
        if (codigo_ <= 0)
            throw std::invalid_argument("Codigo debe ser positivo");
        if (nombre_.empty())
            throw std::invalid_argument("Nombre no puede estar vacio");
        if (ppa_ < 0.0f || ppa_ > 20.0f)
            throw std::out_of_range("PPA debe estar entre 0 y 20");
    }

    // Getters (const correctness)
    [[nodiscard]] int codigo() const { return codigo_; }
    [[nodiscard]] std::string nombre() const { return nombre_; }
    [[nodiscard]] float ppa() const { return ppa_; }
    [[nodiscard]] int ciclo() const { return ciclo_; }

    // Agregar nota al semestre actual
    void agregar_nota(float nota) {
        if (nota < 0.0f || nota > 20.0f)
            throw std::out_of_range("Nota fuera de rango");
        notas_.push_back(nota);
    }

    // Calcular promedio — retorna nullopt si no hay notas
    [[nodiscard]] std::optional<float> calcular_promedio() const {
        if (notas_.empty()) return std::nullopt;
        float suma = std::accumulate(notas_.begin(), notas_.end(), 0.0f);
        return suma / static_cast<float>(notas_.size());
    }

    [[nodiscard]] std::string to_string() const {
        return "[" + std::to_string(codigo_) + "] " + nombre_
            + " — PPA: " + std::to_string(ppa_)
            + " — Ciclo: " + std::to_string(ciclo_);
    }

    // ADICIONAL (Actividad 2A): Método es_aprobado() -> bool (PPA >= 11)
    [[nodiscard]] bool es_aprobado() const {
        return ppa_ >= 11.0f;
    }

    // Getter para consultar la lista de notas
    [[nodiscard]] const std::vector<float>& notas() const {
        return notas_;
    }

private:
    int codigo_;
    std::string nombre_;
    float ppa_;
    int ciclo_;
    std::vector<float> notas_;
};

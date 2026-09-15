// ── personal_unap.hpp — Práctica S3, Actividad 4 ────────────────────────
#pragma once
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>
#include <iostream>
#include <iomanip>

// Clase base abstracta
class PersonalUniversitario {
protected:
    std::string dni_;
    std::string nombres_;
    std::string apellidos_;
public:
    PersonalUniversitario(std::string dni,
                          std::string nombres,
                          std::string apellidos)
        : dni_(std::move(dni)),
          nombres_(std::move(nombres)),
          apellidos_(std::move(apellidos)) {}

    virtual ~PersonalUniversitario() = default; // destructor virtual OBLIGATORIO

    // Método virtual puro: contrato que TODAS las subclases deben implementar
    virtual float calcularRemuneracion() const = 0;

    virtual std::string identificarse() const {
        return apellidos_ + ", " + nombres_ + " (DNI: " + dni_ + ")";
    }
};

// ── Subclase Docente ───────────────────────────────────────────────────
class Docente : public PersonalUniversitario {
    int horas_;
    float tarifa_ = 75.0f;
    float factor_;

    static float resolverFactor(const std::string& cat) {
        if (cat == "Auxiliar") return 1.0f;
        if (cat == "Asociado") return 1.4f;
        if (cat == "Principal") return 1.8f;
        throw std::invalid_argument("Categoría inválida: " + cat);
    }
public:
    Docente(std::string dni, std::string nombres, std::string apellidos,
            int horas, const std::string& categoria)
        : PersonalUniversitario(std::move(dni), std::move(nombres),
                                std::move(apellidos)),
          horas_(horas), factor_(resolverFactor(categoria)) {
        if (horas <= 0 || horas > 40)
            throw std::invalid_argument("Horas fuera de rango [1,40]");
    }

    float calcularRemuneracion() const override {
        return horas_ * tarifa_ * factor_;
    }
};

// ── Subclase Administrativo ────────────────────────────────────────────
class Administrativo : public PersonalUniversitario {
    float salarioBase_;
    float bono_;
public:
    Administrativo(std::string dni, std::string nombres, std::string apellidos,
                   float salarioBase, float bono = 0.0f)
        : PersonalUniversitario(std::move(dni), std::move(nombres),
                                std::move(apellidos)),
          salarioBase_(salarioBase), bono_(bono) {
        if (salarioBase_ <= 0)
            throw std::invalid_argument("Salario base debe ser positivo");
    }

    float calcularRemuneracion() const override {
        return salarioBase_ + bono_;
    }
};

// ── Subclase Investigador ──────────────────────────────────────────────
class Investigador : public PersonalUniversitario {
    int proyectos_;
    static constexpr float REMUNERACION_PROYECTO = 1500.0f;
public:
    Investigador(std::string dni, std::string nombres, std::string apellidos,
                 int proyectos)
        : PersonalUniversitario(std::move(dni), std::move(nombres),
                                std::move(apellidos)),
          proyectos_(proyectos) {
        if (proyectos < 1)
            throw std::invalid_argument("Debe tener al menos 1 proyecto activo");
    }

    float calcularRemuneracion() const override {
        return proyectos_ * REMUNERACION_PROYECTO;
    }
};

// ── Función planilla() — demuestra polimorfismo dinámico ───────────────
void planilla(const std::vector<std::unique_ptr<PersonalUniversitario>>& p) {
    float total = 0.0f;
    std::cout << std::string(60, '=') << "\n";
    std::cout << "PLANILLA PERSONAL UNIVERSITARIO — UNAP PUNO\n";
    std::cout << std::string(60, '=') << "\n";
    for (const auto& persona : p) {
        std::cout << std::fixed << std::setprecision(2)
                  << persona->identificarse()
                  << " S/ " << persona->calcularRemuneracion() << "\n";
        total += persona->calcularRemuneracion();
    }
    std::cout << std::string(60, '-') << "\n";
    std::cout << "TOTAL: S/ " << total << "\n";
}

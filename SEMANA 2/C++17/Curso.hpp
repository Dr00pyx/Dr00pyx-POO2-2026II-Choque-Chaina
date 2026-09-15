// Curso.hpp — Práctica S2, Actividad 3
#pragma once

#include <string>
#include <regex>
#include <stdexcept>
#include <iostream>

class Curso {
private:
    std::string codigo_;
    std::string nombre_;
    int creditos_;
    int cuposMaximo_;
    int inscritos_ = 0; // inicializado en declaración

public:
    // --- Constructor -------------------------------------------------
    Curso(const std::string& codigo, const std::string& nombre,
          int creditos, int cuposMaximo)
        : nombre_(nombre) {
        setCodigo(codigo);
        setCreditos(creditos);
        setCuposMaximo(cuposMaximo);
    }

    // --- Setters con validación --------------------------------------
    void setCodigo(const std::string& cod) {
        static const std::regex patron("^SIS[0-9]{3}$");
        if (!std::regex_match(cod, patron)) {
            throw std::invalid_argument("Codigo invalido: debe tener formato SIS###");
        }
        codigo_ = cod;
    }

    void setCreditos(int c) {
        if (c < 1 || c > 6) {
            throw std::invalid_argument("Creditos fuera de rango [1,6]");
        }
        creditos_ = c;
    }

    void setCuposMaximo(int q) {
        if (q < 1 || q > 50) {
            throw std::invalid_argument("Cupos fuera de rango [1,50]");
        }
        cuposMaximo_ = q;
    }

    // --- Getters (const — no modifican el objeto) --------------------
    const std::string& getCodigo() const { return codigo_; }
    const std::string& getNombre() const { return nombre_; }
    int getCreditos() const { return creditos_; }
    int getCuposMaximo() const { return cuposMaximo_; }
    int getInscritos() const { return inscritos_; }

    // --- Propiedades calculadas (const) ------------------------------
    int cuposDisponibles() const {
        return cuposMaximo_ - inscritos_;
    }

    bool estaLleno() const {
        return inscritos_ >= cuposMaximo_;
    }

    // --- Lógica de negocio -------------------------------------------
    void inscribirEstudiante() {
        if (estaLleno()) {
            throw std::runtime_error("Curso sin cupos disponibles");
        }
        ++inscritos_;
    }

    // --- Representación en string ------------------------------------
    friend std::ostream& operator<<(std::ostream& os, const Curso& c) {
        os << c.codigo_ << " - " << c.nombre_
           << " (" << c.creditos_ << " cr)"
           << " [" << c.inscritos_ << "/" << c.cuposMaximo_ << " inscritos]";
        return os;
    }
};

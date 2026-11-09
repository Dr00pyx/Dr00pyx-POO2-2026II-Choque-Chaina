#pragma once

#include <iomanip>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

/**
 * @class Estudiante
 * @brief Entidad de dominio pura (SRP). Modela código, nombre, PPA y notas.
 */
class Estudiante {
public:
    Estudiante() : codigo_(0), nombre_(""), ppa_(0.0f) {}

    Estudiante(int cod, std::string nom, float ppa = 0.0f, std::vector<float> notas = {})
        : codigo_(cod), nombre_(std::move(nom)), ppa_(ppa), notas_(std::move(notas)) {}

    [[nodiscard]] int codigo() const { return codigo_; }
    [[nodiscard]] const std::string& nombre() const { return nombre_; }
    [[nodiscard]] float ppa() const { return ppa_; }
    [[nodiscard]] const std::vector<float>& notas() const { return notas_; }

    void set_ppa(float v) { ppa_ = v; }
    void set_nombre(std::string nom) { nombre_ = std::move(nom); }
    void set_codigo(int cod) { codigo_ = cod; }
    void set_notas(std::vector<float> notas) { notas_ = std::move(notas); }

    [[nodiscard]] std::string to_string() const {
        std::ostringstream oss;
        oss << "[" << codigo_ << "] " << nombre_ << " — PPA: " << std::fixed << std::setprecision(1) << ppa_;
        return oss.str();
    }

private:
    int codigo_;
    std::string nombre_;
    float ppa_;
    std::vector<float> notas_;
};

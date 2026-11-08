#pragma once

#include <string>
#include <utility>

/**
 * @class Estudiante
 * @brief Entidad de dominio pura (SRP: Solo modela los datos de un estudiante).
 * 
 * Tiene una única razón para cambiar: Modificaciones en los atributos
 * de la entidad estudiante en el dominio del Sistema Académico UNAP.
 */
class Estudiante {
public:
    Estudiante() : codigo_(0), nombre_(""), ppa_(0.0f) {}

    Estudiante(int cod, std::string nom, float ppa = 0.0f)
        : codigo_(cod), nombre_(std::move(nom)), ppa_(ppa) {}

    [[nodiscard]] int codigo() const { return codigo_; }
    [[nodiscard]] const std::string& nombre() const { return nombre_; }
    [[nodiscard]] float ppa() const { return ppa_; }

    void set_ppa(float v) { ppa_ = v; }
    void set_nombre(std::string nom) { nombre_ = std::move(nom); }
    void set_codigo(int cod) { codigo_ = cod; }

private:
    int codigo_;
    std::string nombre_;
    float ppa_;
};

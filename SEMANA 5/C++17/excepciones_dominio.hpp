// ── excepciones_dominio.hpp ──────────────────────────────────────────────
#pragma once

#include <stdexcept>   // std::runtime_error
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>   // std::find

// ── Raiz de dominio: hereda de std::runtime_error ─────────────────────────
class ErrorAcademico : public std::runtime_error {
public:
    explicit ErrorAcademico(const std::string& msg)
        : std::runtime_error("[Academico] " + msg) {}
};

// ── Primer nivel de especializacion ────────────────────────────────────────
class ErrorValidacion : public ErrorAcademico {
public:
    explicit ErrorValidacion(const std::string& msg)
        : ErrorAcademico("[Validacion] " + msg) {}
};

// ── Segundo nivel: error con valor concreto (calificacion) ────────────────
class ErrorCalificacion : public ErrorValidacion {
    float valor_;

public:
    explicit ErrorCalificacion(float v)
        : ErrorValidacion("Calificacion " + std::to_string(v) + " fuera de rango [0, 20]"),
          valor_(v) {}

    float valor() const noexcept { return valor_; }
};

// ── Segundo nivel: error con codigo de estudiante (matricula duplicada) ───
class ErrorMatriculaDuplicada : public ErrorValidacion {
    std::string codigo_estudiante_; // Atributo contextual

public:
    explicit ErrorMatriculaDuplicada(std::string codigo)
        : ErrorValidacion("Estudiante con codigo " + codigo + " ya se encuentra matriculado"),
          codigo_estudiante_(std::move(codigo)) {}

    explicit ErrorMatriculaDuplicada(int codigo)
        : ErrorMatriculaDuplicada(std::to_string(codigo)) {}

    const std::string& codigo_estudiante() const noexcept {
        return codigo_estudiante_;
    }
};

// ── Otros errores del marco teorico de dominio ────────────────────────────
class ErrorCapacidad : public ErrorAcademico {
    int actual_, maximo_;

public:
    ErrorCapacidad(int actual, int maximo, const std::string& entidad)
        : ErrorAcademico(entidad + ": capacidad agotada ("
          + std::to_string(actual) + "/"
          + std::to_string(maximo) + ")"),
          actual_(actual), maximo_(maximo) {}

    int actual() const noexcept { return actual_; }
    int maximo() const noexcept { return maximo_; }
};

class ErrorRecursoNoEncontrado : public ErrorAcademico {
    std::string tipo_;
    int id_;

public:
    ErrorRecursoNoEncontrado(std::string tipo, int id)
        : ErrorAcademico(tipo + " id=" + std::to_string(id) + " no encontrado"),
          tipo_(std::move(tipo)), id_(id) {}

    const std::string& tipo() const noexcept { return tipo_; }
    int id() const noexcept { return id_; }
};

// ── Funcion de validacion de matricula requerida ───────────────────────────
inline void validar_matricula(int codigo, std::vector<int>& matriculados) {
    if (std::find(matriculados.begin(), matriculados.end(), codigo) != matriculados.end()) {
        throw ErrorMatriculaDuplicada(codigo);
    }
}

inline void validar_matricula(int codigo, const std::vector<int>& matriculados) {
    if (std::find(matriculados.begin(), matriculados.end(), codigo) != matriculados.end()) {
        throw ErrorMatriculaDuplicada(codigo);
    }
}
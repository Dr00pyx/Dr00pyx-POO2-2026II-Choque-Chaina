// ── main.cpp ─────────────────────────────────────────────────────────────
#include "excepciones_dominio.hpp"
#include <iostream>
#include <vector>

// Funcion auxiliar para probar el bloque try/catch con orden estricto de captura
template <typename Func>
void procesar_operacion(const std::string& descripcion, Func operacion) {
    std::cout << "\n----------------------------------------\n";
    std::cout << "Ejecutando: " << descripcion << "\n";
    std::cout << "----------------------------------------\n";

    try {
        operacion();
        std::cout << "-> Operacion completada con EXITO (sin excepciones).\n";
    }
    // ── 1. Nivel mas especifico (hojas derivadas) ──────────────────────────
    catch (const ErrorMatriculaDuplicada& e) {
        std::cout << "[CAPTURADO: ErrorMatriculaDuplicada]\n";
        std::cout << "  Mensaje: " << e.what() << "\n";
        std::cout << "  Codigo de estudiante infractor: " << e.codigo_estudiante() << "\n";
    }
    catch (const ErrorCalificacion& e) {
        std::cout << "[CAPTURADO: ErrorCalificacion]\n";
        std::cout << "  Mensaje: " << e.what() << "\n";
        std::cout << "  Valor erroneo: " << e.valor() << "\n";
    }
    // ── 2. Nivel intermedio (clase base de validaciones) ───────────────────
    catch (const ErrorValidacion& e) {
        std::cout << "[CAPTURADO: ErrorValidacion (generico)]\n";
        std::cout << "  Mensaje: " << e.what() << "\n";
    }
    // ── 3. Raiz del dominio academico ─────────────────────────────────────
    catch (const ErrorAcademico& e) {
        std::cout << "[CAPTURADO: ErrorAcademico (generico de dominio)]\n";
        std::cout << "  Mensaje: " << e.what() << "\n";
    }
    // ── 4. Estandar C++ (errores de sistema/STL) ──────────────────────────
    catch (const std::exception& e) {
        std::cout << "[CAPTURADO: std::exception]\n";
        std::cout << "  Mensaje: " << e.what() << "\n";
    }
    // ── 5. Captura comodin para cualquier otro tipo desconocido ───────────
    catch (...) {
        std::cout << "[CAPTURADO: Excepcion desconocida (...)]\n";
    }
}

int main() {
    std::cout << "====================================================\n";
    std::cout << "  DEMOSTRACION DE CAPTURA SELECTIVA EN ORDEN CORRECTO\n";
    std::cout << "====================================================\n";

    std::vector<int> matriculados = {2021001, 2021002, 2021003};

    // Caso 1: Intentar matricular un codigo duplicado
    procesar_operacion("Validar matricula para estudiante existente (2021002)", [&]() {
        int codigo = 2021002;
        validar_matricula(codigo, matriculados);
        matriculados.push_back(codigo);
    });

    // Caso 2: Matricula exitosa de un estudiante nuevo
    procesar_operacion("Validar y registrar estudiante nuevo (2021004)", [&]() {
        int codigo = 2021004;
        validar_matricula(codigo, matriculados);
        matriculados.push_back(codigo);
        std::cout << "  Estudiante " << codigo << " matriculado correctamente.\n";
    });

    // Caso 3: Error de calificacion fuera de rango
    procesar_operacion("Registrar calificacion invalida (22.5)", []() {
        float nota = 22.5f;
        if (nota < 0.0f || nota > 20.0f) {
            throw ErrorCalificacion(nota);
        }
    });

    // Caso 4: Error de validacion generico (no es matricula ni calificacion)
    procesar_operacion("Validacion generica de documento de identidad vacio", []() {
        throw ErrorValidacion("El DNI del estudiante no puede estar vacio");
    });

    // Caso 5: Error de dominio general (ErrorCapacidad hereda de ErrorAcademico)
    procesar_operacion("Exceder capacidad maxima de aula", []() {
        throw ErrorCapacidad(40, 40, "Laboratorio de C++");
    });

    return 0;
}
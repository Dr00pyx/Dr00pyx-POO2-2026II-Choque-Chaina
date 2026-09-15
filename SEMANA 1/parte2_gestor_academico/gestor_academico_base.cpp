// Código monolítico defectuoso en C++ (Base para la Parte 2)

#include <iostream>
#include <vector>
#include <string>
#include <fstream>

struct EstudianteBase {
    std::string codigo;
    std::string nombre;
    std::vector<double> notas;
};

class GestorAcademicoMonolitico {
public:
    std::vector<EstudianteBase> estudiantes; // Estado expuesto

    void agregarEstudiante(const std::string& codigo, const std::string& nombre) {
        estudiantes.push_back({codigo, nombre, {}});
        std::ofstream auditoria("auditoria.txt", std::ios::app);
        auditoria << "Estudiante agregado: " << codigo << " - " << nombre << "\n";
    }

    void agregarNota(const std::string& codigo, double nota) {
        // No valida que la nota esté entre 0 y 20
        for (auto& est : estudiantes) {
            if (est.codigo == codigo) {
                est.notas.push_back(nota);
                std::ofstream auditoria("auditoria.txt", std::ios::app);
                auditoria << "Nota " << nota << " agregada a " << codigo << "\n";
            }
        }
    }

    void generarReporte() {
        std::ofstream reporte("reporte.csv");
        reporte << "codigo,nombre,promedio,estado\n";
        for (const auto& est : estudiantes) {
            double suma = 0.0;
            for (double n : est.notas) suma += n;
            double promedio = est.notas.empty() ? 0.0 : suma / est.notas.size();
            std::string estado = (promedio >= 10.5) ? "APROBADO" : "DESAPROBADO";
            reporte << est.codigo << "," << est.nombre << "," << promedio << "," << estado << "\n";
        }
    }
};
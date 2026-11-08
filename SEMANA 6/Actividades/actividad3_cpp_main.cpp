#include "iterador_planilla.hpp"
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>

struct EmpleadoUNAP {
    std::string dni;
    std::string nombre;
    std::string cargo;
    double salarioBase;
    double bono;

    double calcularRemuneracion() const {
        return salarioBase + bono;
    }
};

int main() {
    std::cout << "===============================================================\n";
    std::cout << "ACTIVIDAD 3 (C++): ITERADOR PERSONALIZADO PlanillaIterador\n";
    std::cout << "===============================================================\n\n";

    std::vector<EmpleadoUNAP> personal = {
        {"70112233", "Carlos Mamani Quispe", "Docente Principal", 5500.0, 1200.0},
        {"70223344", "Ana Luisa Ramos", "Docente Auxiliar", 2800.0, 450.0},
        {"70334455", "Jorge Condori Apaza", "Jefe de Practica", 2200.0, 300.0},
        {"70445566", "Elena Flores Coila", "Docente Asociado", 4200.0, 800.0},
        {"70556677", "Marcos Choque Pari", "Administrativo II", 2600.0, 500.0}
    };

    std::cout << "Personal original ingresado: " << personal.size() << " trabajadores\n";
    std::cout << "\nRecorrido con range-based for sobre PlanillaIterador (ordenado por remuneracion desc):\n";
    std::cout << "------------------------------------------------------------------------------------\n";

    int ranking = 1;
    // Usando el range-based for de C++ directamente sobre el iterador personalizado
    for (const auto& emp : PlanillaIterador<EmpleadoUNAP>(personal)) {
        std::cout << "  " << ranking++ << ". "
                  << std::left << std::setw(25) << emp.nombre
                  << " | " << std::left << std::setw(20) << emp.cargo
                  << " | Remuneracion: S/ " << std::fixed << std::setprecision(2)
                  << emp.calcularRemuneracion() << "\n";
    }

    std::cout << "===============================================================\n";
    return 0;
}

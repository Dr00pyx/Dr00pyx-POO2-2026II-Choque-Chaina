#include <iostream>
#include "Curso.hpp"
#include "Docente.hpp"
#include "Estudiante.hpp"

int main() {
    try {
        Curso poo2("SIS206", "POO II", 4, 30);
        Curso bd("SIS207", "Base de Datos", 3, 25);

        Docente docente("12345678", "Juan Carlos Mamani");
        docente.asignarCurso(poo2);
        docente.asignarCurso(bd);

        Estudiante estudiante("87654321", "María Quispe");
        estudiante.inscribirCurso(poo2);

        std::cout << "Docente: " << docente.getNombre() << "\nCursos asignados:\n";
        docente.mostrarCursos();

        std::cout << "\nEstudiante: " << estudiante.getNombre() << "\nCursos inscritos:\n";
        estudiante.mostrarCursos();

    } catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << std::endl;
    }

    return 0;
}

#include "repositorio.hpp"
#include <iostream>
#include <iomanip>
#include <string>

struct Estudiante {
    int codigo;
    std::string nombre;
    float ppa;
    std::string escuela;
};

struct Curso {
    std::string codigo;
    std::string nombre;
    int creditos;
    int ciclo;
};

int main() {
    std::cout << "===============================================================\n";
    std::cout << "ACTIVIDAD 1: REPOSITORIO GENERICO EN C++17 (TEMPLATES STL)\n";
    std::cout << "===============================================================\n\n";

    // -------------------------------------------------------------------------
    // 1. Instanciación 1: Repositorio<Estudiante, int>
    // -------------------------------------------------------------------------
    std::cout << ">>> 1. DEMOSTRACION CON ENTIDAD 'Estudiante' (ID: int)\n";
    Repositorio<Estudiante, int> repoEstudiantes(
        [](const Estudiante& e) { return e.codigo; }
    );

    // Guardar 5 estudiantes
    repoEstudiantes.guardar({1001, "Juan Carlos Mamani", 15.2f, "Ing. Sistemas"});
    repoEstudiantes.guardar({1002, "Maria Elena Quispe", 18.5f, "Ing. Sistemas"});
    repoEstudiantes.guardar({1003, "Pedro Flores", 9.8f, "Ciencias Comp."});
    repoEstudiantes.guardar({1004, "Ana Torres", 13.0f, "Ing. Sistemas"});
    repoEstudiantes.guardar({1005, "Carlos Condori", 16.8f, "Ing. Sistemas"});

    std::cout << "Total estudiantes registrados: " << repoEstudiantes.tamaño() << "\n\n";

    // Metodo existe(id)
    std::cout << "[existe(1002)]: " << (repoEstudiantes.existe(1002) ? "SI existe" : "NO existe") << "\n";
    std::cout << "[existe(9999)]: " << (repoEstudiantes.existe(9999) ? "SI existe" : "NO existe") << "\n\n";

    // Metodo buscar(id) -> std::optional
    std::cout << "[buscar(1001)]: ";
    if (auto res = repoEstudiantes.buscar(1001); res.has_value()) {
        std::cout << "Encontrado -> " << res->nombre << " (PPA: " << res->ppa << ", " << res->escuela << ")\n";
    } else {
        std::cout << "No encontrado.\n";
    }
    std::cout << "\n";

    // Metodo contar(pred)
    auto cantDestacados = repoEstudiantes.contar([](const Estudiante& e) { return e.ppa >= 14.0f; });
    std::cout << "[contar(PPA >= 14.0)]: " << cantDestacados << " estudiantes\n\n";

    // Metodo primero(pred) -> std::optional
    std::cout << "[primero(escuela == 'Ciencias Comp.')]: ";
    auto primerCC = repoEstudiantes.primero([](const Estudiante& e) { return e.escuela == "Ciencias Comp."; });
    if (primerCC) {
        std::cout << primerCC->nombre << " (Codigo: " << primerCC->codigo << ")\n\n";
    }

    // Metodo filtrar(pred)
    std::cout << "[filtrar(PPA >= 14.0f)]:\n";
    auto destacados = repoEstudiantes.filtrar([](const Estudiante& e) { return e.ppa >= 14.0f; });
    for (const auto& e : destacados) {
        std::cout << "  - [" << e.codigo << "] " << std::left << std::setw(22) << e.nombre 
                  << " | PPA: " << std::fixed << std::setprecision(2) << e.ppa << "\n";
    }
    std::cout << "\n";

    // Metodo ordenar(comp)
    std::cout << "[ordenar(PPA descendente)]:\n";
    auto ranking = repoEstudiantes.ordenar(
        [](const Estudiante& a, const Estudiante& b) { return a.ppa > b.ppa; }
    );
    int pos = 1;
    for (const auto& e : ranking) {
        std::cout << "  " << pos++ << ". [" << e.codigo << "] " << std::left << std::setw(22) 
                  << e.nombre << " | PPA: " << std::fixed << std::setprecision(2) << e.ppa 
                  << " (" << e.escuela << ")\n";
    }
    std::cout << "\n";

    // Metodo acumular(init, f)
    float sumaPpa = repoEstudiantes.acumular(0.0f, [](float acc, const Estudiante& e) {
        return acc + e.ppa;
    });
    float promedioPpa = sumaPpa / static_cast<float>(repoEstudiantes.tamaño());
    std::cout << "[acumular]: Suma PPA = " << sumaPpa 
              << " | Promedio PPA = " << std::fixed << std::setprecision(2) << promedioPpa << "\n\n";

    // -------------------------------------------------------------------------
    // 2. Instanciación 2: Repositorio<Curso, std::string>
    // -------------------------------------------------------------------------
    std::cout << "---------------------------------------------------------------\n";
    std::cout << ">>> 2. DEMOSTRACION CON SEGUNDA ENTIDAD 'Curso' (ID: std::string)\n";
    Repositorio<Curso, std::string> repoCursos(
        [](const Curso& c) { return c.codigo; }
    );

    repoCursos.guardar({"SIS206", "Programacion Orientada a Objetos II", 4, 4});
    repoCursos.guardar({"SIS201", "Algoritmos y Estructuras de Datos", 4, 3});
    repoCursos.guardar({"MAT101", "Calculo Diferencial e Integral", 5, 1});
    repoCursos.guardar({"SIS305", "Base de Datos Avanzadas", 3, 5});

    std::cout << "Total cursos registrados: " << repoCursos.tamaño() << "\n\n";

    // buscar y existe en Cursos
    std::cout << "[existe('SIS206')]: " << (repoCursos.existe("SIS206") ? "SI" : "NO") << "\n";
    std::cout << "[buscar('SIS206')]: ";
    if (auto c = repoCursos.buscar("SIS206"); c) {
        std::cout << c->nombre << " (" << c->creditos << " creditos, Ciclo " << c->ciclo << ")\n";
    }
    std::cout << "\n";

    // filtrar cursos con creditos >= 4
    std::cout << "[filtrar(creditos >= 4)]:\n";
    auto cursosPesados = repoCursos.filtrar([](const Curso& c) { return c.creditos >= 4; });
    for (const auto& c : cursosPesados) {
        std::cout << "  - [" << c.codigo << "] " << std::left << std::setw(38) << c.nombre 
                  << " | " << c.creditos << " creds.\n";
    }
    std::cout << "\n";

    // ordenar alfabeticamente por nombre
    std::cout << "[ordenar(nombre ascendente)]:\n";
    auto cursosOrdenados = repoCursos.ordenar([](const Curso& a, const Curso& b) {
        return a.nombre < b.nombre;
    });
    for (const auto& c : cursosOrdenados) {
        std::cout << "  - [" << c.codigo << "] " << c.nombre << " (Ciclo " << c.ciclo << ")\n";
    }

    std::cout << "\n===============================================================\n";
    std::cout << "FIN ACTIVIDAD 1\n";
    std::cout << "===============================================================\n";
    return 0;
}

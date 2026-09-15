#include "Docente.hpp"
#include "Administrativo.hpp"
#include "Investigador.hpp"
#include "planilla.hpp"
#include "Rectangulo.hpp"
#include "Cuadrado.hpp"
#include <memory>
#include <vector>
#include <iostream>
#include <cassert>

void testRectangulo(Rectangulo& r) {
    r.setAncho(4);
    r.setAlto(5);
    float esperado = 20.0f;
    assert(r.area() == esperado && "LSP violado: área incorrecta");
}

int main() {
    std::vector<std::unique_ptr<PersonalUniversitario>> personal;
    personal.push_back(std::make_unique<Docente>("12345678","Juan Carlos","Mamani Quispe",16,"Asociado"));
    personal.push_back(std::make_unique<Docente>("23456789","María Elena","Quispe Torres",12,"Principal"));
    personal.push_back(std::make_unique<Administrativo>("34567890","Pedro","Huanca Lazo",2800.0f,350.0f));
    personal.push_back(std::make_unique<Investigador>("45678901","Ana Lucía","Flores Ramos",2));

    planilla(personal);

    // LSP test
    Rectangulo rect(2,2);
    testRectangulo(rect); // OK

    Cuadrado cuad(2);
    try {
        testRectangulo(cuad); // FALLA
    } catch (...) {
        std::cout << "LSP VIOLADO en Cuadrado: área no coincide con lo esperado\n";
        std::cout << "Solución: no heredar Cuadrado de Rectángulo; usar interfaz independiente.\n";
    }

    return 0;
}

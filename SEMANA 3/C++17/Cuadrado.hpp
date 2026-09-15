#pragma once
#include "Rectangulo.hpp"
#include <stdexcept>

class Cuadrado : public Rectangulo {
public:
    Cuadrado(float lado) : Rectangulo(lado, lado) {}
    void setAncho(float v) override {
        ancho_ = v;
        alto_ = v; // fuerza lados iguales
    }
    void setAlto(float v) override {
        ancho_ = v;
        alto_ = v; // fuerza lados iguales
    }
};

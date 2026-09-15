#pragma once
#include "Figura.hpp"

class Rectangulo : public Figura {
protected:
    float ancho_;
    float alto_;
public:
    Rectangulo(float ancho, float alto) : ancho_(ancho), alto_(alto) {}
    virtual void setAncho(float v) { ancho_ = v; }
    virtual void setAlto(float v) { alto_ = v; }
    float area() const override { return ancho_ * alto_; }
};

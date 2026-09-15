#pragma once

class Figura {
public:
    virtual ~Figura() = default;
    virtual float area() const = 0;
};

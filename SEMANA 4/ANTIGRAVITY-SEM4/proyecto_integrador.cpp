#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <unordered_map>
#include <utility>

// ── 1. Interfaz Pura (Contrato) ──────────────────────────────────────────
class IAlmacenable {
public:
    virtual ~IAlmacenable() = default;
    virtual bool guardar(const std::string& clave, const std::string& datos) = 0;
    virtual std::string recuperar(const std::string& clave) const = 0;
    virtual size_t totalRegistros() const = 0;
};

// ── 2. Implementación Concreta de la Interfaz ────────────────────────────
class RepositorioMemoria : public IAlmacenable {
private:
    std::unordered_map<std::string, std::string> tabla_;

public:
    bool guardar(const std::string& clave, const std::string& datos) override {
        tabla_[clave] = datos;
        return true;
    }

    std::string recuperar(const std::string& clave) const override {
        auto it = tabla_.find(clave);
        return (it != tabla_.end()) ? it->second : "";
    }

    size_t totalRegistros() const override {
        return tabla_.size();
    }
};

// ── 3. Dominio: Personal Universitario (Polimorfismo) ────────────────────
class PersonalUniversitario {
protected:
    std::string dni_;
    std::string nombres_;
    std::string apellidos_;

public:
    PersonalUniversitario(std::string dni, std::string nombres, std::string apellidos)
        : dni_(std::move(dni)), nombres_(std::move(nombres)), apellidos_(std::move(apellidos)) {}

    virtual ~PersonalUniversitario() = default;

    std::string getDni() const { return dni_; }
    std::string getNombreCompleto() const { return apellidos_ + ", " + nombres_; }

    virtual double calcularRemuneracion() const = 0;
    virtual std::string serializar() const {
        return "DNI: " + dni_ + " | " + getNombreCompleto() + " | S/ " + std::to_string(calcularRemuneracion());
    }
};

class Docente : public PersonalUniversitario {
private:
    int horas_;
    double tarifaBase_ = 75.0;
    double factorCategoria_;

public:
    Docente(std::string dni, std::string nombres, std::string apellidos, int horas, double factor)
        : PersonalUniversitario(std::move(dni), std::move(nombres), std::move(apellidos)),
          horas_(horas), factorCategoria_(factor) {}

    double calcularRemuneracion() const override {
        return horas_ * tarifaBase_ * factorCategoria_;
    }
};

class Administrativo : public PersonalUniversitario {
private:
    double salarioBase_;
    double bono_;

public:
    Administrativo(std::string dni, std::string nombres, std::string apellidos, double salarioBase, double bono)
        : PersonalUniversitario(std::move(dni), std::move(nombres), std::move(apellidos)),
          salarioBase_(salarioBase), bono_(bono) {}

    double calcularRemuneracion() const override {
        return salarioBase_ + bono_;
    }
};

// ── 4. Clase Consumidora: Composición e Inyección de Dependencias ────────
class GestorPersonalUniversitario {
private:
    std::unique_ptr<IAlmacenable> repositorio_; // Composición: HAS-A
    std::vector<std::unique_ptr<PersonalUniversitario>> personal_;

public:
    // Inyección de dependencias en el constructor
    explicit GestorPersonalUniversitario(std::unique_ptr<IAlmacenable> repo)
        : repositorio_(std::move(repo)) {}

    void registrarPersonal(std::unique_ptr<PersonalUniversitario> p) {
        repositorio_->guardar(p->getDni(), p->serializar());
        personal_.push_back(std::move(p));
    }

    double calcularTotalPlanilla() const {
        double total = 0.0;
        for (const auto& p : personal_) {
            total += p->calcularRemuneracion();
        }
        return total;
    }

    void emitirReporte() const {
        std::cout << "========================================================\n";
        std::cout << "PLANILLA UNAP PUNO - C++17 (COMPOSICION + DI)\n";
        std::cout << "========================================================\n";
        for (const auto& p : personal_) {
            std::cout << "- " << p->getNombreCompleto() << " -> S/ "
                      << p->calcularRemuneracion() << "\n";
        }
        std::cout << "--------------------------------------------------------\n";
        std::cout << "TOTAL PLANILLA: S/ " << calcularTotalPlanilla() << "\n";
        std::cout << "REGISTROS PERSISTIDOS EN REPOSITORIO: " << repositorio_->totalRegistros() << "\n";
        std::cout << "========================================================\n";
    }
};

int main() {
    auto repo = std::make_unique<RepositorioMemoria>();
    GestorPersonalUniversitario gestor(std::move(repo));

    gestor.registrarPersonal(std::make_unique<Docente>("12345678", "Juan Carlos", "Mamani Quispe", 16, 1.4));
    gestor.registrarPersonal(std::make_unique<Administrativo>("34567890", "Pedro", "Huanca Lazo", 2800.0, 350.0));

    gestor.emitirReporte();
    return 0;
}
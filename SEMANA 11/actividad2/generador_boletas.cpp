#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <map>
#include <functional>
#include <fstream>
#include <iomanip>

// ── Producto Abstracto ──────────────────────────────────
class BoletaNotas {
protected:
    std::string estudiante_;
    std::string codigo_;
    std::string semestre_;
    struct NotaItem {
        std::string curso;
        double nota;
        int creditos;
    };
    std::vector<NotaItem> notas_;

public:
    virtual ~BoletaNotas() = default;

    void setDatos(const std::string& est, const std::string& cod, const std::string& sem) {
        estudiante_ = est;
        codigo_ = cod;
        semestre_ = sem;
    }

    void agregarNota(const std::string& curso, double nota, int creditos) {
        notas_.push_back({curso, nota, creditos});
    }

    int totalCreditos() const {
        int tot = 0;
        for (const auto& n : notas_) tot += n.creditos;
        return tot;
    }

    double promedioPonderado() const {
        int totCr = totalCreditos();
        if (totCr == 0) return 0.0;
        double sum = 0;
        for (const auto& n : notas_) sum += (n.nota * n.creditos);
        return sum / totCr;
    }

    virtual std::string generar() const = 0;
    virtual std::string formato() const noexcept = 0;
    virtual std::string extension() const noexcept = 0;
};

// ── Productos Concretos ─────────────────────────────────
class BoletaTXT : public BoletaNotas {
public:
    std::string formato() const noexcept override { return "TXT"; }
    std::string extension() const noexcept override { return ".txt"; }
    std::string generar() const override {
        std::ostringstream oss;
        oss << "=== BOLETA DE NOTAS (TXT) ===\n";
        oss << "Estudiante: " << estudiante_ << " (" << codigo_ << ")\n";
        oss << "Semestre  : " << semestre_ << "\n";
        oss << "--------------------------------------------------\n";
        for (const auto& n : notas_) {
            oss << std::left << std::setw(30) << n.curso
                << " Cred: " << n.creditos
                << " Nota: " << std::fixed << std::setprecision(1) << n.nota << "\n";
        }
        oss << "--------------------------------------------------\n";
        oss << "Total Creditos: " << totalCreditos()
            << " | Promedio: " << std::fixed << std::setprecision(2) << promedioPonderado() << "\n";
        return oss.str();
    }
};

class BoletaCSV : public BoletaNotas {
public:
    std::string formato() const noexcept override { return "CSV"; }
    std::string extension() const noexcept override { return ".csv"; }
    std::string generar() const override {
        std::ostringstream oss;
        oss << "# Estudiante," << estudiante_ << "," << codigo_ << "," << semestre_ << "\n";
        oss << "Curso,Creditos,Nota\n";
        for (const auto& n : notas_) {
            oss << "\"" << n.curso << "\"," << n.creditos << "," << n.nota << "\n";
        }
        oss << "PROMEDIO," << totalCreditos() << "," << promedioPonderado() << "\n";
        return oss.str();
    }
};

class BoletaHTML : public BoletaNotas {
public:
    std::string formato() const noexcept override { return "HTML"; }
    std::string extension() const noexcept override { return ".html"; }
    std::string generar() const override {
        std::ostringstream oss;
        oss << "<!DOCTYPE html><html><head><title>Boleta " << estudiante_ << "</title></head><body>\n";
        oss << "<h2>Boleta de Notas - UNAP</h2>\n<p>Estudiante: " << estudiante_ << " | Semestre: " << semestre_ << "</p>\n";
        oss << "<table border='1'><tr><th>Curso</th><th>Creditos</th><th>Nota</th></tr>\n";
        for (const auto& n : notas_) {
            oss << "<tr><td>" << n.curso << "</td><td>" << n.creditos << "</td><td>" << n.nota << "</td></tr>\n";
        }
        oss << "</table>\n<p><strong>Promedio Ponderado: " << promedioPonderado() << "</strong></p>\n</body></html>";
        return oss.str();
    }
};

// ── Creador Base (Factory Method) ───────────────────────
class GeneradorBoleta {
public:
    virtual ~GeneradorBoleta() = default;
    virtual std::unique_ptr<BoletaNotas> crearBoleta() const = 0;

    void generarYEnviar(const std::string& estudiante, const std::string& codigo,
                        const std::string& semestre,
                        const std::vector<std::tuple<std::string, double, int>>& notas) const {
        auto boleta = crearBoleta();
        boleta->setDatos(estudiante, codigo, semestre);
        for (const auto& [c, n, cr] : notas) {
            boleta->agregarNota(c, n, cr);
        }
        std::string contenido = boleta->generar();
        std::cout << "[" << boleta->formato() << "] Generando boleta para " << estudiante << "...\n";
        std::cout << contenido << "\n\n";
    }
};

class GeneradorBoletaTXT : public GeneradorBoleta {
public:
    std::unique_ptr<BoletaNotas> crearBoleta() const override {
        return std::make_unique<BoletaTXT>();
    }
};

class GeneradorBoletaCSV : public GeneradorBoleta {
public:
    std::unique_ptr<BoletaNotas> crearBoleta() const override {
        return std::make_unique<BoletaCSV>();
    }
};

class GeneradorBoletaHTML : public GeneradorBoleta {
public:
    std::unique_ptr<BoletaNotas> crearBoleta() const override {
        return std::make_unique<BoletaHTML>();
    }
};

// ── Registro de Fábricas ────────────────────────────────
class RegistroGeneradoresCpp {
    using CreadorFn = std::function<std::unique_ptr<GeneradorBoleta>()>;
    std::map<std::string, CreadorFn> registro_;
public:
    void registrar(const std::string& fmt, CreadorFn fn) {
        registro_[fmt] = std::move(fn);
    }

    std::unique_ptr<GeneradorBoleta> crear(const std::string& fmt) const {
        auto it = registro_.find(fmt);
        if (it == registro_.end()) {
            throw std::invalid_argument("Formato no registrado: " + fmt);
        }
        return it->second();
    }
};

int main() {
    RegistroGeneradoresCpp reg;
    reg.registrar("txt", [] { return std::make_unique<GeneradorBoletaTXT>(); });
    reg.registrar("csv", [] { return std::make_unique<GeneradorBoletaCSV>(); });
    reg.registrar("html", [] { return std::make_unique<GeneradorBoletaHTML>(); });

    std::vector<std::tuple<std::string, double, int>> notas = {
        {"POO II", 17.5, 4},
        {"Arquitectura de Software", 16.0, 4},
        {"Bases de Datos", 15.0, 4}
    };

    for (const auto& fmt : {"txt", "csv", "html"}) {
        auto gen = reg.crear(fmt);
        gen->generarYEnviar("Maria Quispe", "20230145", "2026-II", notas);
    }

    return 0;
}

#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <numeric>
#include <stdexcept>
#include <fstream>
#include <iomanip>

// --- ENTIDAD DOMINIO ---
class Estudiante {
private:
    std::string codigo;
    std::string nombre;
    std::vector<double> notas;

public:
    Estudiante(std::string cod, std::string nom) 
        : codigo(std::move(cod)), nombre(std::move(nom)) {}

    void agregarNota(double nota) {
        if (nota < 0.0 || nota > 20.0) {
            throw std::invalid_argument("La nota " + std::to_string(nota) + " esta fuera del rango [0, 20].");
        }
        notas.push_back(nota);
    }

    [[nodiscard]] std::string getCodigo() const { return codigo; }
    [[nodiscard]] std::string getNombre() const { return nombre; }
    [[nodiscard]] const std::vector<double>& getNotas() const { return notas; }

    [[nodiscard]] double calcularPromedio() const {
        if (notas.empty()) return 0.0;
        double suma = std::accumulate(notas.begin(), notas.end(), 0.0);
        return suma / static_cast<double>(notas.size());
    }

    [[nodiscard]] bool estaAprobado() const {
        return calcularPromedio() >= 10.5;
    }
};

// --- ABSTRACCIÓN AUDITORÍA (DIP) ---
class IAuditoriaService {
public:
    virtual ~IAuditoriaService() = default;
    virtual void registrarAccion(const std::string& mensaje) = 0;
};

class AuditoriaConsola : public IAuditoriaService {
public:
    void registrarAccion(const std::string& mensaje) override {
        std::cout << "[AUDITORIA]: " << mensaje << std::endl;
    }
};

// --- REPOSITORIO ---
class RepositorioEstudiantes {
private:
    std::vector<Estudiante> estudiantes;

public:
    void guardar(const Estudiante& est) {
        estudiantes.push_back(est);
    }

    Estudiante* buscarPorCodigo(const std::string& codigo) {
        for (auto& est : estudiantes) {
            if (est.getCodigo() == codigo) return &est;
        }
        return nullptr;
    }

    [[nodiscard]] const std::vector<Estudiante>& obtenerTodos() const {
        return estudiantes;
    }
};

// --- CASO DE USO / SERVICIO ACADÉMICO ---
class ServicioAcademico {
private:
    RepositorioEstudiantes& repo;
    std::shared_ptr<IAuditoriaService> auditoria;

public:
    ServicioAcademico(RepositorioEstudiantes& r, std::shared_ptr<IAuditoriaService> aud)
        : repo(r), auditoria(std::move(aud)) {}

    void registrarEstudiante(const std::string& codigo, const std::string& nombre) {
        repo.guardar(Estudiante(codigo, nombre));
        if (auditoria) {
            auditoria->registrarAccion("Estudiante registrado: " + codigo + " - " + nombre);
        }
    }

    void agregarNotaEstudiante(const std::string& codigo, double nota) {
        Estudiante* est = repo.buscarPorCodigo(codigo);
        if (!est) {
            throw std::runtime_error("Estudiante no encontrado con codigo: " + codigo);
        }
        est->agregarNota(nota);
        if (auditoria) {
            auditoria->registrarAccion("Nota " + std::to_string(nota) + " agregada a " + codigo);
        }
    }
};

// --- GENERADOR REPORTE ---
class ReporteService {
public:
    static void generarCSV(const RepositorioEstudiantes& repo, const std::string& ruta) {
        std::ofstream archivo(ruta);
        if (!archivo.is_open()) throw std::runtime_error("No se pudo abrir el archivo de reporte.");

        archivo << "codigo,nombre,promedio,estado\n";
        for (const auto& est : repo.obtenerTodos()) {
            std::string estado = est.estaAprobado() ? "APROBADO" : "DESAPROBADO";
            archivo << est.getCodigo() << "," 
                    << est.getNombre() << "," 
                    << std::fixed << std::setprecision(2) << est.calcularPromedio() << "," 
                    << estado << "\n";
        }
    }
};

int main() {
    try {
        RepositorioEstudiantes repo;
        auto auditoria = std::make_shared<AuditoriaConsola>();
        ServicioAcademico servicio(repo, auditoria);

        servicio.registrarEstudiante("202601", "Juan Perez");
        servicio.agregarNotaEstudiante("202601", 14.5);
        servicio.agregarNotaEstudiante("202601", 18.0);

        servicio.registrarEstudiante("202602", "Maria Lopez");
        servicio.agregarNotaEstudiante("202602", 08.0);

        ReporteService::generarCSV(repo, "reporte_cpp.csv");
        std::cout << "\nProceso finalizado con exito. Reporte generado en 'reporte_cpp.csv'.\n";

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
#pragma once
#include "repositorio.hpp"
#include <string>
#include <vector>
#include <deque>
#include <iostream>
#include <iomanip>
#include <optional>
#include <numeric>
#include <algorithm>

// ============================================================================
// ENTIDADES DEL DOMINIO UNIVERSITARIO
// ============================================================================
struct Docente {
    std::string dni;
    std::string nombres;
    std::string apellidos;
    std::string categoria; // "Auxiliar", "Asociado", "Principal"
    int horas;
    double factor;

    double calcularRemuneracion() const {
        return horas * 75.0 * factor;
    }

    std::string getNombreCompleto() const {
        return apellidos + ", " + nombres;
    }
};

struct Administrativo {
    std::string dni;
    std::string nombres;
    std::string apellidos;
    std::string area;
    double salarioBase;
    double bono;

    double calcularRemuneracion() const {
        return salarioBase + bono;
    }

    std::string getNombreCompleto() const {
        return apellidos + ", " + nombres;
    }
};

// ============================================================================
// SISTEMA INTEGRADO CON REPOSITORIOS GENÉRICOS Y COLA FIFO
// ============================================================================
class SistemaGestionUNAP {
public:
    Repositorio<Docente, std::string> repoDocentes;
    Repositorio<Administrativo, std::string> repoAdministrativos;
    std::deque<std::string> colaTramites; // Cola FIFO O(1)

    SistemaGestionUNAP()
        : repoDocentes([](const Docente& d) { return d.dni; }),
          repoAdministrativos([](const Administrativo& a) { return a.dni; }) {}

    // Registro
    void registrarDocente(Docente d) {
        repoDocentes.guardar(std::move(d));
    }

    void registrarAdministrativo(Administrativo a) {
        repoAdministrativos.guardar(std::move(a));
    }

    // Flujo de atención de trámites (FIFO)
    void encolarTramite(const std::string& dni) {
        colaTramites.push_back(dni);
    }

    std::optional<std::string> atenderTramite() {
        if (colaTramites.empty()) return std::nullopt;
        std::string dni = colaTramites.front();
        colaTramites.pop_front();
        return dni;
    }

    // ── 5 CONSULTAS DE DOMINIO REQUERIDAS ────────────────────────────────────

    // Consulta 1: Docentes a tiempo completo / alta dedicación (horas >= 30)
    std::vector<Docente> docentesTiempoCompleto() const {
        return repoDocentes.filtrar([](const Docente& d) {
            return d.horas >= 30;
        });
    }

    // Consulta 2: Ranking de docentes por remuneración descendente
    std::vector<Docente> rankingDocentesPorRemuneracion() const {
        return repoDocentes.ordenar([](const Docente& a, const Docente& b) {
            return a.calcularRemuneracion() > b.calcularRemuneracion();
        });
    }

    // Consulta 3: Administrativos que perciben bono especial (bono > 0)
    std::vector<Administrativo> administrativosConBono() const {
        return repoAdministrativos.filtrar([](const Administrativo& a) {
            return a.bono > 0.0;
        });
    }

    // Consulta 4: Total acumulado de la planilla de docentes
    double calcularTotalPlanillaDocentes() const {
        return repoDocentes.acumular(0.0, [](double acc, const Docente& d) {
            return acc + d.calcularRemuneracion();
        });
    }

    // Consulta 5: Total general de la planilla institucional (Docentes + Administrativos)
    double calcularTotalPlanillaInstitucional() const {
        double totalDoc = calcularTotalPlanillaDocentes();
        double totalAdm = repoAdministrativos.acumular(0.0, [](double acc, const Administrativo& a) {
            return acc + a.calcularRemuneracion();
        });
        return totalDoc + totalAdm;
    }
};

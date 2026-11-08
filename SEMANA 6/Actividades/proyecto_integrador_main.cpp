#include "proyecto_integrador.hpp"
#include <iostream>
#include <iomanip>

int main() {
    std::cout << "===============================================================\n";
    std::cout << "ACTIVIDAD 5 (C++): PROYECTO INTEGRADOR CON REPOSITORIOS GENER.\n";
    std::cout << "===============================================================\n\n";

    SistemaGestionUNAP sistema;

    // Poblar Repositorio de Docentes (Tipo 1)
    sistema.registrarDocente({"70112233", "Carlos", "Mamani Quispe", "Principal", 40, 1.8});
    sistema.registrarDocente({"70223344", "Elena", "Flores Coila", "Asociado", 35, 1.4});
    sistema.registrarDocente({"70334455", "Ana", "Ramos Cutipa", "Auxiliar", 20, 1.0});
    sistema.registrarDocente({"70445566", "Victor", "Paredes Choque", "Auxiliar", 15, 1.0});
    sistema.registrarDocente({"70556677", "Marcos", "Condori Apaza", "Principal", 38, 1.8});

    // Poblar Repositorio de Administrativos (Tipo 2)
    sistema.registrarAdministrativo({"80112233", "Rosa", "Quispe Mamani", "Recursos Humanos", 2800.0, 450.0});
    sistema.registrarAdministrativo({"80223344", "Juan", "Calsin Ticona", "Contabilidad", 3200.0, 0.0});
    sistema.registrarAdministrativo({"80334455", "Sonia", "Chura Pari", "Secretaria General", 2500.0, 300.0});
    sistema.registrarAdministrativo({"80445566", "David", "Huanca Gomez", "Informatica", 3500.0, 600.0});

    std::cout << "Docentes en repositorio       : " << sistema.repoDocentes.tamaño() << "\n";
    std::cout << "Administrativos en repositorio: " << sistema.repoAdministrativos.tamaño() << "\n\n";

    // ── DEMOSTRACIÓN DE LAS 5 CONSULTAS DE DOMINIO ───────────────────────────
    std::cout << "---------------------------------------------------------------\n";
    std::cout << ">>> EJECUCION DE LAS 5 CONSULTAS DE DOMINIO:\n";
    std::cout << "---------------------------------------------------------------\n";

    // Consulta 1: Docentes a tiempo completo (horas >= 30)
    auto tc = sistema.docentesTiempoCompleto();
    std::cout << "\n[Consulta 1] Docentes a Tiempo Completo (Horas >= 30) [" << tc.size() << "]:\n";
    for (const auto& d : tc) {
        std::cout << "  * " << std::left << std::setw(25) << d.getNombreCompleto()
                  << " | " << d.horas << " hrs | Cat: " << std::setw(10) << d.categoria
                  << " | S/ " << std::fixed << std::setprecision(2) << d.calcularRemuneracion() << "\n";
    }

    // Consulta 2: Ranking de docentes por remuneración descendente
    auto rankDoc = sistema.rankingDocentesPorRemuneracion();
    std::cout << "\n[Consulta 2] Ranking Docentes por Remuneracion Descendente:\n";
    int rank = 1;
    for (const auto& d : rankDoc) {
        std::cout << "  " << rank++ << ". " << std::left << std::setw(25) << d.getNombreCompleto()
                  << " | DNI: " << d.dni << " | S/ " << std::fixed << std::setprecision(2)
                  << d.calcularRemuneracion() << "\n";
    }

    // Consulta 3: Administrativos con bono
    auto conBono = sistema.administrativosConBono();
    std::cout << "\n[Consulta 3] Personal Administrativo con Bono Especial [" << conBono.size() << "]:\n";
    for (const auto& a : conBono) {
        std::cout << "  * " << std::left << std::setw(25) << a.getNombreCompleto()
                  << " | Area: " << std::left << std::setw(20) << a.area
                  << " | Bono: S/ " << std::fixed << std::setprecision(2) << a.bono
                  << " | Total: S/ " << a.calcularRemuneracion() << "\n";
    }

    // Consulta 4: Total planilla docentes
    double totalDoc = sistema.calcularTotalPlanillaDocentes();
    std::cout << "\n[Consulta 4] Total Planilla Docentes (acumular): S/ " 
              << std::fixed << std::setprecision(2) << totalDoc << "\n";

    // Consulta 5: Total planilla institucional general
    double totalInst = sistema.calcularTotalPlanillaInstitucional();
    std::cout << "\n[Consulta 5] Total Planilla Institucional (Docentes + Administrativos): S/ " 
              << std::fixed << std::setprecision(2) << totalInst << "\n\n";

    // ── FLUJO DE ATENCIÓN CON COLA FIFO ──────────────────────────────────────
    std::cout << "---------------------------------------------------------------\n";
    std::cout << ">>> INTEGRACION DE FLUJO DE ATENCION DE TRAMITES (COLA FIFO):\n";
    std::cout << "---------------------------------------------------------------\n";
    sistema.encolarTramite("70112233");
    sistema.encolarTramite("80112233");
    sistema.encolarTramite("70556677");
    sistema.encolarTramite("80445566");

    std::cout << "Tramites en cola pendientes: " << sistema.colaTramites.size() << "\n";
    int turno = 1;
    while (auto dniOpt = sistema.atenderTramite()) {
        std::string dni = *dniOpt;
        std::string nombre = "Desconocido";
        if (auto doc = sistema.repoDocentes.buscar(dni)) {
            nombre = doc->getNombreCompleto() + " (Docente)";
        } else if (auto adm = sistema.repoAdministrativos.buscar(dni)) {
            nombre = adm->getNombreCompleto() + " (Administrativo)";
        }
        std::cout << "  Atendiendo Turno #" << turno++ << " -> DNI: " << dni 
                  << " | " << nombre << "\n";
    }

    std::cout << "\n===============================================================\n";
    std::cout << "FIN ACTIVIDAD 5 (C++)\n";
    std::cout << "===============================================================\n";
    return 0;
}

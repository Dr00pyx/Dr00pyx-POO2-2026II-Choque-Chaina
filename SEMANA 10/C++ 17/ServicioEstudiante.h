#pragma once

#include "Estudiante.h"
#include "IEstrategiaCalculo.h"
#include "IRepositorioEstudiante.h"
#include <vector>
#include <optional>

/**
 * @class ServicioEstudiante
 * @brief Orquestador de la lógica de aplicación para la gestión de estudiantes.
 * 
 * Cumple con:
 * - SRP: Su única responsabilidad es la coordinación del flujo de trabajo de registro
 *        y consulta de estudiantes.
 * - DIP: No depende de implementaciones concretas (como RepositorioMemoria o PromedioSimple),
 *        sino de las abstracciones IRepositorioEstudiante e IEstrategiaCalculo recibidas
 *        mediante Inyección de Dependencias por constructor.
 * - OCP: Permite incorporar nuevas estrategias de cálculo o nuevos mecanismos de persistencia
 *        sin modificar una sola línea de esta clase.
 */
class ServicioEstudiante {
public:
    ServicioEstudiante(IRepositorioEstudiante& repo, IEstrategiaCalculo& calc)
        : repo_(repo), calc_(calc) {}

    void registrar(Estudiante e, const std::vector<float>& notas) {
        float ppaCalculado = calc_.calcular(notas);
        e.set_ppa(ppaCalculado);
        repo_.guardar(e);
    }

    [[nodiscard]] std::optional<Estudiante> buscar(int codigo) const {
        return repo_.buscar(codigo);
    }

    [[nodiscard]] std::vector<Estudiante> listar() const {
        return repo_.listar();
    }

private:
    IRepositorioEstudiante& repo_;
    IEstrategiaCalculo& calc_;
};

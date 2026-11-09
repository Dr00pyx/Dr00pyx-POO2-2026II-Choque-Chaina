#pragma once

#include "Estudiante.h"
#include "IRepositorioEstudiante.h"
#include "Logger.h"
#include <algorithm>
#include <iostream>
#include <vector>

/**
 * @struct IObserverEstudiante
 * @brief Interfaz para los observadores interesados en eventos del Estudiante.
 */
struct IObserverEstudiante {
    virtual void on_guardado(const Estudiante& e) = 0;
    virtual ~IObserverEstudiante() = default;
};

/**
 * @struct LoggerObserver
 * @brief Observador concreto que registra auditorías a través del Singleton Logger.
 */
struct LoggerObserver : public IObserverEstudiante {
    void on_guardado(const Estudiante& e) override {
        Logger::getInstance().log(
            "Guardado: [" + std::to_string(e.codigo()) + "] " + e.nombre());
    }
};

/**
 * @struct ConsolaObserver
 * @brief Observador concreto que actúa como Vista renderizando el estudiante en terminal.
 */
struct ConsolaObserver : public IObserverEstudiante {
    void on_guardado(const Estudiante& e) override {
        std::cout << ">> Vista: " << e.to_string() << std::endl;
    }
};

/**
 * @struct EmailObserver
 * @brief ADICIONAL Actividad 1A: Notificador de correo electrónico.
 */
struct EmailObserver : public IObserverEstudiante {
    void on_guardado(const Estudiante& e) override {
        std::cout << "Enviando correo a " << e.nombre() << std::endl;
    }
};

/**
 * @class RepositorioObservable
 * @brief Sujeto Observable (Subject) que notifica a los suscriptores al guardar.
 */
class RepositorioObservable : public IRepositorioEstudiante {
public:
    explicit RepositorioObservable(IRepositorioEstudiante& r) : repo_(r) {}

    void suscribir(IObserverEstudiante* o) {
        if (std::find(obs_.begin(), obs_.end(), o) == obs_.end()) {
            obs_.push_back(o);
        }
    }

    void desuscribir(IObserverEstudiante* o) {
        auto it = std::find(obs_.begin(), obs_.end(), o);
        if (it != obs_.end()) {
            obs_.erase(it);
        }
    }

    [[nodiscard]] const std::vector<IObserverEstudiante*>& observadores() const {
        return obs_;
    }

    void guardar(const Estudiante& e) override {
        repo_.guardar(e);
        for (auto* o : obs_) {
            if (o != nullptr) {
                o->on_guardado(e);
            }
        }
    }

    std::optional<Estudiante> buscar(int cod) override {
        return repo_.buscar(cod);
    }

    [[nodiscard]] std::vector<Estudiante> listar() const override {
        return repo_.listar();
    }

private:
    IRepositorioEstudiante& repo_;
    std::vector<IObserverEstudiante*> obs_;
};

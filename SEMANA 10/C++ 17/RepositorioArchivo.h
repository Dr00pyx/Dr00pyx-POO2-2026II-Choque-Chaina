#pragma once

#include "IRepositorioEstudiante.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <unordered_map>
#include <vector>

/**
 * @class RepositorioArchivo
 * @brief Implementación de IRepositorioEstudiante basada en almacenamiento persistente CSV
 *        utilizando std::ofstream y std::ifstream.
 * 
 * Cumple con el requisito de Actividad 1A (ADICIONAL) y Actividad 3A (RepositorioCsv).
 * Mantiene la persistencia en disco asegurando que el contrato de IRepositorioEstudiante
 * se cumpla fielmente.
 */
class RepositorioArchivo : public IRepositorioEstudiante {
public:
    explicit RepositorioArchivo(std::string rutaArchivo = "estudiantes.csv")
        : rutaArchivo_(std::move(rutaArchivo)) {
        cargarDesdeArchivo();
    }

    void guardar(const Estudiante& e) override {
        cache_[e.codigo()] = e;
        persistirEnArchivo();
    }

    std::optional<Estudiante> buscar(int codigo) const override {
        auto it = cache_.find(codigo);
        if (it != cache_.end()) {
            return it->second;
        }
        return std::nullopt;
    }

    std::vector<Estudiante> listar() const override {
        std::vector<Estudiante> lista;
        lista.reserve(cache_.size());
        for (const auto& [cod, est] : cache_) {
            lista.push_back(est);
        }
        return lista;
    }

    const std::string& ruta() const { return rutaArchivo_; }

private:
    std::string rutaArchivo_;
    std::unordered_map<int, Estudiante> cache_;

    void cargarDesdeArchivo() {
        std::ifstream file(rutaArchivo_);
        if (!file.is_open()) return;

        std::string linea;
        bool primeraLinea = true;
        while (std::getline(file, linea)) {
            if (linea.empty()) continue;
            // Omitir cabecera si existe
            if (primeraLinea && linea.find("codigo") != std::string::npos) {
                primeraLinea = false;
                continue;
            }
            std::stringstream ss(linea);
            std::string codStr, nombre, ppaStr;
            if (std::getline(ss, codStr, ',') &&
                std::getline(ss, nombre, ',') &&
                std::getline(ss, ppaStr, ',')) {
                try {
                    int cod = std::stoi(codStr);
                    float ppa = std::stof(ppaStr);
                    cache_[cod] = Estudiante(cod, nombre, ppa);
                } catch (...) {
                    // Ignorar líneas no parseables
                }
            }
        }
    }

    void persistirEnArchivo() const {
        std::ofstream file(rutaArchivo_, std::ios::trunc);
        if (!file.is_open()) {
            std::cerr << "Error: No se pudo abrir el archivo para escritura: " << rutaArchivo_ << std::endl;
            return;
        }
        file << "codigo,nombre,ppa\n";
        for (const auto& [cod, est] : cache_) {
            file << est.codigo() << "," << est.nombre() << "," << est.ppa() << "\n";
        }
    }
};

// Alias para coincidir con la nomenclatura del diagrama de clases PlantUML
using RepositorioCsv = RepositorioArchivo;

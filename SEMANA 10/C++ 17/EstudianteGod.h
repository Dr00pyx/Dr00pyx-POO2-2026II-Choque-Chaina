// EstudianteGod.h — VIOLACIÓN de SRP — NO copiar como solución
// Archivo de referencia para análisis de malas prácticas de diseño
#pragma once

#include <string>
#include <vector>
#include <fstream>
#include <iostream>

/**
 * @class EstudianteGod
 * @brief Ejemplo de clase "God Object" que viola flagrantemente el
 *        Principio de Responsabilidad Única (SRP - Single Responsibility Principle).
 * 
 * Posee múltiples responsabilidades y más de 4 razones para cambiar:
 * 1. Lógica de dominio y estructura de datos del estudiante.
 * 2. Lógica de negocio / cálculo estadístico (cálculo del PPA).
 * 3. Persistencia de datos en disco (formato CSV/texto plano).
 * 4. Serialización y representación externa (formato JSON).
 * 5. Infraestructura de comunicación y notificaciones (envío de correos).
 */
class EstudianteGod {
public:
    int codigo;
    std::string nombre;
    float ppa;
    std::vector<float> notas;

    // =========================================================================
    // Responsabilidad 1: Cálculo de métricas académicas (Lógica de Negocio)
    // Razón de cambio: Si se modifica la fórmula de ponderación, redondeo o
    //                  se decide descartar notas mínimas/máximas.
    // =========================================================================
    float calcularPPA() {
        if (notas.empty()) return 0.0f;
        float s = 0.0f;
        for (auto n : notas) s += n;
        return s / notas.size();
    }

    // =========================================================================
    // Responsabilidad 2: Persistencia física de datos (Acceso a Datos)
    // Razón de cambio: Si cambia la estructura del archivo, delimitador,
    //                  o se migra a SQLite, PostgreSQL o almacenamiento remoto.
    // =========================================================================
    void guardarEnArchivo(const std::string& ruta) {
        std::ofstream f(ruta);
        f << codigo << "," << nombre << "," << ppa << std::endl;
    }

    // =========================================================================
    // Responsabilidad 3: Serialización de datos (Capa de Presentación / API)
    // Razón de cambio: Si cambia el esquema JSON, se añaden atributos
    //                  o se adopta otro formato (XML, YAML, Protocol Buffers).
    // =========================================================================
    std::string toJson() {
        return "{\"codigo\":" + std::to_string(codigo) + 
               ",\"nombre\":\"" + nombre + "\"" +
               ",\"ppa\":" + std::to_string(ppa) + "}";
    }

    // =========================================================================
    // Responsabilidad 4: Notificaciones y comunicación (Servicio Externo)
    // Razón de cambio: Si cambia el protocolo SMTP, servidor de correo,
    //                  plantilla del mensaje o se envía por SMS o Push.
    // =========================================================================
    void enviarCorreo(const std::string& dest) {
        std::cout << "[EstudianteGod] Enviando correo a " << dest 
                  << " con la información de " << nombre << std::endl;
    }
};

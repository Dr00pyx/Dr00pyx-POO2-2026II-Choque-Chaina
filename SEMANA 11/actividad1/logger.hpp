#ifndef LOGGER_HPP
#define LOGGER_HPP

#include <iostream>
#include <fstream>
#include <string>
#include <mutex>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <stdexcept>

enum class NivelLog {
    DEBUG,
    INFO,
    WARN,
    ERROR
};

/**
 * @brief Singleton Meyers para registro de logs centralizado y thread-safe.
 * Cumple con el estándar C++17 asegurando inicialización única y segura.
 */
class Logger {
private:
    std::ofstream archivo_;
    std::mutex mtx_;
    NivelLog nivelMinimo_;

    // Constructor privado: previene instanciación externa
    explicit Logger(const std::string& ruta = "app.log", NivelLog nivel = NivelLog::DEBUG)
        : nivelMinimo_(nivel) {
        archivo_.open(ruta, std::ios::out | std::ios::app);
        if (!archivo_.is_open()) {
            // Intento adicional con creación simple si falló
            archivo_.clear();
            archivo_.open(ruta);
            if (!archivo_.is_open()) {
                throw std::runtime_error("Error: No se pudo abrir el archivo de log: " + ruta);
            }
        }
    }

    // Destructor privado/protegido o estándar
    ~Logger() {
        if (archivo_.is_open()) {
            archivo_.flush();
            archivo_.close();
        }
    }

    // Eliminación de constructores de copia y asignación para garantizar unicidad
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;
    Logger(Logger&&) = delete;
    Logger& operator=(Logger&&) = delete;

    std::string timestamp() const {
        auto now = std::chrono::system_clock::now();
        auto t = std::chrono::system_clock::to_time_t(now);
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;
        
        std::ostringstream oss;
        oss << std::put_time(std::localtime(&t), "%Y-%m-%d %H:%M:%S")
            << '.' << std::setfill('0') << std::setw(3) << ms.count();
        return oss.str();
    }

    static std::string nivelStr(NivelLog n) {
        switch (n) {
            case NivelLog::DEBUG: return "DEBUG";
            case NivelLog::INFO:  return "INFO ";
            case NivelLog::WARN:  return "WARN ";
            case NivelLog::ERROR: return "ERROR";
        }
        return "UNKNOWN";
    }

public:
    /**
     * @brief Punto de acceso global único (Singleton Meyers).
     * Desde C++11, la inicialización de variables locales estáticas es thread-safe por especificación.
     */
    static Logger& instancia(const std::string& ruta = "app.log") {
        static Logger inst(ruta);
        return inst;
    }

    void setNivelMinimo(NivelLog nivel) {
        std::lock_guard<std::mutex> lock(mtx_);
        nivelMinimo_ = nivel;
    }

    void log(NivelLog nivel, const std::string& modulo, const std::string& mensaje) {
        if (nivel < nivelMinimo_) return;

        std::lock_guard<std::mutex> lock(mtx_);
        std::string entrada = "[" + timestamp() + "] [" + nivelStr(nivel) + "] [" + modulo + "] " + mensaje;
        
        if (archivo_.is_open()) {
            archivo_ << entrada << "\n";
            archivo_.flush();
        }
        std::cout << entrada << "\n";
    }

    void debug(const std::string& mod, const std::string& msg) { log(NivelLog::DEBUG, mod, msg); }
    void info (const std::string& mod, const std::string& msg) { log(NivelLog::INFO,  mod, msg); }
    void warn (const std::string& mod, const std::string& msg) { log(NivelLog::WARN,  mod, msg); }
    void error(const std::string& mod, const std::string& msg) { log(NivelLog::ERROR, mod, msg); }
};

#endif // LOGGER_HPP

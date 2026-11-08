#ifndef CONEXION_MEJORADA_HPP
#define CONEXION_MEJORADA_HPP

#include <iostream>
#include <string>
#include <memory>
#include <mutex>
#include <vector>

// ── 1. Abstracción del Logger (DIP) ─────────────────────
class ILogger {
public:
    virtual ~ILogger() = default;
    virtual void info(const std::string& modulo, const std::string& mensaje) = 0;
};

class LoggerConsola : public ILogger {
    std::mutex mtx_;
public:
    void info(const std::string& modulo, const std::string& mensaje) override {
        std::lock_guard<std::mutex> lock(mtx_);
        std::cout << "[LOG][" << modulo << "] " << mensaje << "\n";
    }
};

// ── 2. Abstracción de la Conexión a BD (DIP + OCP) ───────
class IConexionBD {
public:
    virtual ~IConexionBD() = default;
    virtual void ejecutar(const std::string& sql) = 0;
    virtual const std::string& getUrl() const noexcept = 0;
};

// ── 3. Implementación Concreta Desacoplada (Inyección DIP)
class ConexionSQLite : public IConexionBD {
private:
    std::string url_;
    std::shared_ptr<ILogger> logger_;
    std::mutex mtx_;

public:
    ConexionSQLite(std::string url, std::shared_ptr<ILogger> logger)
        : url_(std::move(url)), logger_(std::move(logger)) {}

    void ejecutar(const std::string& sql) override {
        std::lock_guard<std::mutex> lock(mtx_);
        if (logger_) {
            logger_->info("BD-SQLite", "Ejecutando consulta: " + sql);
        }
        std::cout << "-> SQLite (" << url_ << ") ejecutó: " << sql << std::endl;
    }

    const std::string& getUrl() const noexcept override {
        return url_;
    }
};

// ── 4. Singleton Thread-Safe Idiomático (Meyers Singleton)
// Cuando se requiere un punto de acceso único sin comprometer DIP
class GestorConexionSingleton {
private:
    std::shared_ptr<IConexionBD> conexion_;

    explicit GestorConexionSingleton(std::shared_ptr<IConexionBD> conexion)
        : conexion_(std::move(conexion)) {}

    // Prevenir copia y movimiento
    GestorConexionSingleton(const GestorConexionSingleton&) = delete;
    GestorConexionSingleton& operator=(const GestorConexionSingleton&) = delete;
    GestorConexionSingleton(GestorConexionSingleton&&) = delete;
    GestorConexionSingleton& operator=(GestorConexionSingleton&&) = delete;

public:
    static GestorConexionSingleton& instancia(std::shared_ptr<IConexionBD> conexionInicial = nullptr) {
        static GestorConexionSingleton inst(
            conexionInicial ? conexionInicial
                            : std::make_shared<ConexionSQLite>("sqlite:///datos_default.db",
                                                               std::make_shared<LoggerConsola>())
        );
        return inst;
    }

    std::shared_ptr<IConexionBD> conexion() const {
        return conexion_;
    }
};

#endif // CONEXION_MEJORADA_HPP

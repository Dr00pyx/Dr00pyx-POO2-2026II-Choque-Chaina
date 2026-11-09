#pragma once

#include <chrono>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <mutex>
#include <sstream>
#include <string>
#include <vector>

/**
 * @class Logger
 * @brief Singleton thread-safe (Meyers Singleton) para auditoría centralizada.
 */
class Logger {
public:
    static Logger& getInstance() {
        static Logger instancia;
        return instancia;
    }

    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    std::string log(const std::string& mensaje) {
        std::lock_guard<std::mutex> lock(mutex_);

        auto ahora = std::chrono::system_clock::now();
        std::time_t tiempo_t = std::chrono::system_clock::to_time_t(ahora);
        std::tm tm_local{};
#if defined(_WIN32) || defined(_WIN64)
        localtime_s(&tm_local, &tiempo_t);
#else
        localtime_r(&tiempo_t, &tm_local);
#endif

        std::ostringstream oss;
        oss << "[LOG] "
            << std::setfill('0') << std::setw(2) << tm_local.tm_hour << ":"
            << std::setfill('0') << std::setw(2) << tm_local.tm_min << ":"
            << std::setfill('0') << std::setw(2) << tm_local.tm_sec << " "
            << mensaje;

        std::string linea = oss.str();
        entradas_.push_back(linea);
        std::cout << linea << std::endl;
        return linea;
    }

    [[nodiscard]] std::vector<std::string> get_entradas() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return entradas_;
    }

    void limpiar() {
        std::lock_guard<std::mutex> lock(mutex_);
        entradas_.clear();
    }

private:
    Logger() = default;
    mutable std::mutex mutex_;
    std::vector<std::string> entradas_;
};

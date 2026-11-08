#include <vector>
#include <unordered_map>
#include <chrono>
#include <iostream>
#include <numeric>
#include <algorithm>
#include <iomanip>

using Clock = std::chrono::high_resolution_clock;
using Ms = std::chrono::duration<double, std::milli>;

struct BenchResultCpp {
    int n;
    double vec_ms;
    double map_ms;
};

BenchResultCpp benchmarkBusqueda(int n, int repeticiones) {
    std::vector<int> vec(n);
    std::iota(vec.begin(), vec.end(), 0);

    std::unordered_map<int, int> umap;
    umap.reserve(n);
    for (int i = 0; i < n; ++i) umap[i] = i;

    int buscar = n / 2; // Buscar elemento del medio

    // ── Benchmark vector (búsqueda lineal O(n)) ─────────────────────────
    auto t0 = Clock::now();
    volatile int sink = 0;
    for (int r = 0; r < repeticiones; ++r) {
        auto it = std::find(vec.begin(), vec.end(), buscar);
        sink += *it;
    }
    auto t1 = Clock::now();
    double vec_ms = std::chrono::duration_cast<Ms>(t1 - t0).count();

    // ── Benchmark unordered_map (hash O(1)) ─────────────────────────────
    auto t2 = Clock::now();
    for (int r = 0; r < repeticiones; ++r) {
        auto it = umap.find(buscar);
        sink += it->second;
    }
    auto t3 = Clock::now();
    double map_ms = std::chrono::duration_cast<Ms>(t3 - t2).count();

    (void)sink;
    return {n, vec_ms, map_ms};
}

int main() {
    std::cout << "===============================================================\n";
    std::cout << "BENCHMARK C++17: std::vector vs std::unordered_map\n";
    std::cout << "===============================================================\n";
    std::cout << std::setw(12) << "N" 
              << std::setw(20) << "vector (ms)" 
              << std::setw(24) << "unordered_map (ms)" << "\n";
    std::cout << "---------------------------------------------------------------\n";

    // 10 000 repeticiones para n <= 100 000; para 1 000 000 escalamos o medimos
    int valores_n[] = {1000, 10000, 100000, 1000000};
    for (int n : valores_n) {
        // Para n=1_000_000, 10 000 repeticiones de búsqueda lineal harían 5 mil millones de comparaciones.
        // Hacemos 1000 repeticiones y normalizamos a 10000 para que termine en ~1 segundo con precisión.
        int reps = (n >= 1000000) ? 1000 : 10000;
        double factor = (n >= 1000000) ? 10.0 : 1.0;

        auto res = benchmarkBusqueda(n, reps);
        double v_total = res.vec_ms * factor;
        double m_total = res.map_ms * factor;

        std::cout << std::setw(12) << n 
                  << std::setw(20) << std::fixed << std::setprecision(3) << v_total 
                  << std::setw(24) << std::fixed << std::setprecision(3) << m_total << "\n";
    }
    std::cout << "===============================================================\n";
    return 0;
}

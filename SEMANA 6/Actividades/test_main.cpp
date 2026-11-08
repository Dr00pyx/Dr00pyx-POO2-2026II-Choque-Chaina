#include "repositorio.hpp"
#include <iostream>
#include <cassert>
#include <string>

struct ItemTest {
    int id;
    std::string nombre;
    int valor;
};

int main() {
    std::cout << "[TEST C++] Iniciando suite de pruebas unitarias para Repositorio<T, ID>...\n";

    Repositorio<ItemTest, int> repo([](const ItemTest& it) { return it.id; });

    // Test vacio() y tamaño()
    assert(repo.vacio());
    assert(repo.tamaño() == 0);

    // Test guardar() y tamaño()
    repo.guardar({1, "A", 100});
    repo.guardar({2, "B", 200});
    repo.guardar({3, "C", 300});
    assert(!repo.vacio());
    assert(repo.tamaño() == 3);

    // Test existe()
    assert(repo.existe(1));
    assert(repo.existe(2));
    assert(!repo.existe(99));

    // Test buscar()
    auto res1 = repo.buscar(1);
    assert(res1.has_value());
    assert(res1->nombre == "A");
    assert(res1->valor == 100);

    auto res99 = repo.buscar(99);
    assert(!res99.has_value());

    // Test contar()
    size_t mayores150 = repo.contar([](const ItemTest& it) { return it.valor > 150; });
    assert(mayores150 == 2);

    // Test primero()
    auto primerMayor = repo.primero([](const ItemTest& it) { return it.valor >= 200; });
    assert(primerMayor.has_value());
    assert(primerMayor->valor >= 200);

    // Test filtrar()
    auto filtrados = repo.filtrar([](const ItemTest& it) { return it.valor > 100; });
    assert(filtrados.size() == 2);

    // Test acumular()
    int suma = repo.acumular(0, [](int acc, const ItemTest& it) { return acc + it.valor; });
    assert(suma == 600);

    // Test ordenar()
    auto ordenadosDesc = repo.ordenar([](const ItemTest& a, const ItemTest& b) {
        return a.valor > b.valor;
    });
    assert(ordenadosDesc.size() == 3);
    assert(ordenadosDesc[0].valor == 300);
    assert(ordenadosDesc[1].valor == 200);
    assert(ordenadosDesc[2].valor == 100);

    // Test eliminar()
    assert(repo.eliminar(2));
    assert(!repo.existe(2));
    assert(repo.tamaño() == 2);
    assert(!repo.eliminar(2)); // Segundo intento retorna false

    std::cout << "[TEST C++] TODOS LOS TESTS PASARON EXITOSAMENTE (100% OK).\n";
    return 0;
}

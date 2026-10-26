#include "notificador.hpp"
#include <iostream>
#include <memory>

int main() {
    SistemaAlertas sistema;
    sistema.agregar(std::make_unique<NotificadorEmail>("smtp.unap.edu.pe"));
    sistema.agregar(std::make_unique<NotificadorSMS>("Movistar"));

    int n = sistema.alertar(
        "jmamani@unap.edu.pe",
        "ALERTA: Temperatura Titicaca supera 18 grados"
    );

    std::cout << "Alerta enviada por " << n << " canal(es).\n";
    return 0;
}
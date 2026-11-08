# Pregunta 4: Singleton y el Principio de Inversión de Dependencias (DIP)

### ¿Por qué Singleton viola DIP?
El patrón Singleton clásico viola el Principio de Inversión de Dependencias (DIP) porque los módulos de alto nivel se acoplan directamente a una clase concreta mediante llamadas estáticas globales (por ejemplo `Logger::instancia()` o `ConfiguracionApp()`), dependiendo de un detalle de bajo nivel en lugar de una abstracción (interfaz), lo que además impide el aislamiento en pruebas unitarias al no permitir inyectar dobles de prueba (mocks/stubs).

### ¿Cómo mitigarlo con Inyección de Dependencias (DIP)?
Se mitiga definiendo una interfaz abstracta (`ILogger` o `IConfiguracion`) de la cual dependan las clases de negocio a través de inyección por constructor; de este modo, el contenedor de dependencias (IoC Container) o el inicializador del sistema resuelve y entrega una única instancia (tiempo de vida *Singleton* administrado por el contenedor), preservando la unicidad del recurso sin generar acoplamiento a clases concretas ni llamadas globales estáticas.

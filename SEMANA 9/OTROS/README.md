# SIS206 — Programación Orientada a Objetos II
## GUÍA DE PRÁCTICA AVANZADA — SEMANA 09
### Inicio Unidad II: Arquitectura del Sistema Académico UNAP
**Docente:** Dr. Aldo Hernán Zanabria Gálvez  
**Carpeta del Proyecto:** `SEMANA 9`

---

## 📁 Estructura del Proyecto

```text
SEMANA 9/
├── README.md                               # Guía explicativa y resumen de la práctica
├── verificacion_entorno_apellido.txt       # Reporte Actividad 1A con salidas de terminal
├── verificacion_entorno_reporte.txt        # Copia de respaldo del reporte de entorno
├── s09_arquitectura_apellido.png           # Diagrama PNG renderizado (Actividad 3A)
├── ACTIVIDAD_4_REFLEXION.md                # Respuestas profundas y matriz comparativa (Act. 4)
├── actividad_4_reflexion.txt               # Versión texto plano de las reflexiones
│
├── s09/
│   ├── cpp/                                # Actividad 2A: Implementación en C++17
│   │   ├── estudiante.h                    # Clase Estudiante (invariantes + es_aprobado)
│   │   ├── main.cpp                        # Pruebas de consola, verificación y casos límite
│   │   ├── main.exe                        # Binario compilado con g++ -std=c++17
│   │   └── salida_cpp.txt                  # Log verificado de la ejecución en consola
│   │
│   ├── python/                             # Actividad 2B: Implementación en Python 3.12+
│   │   ├── estudiante.py                   # Clase Estudiante (@dataclass + asserts + JSON)
│   │   ├── test_estudiante.py              # Suite de pruebas unitarias automatizadas (pytest)
│   │   └── salida_python.txt               # Log verificado de la ejecución en consola
│   │
│   └── plantuml/                           # Actividad 3 y 3A: Diagrama de Arquitectura
│       ├── s09_arquitectura.puml           # Código fuente PlantUML con extensión Observer
│       ├── s09_arquitectura_ChoqueChaiña.png   # Imagen exportada en alta resolución
│       ├── s09_arquitectura_diagrama.svg   # Imagen en formato vectorial SVG
│       ├── enlaces_plantuml_online.txt     # Enlace directo web a plantuml.com
│       ├── generate_plantuml_artifacts.py  # Script de compresión y generación de URLs
│       ├── generate_svg.py                 # Generador del diagrama vectorial SVG
│       └── render_diagram.ps1              # Generador GDI+ del PNG
```

---

## 🚀 Resumen de Cumplimiento de Actividades

### 1. Actividad 1 & 1A — Verificación del Entorno de Desarrollo
- **C++17:** Compilador `g++.exe 15.2.0` (MSYS2 UCRT64). Verificación ejecutada con `test17.cpp` empleando `std::optional` y `std::string_view` con salida exitosa `C++17 OK: UNAP`.
- **Python 3.12+:** Intérprete `Python 3.14.8` y framework `pytest 9.1.1` verificados y operativos. Documentación de paquetes de Unidad II (`SQLAlchemy`, `Alembic`, `PyQt5`).
- **PlantUML / Java:** Configuración analizada y complementada mediante el editor en línea oficial `plantuml.com` y renderizado automatizado nativo a PNG y SVG.
- **Entregable:** Archivo [`verificacion_entorno_apellido.txt`](./verificacion_entorno_apellido.txt).

---

### 2. Actividad 2A — Clase Estudiante en C++17
- Ubicación: `s09/cpp/`
- **Archivos:** [`estudiante.h`](./s09/cpp/estudiante.h) y [`main.cpp`](./s09/cpp/main.cpp).
- **Validaciones e invariantes:** Código positivo (`codigo > 0`), nombre no vacío, PPA en rango `[0.0, 20.0]` y notas en rango `[0.0, 20.0]`.
- **Funcionalidades requeridas:**
  - `to_string()`, `calcular_promedio()` retornando `std::optional<float>`.
  - Prueba de adición de nota `20.0` verificando cambio de promedio (de `16` a `17`).
  - **ADICIONAL implementado:** Método `es_aprobado() -> bool` evaluando `PPA >= 11.0f`.
- **Compilación y ejecución:**
  ```powershell
  cd "s09/cpp"
  g++ -std=c++17 main.cpp -o main.exe
  ./main.exe
  ```
- **Salida:** Registrada en [`salida_cpp.txt`](./s09/cpp/salida_cpp.txt).

---

### 3. Actividad 2B — Clase Estudiante en Python 3.12+
- Ubicación: `s09/python/`
- **Archivos:** [`estudiante.py`](./s09/python/estudiante.py) y [`test_estudiante.py`](./s09/python/test_estudiante.py).
- **Funcionalidades requeridas:**
  - `@dataclass` con validación en `__post_init__`.
  - Inclusión de 5 notas distintas mostrando el promedio formateado a 2 decimales (`:.2f`).
  - 3 casos de prueba con `assert` verificando que código <= 0, nombre vacío y PPA inválido lancen `ValueError`.
  - **ADICIONAL implementado:** Serialización a formato JSON mediante `json.dumps(dataclasses.asdict(e))` y método `es_aprobado()`.
- **Ejecución y pruebas:**
  ```powershell
  cd "s09/python"
  python estudiante.py
  python -m pytest test_estudiante.py -v
  ```
- **Salida:** Registrada en [`salida_python.txt`](./s09/python/salida_python.txt).

---

### 4. Actividad 3 & 3A — Diagrama de Arquitectura con PlantUML
- Ubicación: `s09/plantuml/`
- **Código fuente:** [`s09_arquitectura.puml`](./s09/plantuml/s09_arquitectura.puml).
- **Extensión requerida (Actividad 3A):**
  - Componente `[NotificadorEmail]` incorporado en la Capa de Servicios.
  - Flecha de relación añadida: `SVC --> NotificadorEmail : Observer (S12)`.
- **Enlace PlantUML Web Editor:** [Abrir diagrama en plantuml.com](https://www.plantuml.com/plantuml/uml/TLFHRjem57ttLrpHbw4A1WoOXgQgQGWeKu1GGr_6DBcEeLOJcpbEDRHDsaVi9_RSJ-1FzYNJJPgD1lgMS-znVEwvnvUfPSPcIGnKfbOapE4i4edaUZbrmi-qzOvOQMDHjW7x-zz806J0dv-_m35VCca5jvbXi5GoOX7uFY5Rnk_PHa3DPLi6aO3GY5GeoxZSFweQd0txNdVKWcy4WEjagvLG5ZwEbxwNsYoIJ5dn2LWAuwL_H74pa-gocmC2eBGLOEJcpe9UOmC6iBYNoWe3hsYxMr-fS3UtlGAG7oSqKc4U99SwXTSGx1ytahCQd7aTRpHqgafBRaKklN5FyoRC6icpc9MqoNEUosBiHjg4ePDpN2Ue_6kghLnBZYGlOJBEQTKY0SY7NZCk0Dqqp8gDPCK56e_u7bqSEKPlN1W0dGN-42rgrLTgh4VusMxGTkUqOw4mAQP3SObMZLolE-pdLXrek1PRdKghpQ5RgEFQ2sVF9poWVg2pQJuWVhp8elD0bjRF0t_XlSmiNANEqUGe0mOmzCDoy7_7TbXvKryfEW-ScD-99A_qAcwSdxVVmaHRRJ0lph0zwbNp4ijRNcoW-PJTmBywaXBuLp00yTKAey35g_hrbU9sjnLfWV1Y37UZSP67hNm1PM52S948SdTBa8Uf1DN8m01cjwam3yLJwTG9qg5vKIGb1tYkK5Ue8RbhxxytcyM2_iEdFHmK748kXOgo92P_0G00)
- **Imagen generada:** [`s09_arquitectura_apellido.png`](./s09_arquitectura_apellido.png).

---

### 5. Actividad 4 — Reflexión: El Hilo Conductor
- Respuestas académicas rigurosas y detalladas a las 5 preguntas que articulan la Unidad II (S10–S18), abarcando:
  1. Principio de Responsabilidad Única (SRP) en la entidad `Estudiante`.
  2. Aislamiento de capas entre la GUI y la Base de Datos.
  3. Principio de Inversión de Dependencias (DIP) y Patrón Repositorio (`IRepositorioEstudiante`).
  4. Interoperabilidad de alto rendimiento entre C++17 y Python mediante `ctypes`.
  5. Prevención de rotura de contratos de API mediante pruebas automatizadas con `pytest`.
- **Entregables:** Documento formateado [`ACTIVIDAD_4_REFLEXION.md`](./ACTIVIDAD_4_REFLEXION.md) y [`actividad_4_reflexion.txt`](./actividad_4_reflexion.txt).

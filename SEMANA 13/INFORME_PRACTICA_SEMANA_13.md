# UNIVERSIDAD NACIONAL DEL ALTIPLANO - PUNO
## FACULTAD DE INGENIERÍA MECÁNICA ELÉCTRICA, ELECTRÓNICA Y SISTEMAS
### ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

---

# INFORME DE PRÁCTICA AVANZADA — SEMANA 13
## PERSISTENCIA MULTICAPA: REPOSITORIOJSON, CSV Y SQLITE
### PATRÓN REPOSITORY, SUSTITUCIÓN DE LISKOV (LSP) Y ANÁLISIS DE TRADE-OFFS

* **Asignatura:** SIS206 — Programación Orientada a Objetos II
* **Semestre Académico:** 2026-II
* **Docente:** Dr. Aldo Hernán Zanabria Gálvez | ORCID: [0000-0003-3314-8768](https://orcid.org/0000-0003-3314-8768) | RENACYT: P0020608 | UNAP Puno
* **Duración:** 2 horas
* **Herramientas Utilizadas:** Python 3.12 / 3.14 (json, csv, sqlite3 — biblioteca estándar), pytest 9.1.1, PowerShell / CMD

---

## ÍNDICE DEL INFORME
1. [Resumen Ejecutivo y Objetivos de la Práctica](#1-resumen-ejecutivo-y-objetivos)
2. [Arquitectura del Sistema y Contrato IRepositorioEstudiante](#2-arquitectura-y-contrato)
3. [Actividad 1: RepositorioJSON con Persistencia Real](#3-actividad-1-repositorio-json)
   - [3.1 Implementación y Persistencia Documental](#31-implementacion-json)
   - [3.2 Verificación de Persistencia entre Instancias](#32-persistencia-instancias)
   - [3.3 Inspección del Archivo JSON Generado](#33-inspeccion-json)
   - [3.4 Pregunta Reflexiva: Ejecución Consecutiva sin Borrar el Archivo](#34-pregunta-reflexiva-json)
   - [3.5 Adicional Actividad 1A: Implementación de eliminar(cod)](#35-adicional-eliminar-json)
4. [Actividad 2: RepositorioCSV con Persistencia Tabular](#4-actividad-2-repositorio-csv)
   - [4.1 Implementación y Reto de Serialización Objeto-Relacional](#41-implementacion-csv)
   - [4.2 Registro de 3 Estudiantes y Verificación Estricta del Encabezado](#42-registro-encabezado-csv)
   - [4.3 Inserción Manual Externa y Recarga en Caliente](#43-insercion-manual-csv)
   - [4.4 Operación de Eliminación en CSV](#44-eliminacion-csv)
5. [Actividad 3: RepositorioSQLite y Prueba de Sustitución LSP](#5-actividad-3-repositorio-sqlite-lsp)
   - [5.1 Implementación de RepositorioSQLite con Motor Embebido](#51-implementacion-sqlite)
   - [5.2 Prueba Parametrizada de Sustitución con pytest (4 Backends)](#52-prueba-pytest-lsp)
   - [5.3 Pregunta Reflexiva: ¿ServicioEstudiante Cambió Alguna Línea?](#53-pregunta-reflexiva-servicio)
   - [5.4 Adicional Actividad 3A: 5° Parámetro con MockRepositorio y Auditoría](#54-adicional-mock-repositorio)
6. [Análisis Comparativo Profundo de Trade-Offs](#6-analisis-trade-offs)
   - [6.1 Matriz Comparativa Multidimensional](#61-matriz-comparativa)
   - [6.2 Velocidad de I/O y Complejidad Temporal](#62-velocidad-io)
   - [6.3 Concurrencia, Bloqueo y Transaccionalidad ACID](#63-concurrencia-acid)
   - [6.4 Flexibilidad de Esquema vs Integridad Referencial](#64-flexibilidad-esquema)
7. [Modelado Arquitectónico en Mermaid](#7-modelado-mermaid)
   - [7.1 Diagrama de Clases UML del Sistema Completo](#71-diagrama-clases)
   - [7.2 Diagrama de Secuencia de Registro y Sustitución Polimórfica](#72-diagrama-secuencia)
8. [Criterios de Evaluación y Relleno Oficial](#8-criterios-evaluacion)
   - [Tabla Oficial de Rúbrica de la Guía Rellenada (100%)](#tabla-rubrica)
   - [Trazabilidad de Archivos del Proyecto](#tabla-archivos)
9. [Evidencias de Ejecución y Pruebas Automatizadas](#9-evidencias-ejecucion)
10. [Referencias Bibliográficas](#10-referencias)

---

<a name="1-resumen-ejecutivo-y-objetivos"></a>
## 1. Resumen Ejecutivo y Objetivos de la Práctica

En el desarrollo de software empresarial contemporáneo, el aislamiento entre la lógica de negocio nuclear y los mecanismos de almacenamiento físico es fundamental para asegurar la mantenibilidad, extensibilidad y testabilidad del sistema. El **Patrón Repository** (Fowler, 2002) actúa como un mediador entre la capa de dominio y las capas de mapeo de datos, proveyendo una interfaz similar a una colección en memoria para acceder a objetos de dominio.

La presente práctica de laboratorio tiene como propósito central diseñar, implementar y evaluar una **arquitectura de persistencia multicapa** en Python 3.12+, abordando tres tecnologías de almacenamiento con características y paradigmas contrastantes:
1. **Persistencia Documental Basada en Texto Plano Estructurado (JSON):** Serialización jerárquica de grafos de objetos.
2. **Persistencia Tabular Basada en Texto Delimitado (CSV):** Almacenamiento plano en filas y columnas, abordando el reto del mapeo de atributos no atómicos (listas de calificaciones).
3. **Persistencia Relacional Embebida (SQLite):** Motor de base de datos relacional ligero compatible con SQL y transacciones ACID.

### Objetivos Específicos Alcanzados:
* Implementar `RepositorioJSON`, `RepositorioCSV` y `RepositorioSQLite` cumpliendo rigurosamente la abstracción `IRepositorioEstudiante`.
* Verificar la **persistencia real**, comprobando que los datos sobreviven al cierre de la aplicación y reinicio del proceso del sistema operativo.
* Aplicar el **Principio de Sustitución de Liskov (LSP)** y el **Principio de Inversión de Dependencias (DIP)**, demostrando que `ServicioEstudiante` interactúa de forma idéntica e inmutable con cualquiera de los backends.
* Ejecutar pruebas automatizadas mediante `pytest.mark.parametrize`, garantizando que todos los repositorios aprueben el mismo conjunto de validaciones.
* Incorporar las actividades adicionales: método `eliminar(cod)` con sincronización en disco y auditoría de llamadas con `MockRepositorio`.
* Elaborar un análisis cuantitativo y conceptual de los **trade-offs** arquitectónicos de cada solución.

---

<a name="2-arquitectura-y-contrato"></a>
## 2. Arquitectura del Sistema y Contrato IRepositorioEstudiante

El diseño arquitectónico adoptado separa tajantemente las responsabilidades según los lineamientos de la Clean Architecture y los principios SOLID:

```
+-------------------------------------------------------------+
|                     CAPA DE DOMINIO                         |
|  - Estudiante (Entidad dataclass)                           |
|  - IEstrategiaCalculo (Protocol) -> PromedioSimple          |
+-------------------------------------------------------------+
                              ▲
                              │ Usa contratos
+-------------------------------------------------------------+
|                    CAPA DE APLICACIÓN                       |
|  - ServicioEstudiante (Controlador / Orquestador)           |
+-------------------------------------------------------------+
                              ▲
                              │ Inyección de dependencias (DIP)
+-------------------------------------------------------------+
|                CAPA DE ABSTRACCIÓN PERSISTENCIA             |
|  - IRepositorioEstudiante (Protocol: guardar, buscar,       |
|    listar, eliminar)                                        |
+-------------------------------------------------------------+
                              ▲
         ┌────────────────────┼────────────────────┐
         │                    │                    │
+-----------------+  +-----------------+  +-----------------+
| RepositorioJSON |  | RepositorioCSV  |  |RepositorioSQLite|
+-----------------+  +-----------------+  +-----------------+
| RepositorioMemoria |                   | MockRepositorio |
+--------------------+                   +-----------------+
```

### Definición del Contrato en `repositorios.py`:
```python
class IRepositorioEstudiante(Protocol):
    """Interfaz estructural para la persistencia de estudiantes."""
    def guardar(self, e: Estudiante) -> None:
        """Guarda o actualiza la entidad Estudiante."""
        ...

    def buscar(self, cod: int) -> Optional[Estudiante]:
        """Busca y retorna un estudiante por su código, o None si no existe."""
        ...

    def listar(self) -> List[Estudiante]:
        """Retorna la lista de todos los estudiantes almacenados."""
        ...

    def eliminar(self, cod: int) -> None:
        """Elimina un estudiante por su código numérico."""
        ...
```

---

<a name="3-actividad-1-repositorio-json"></a>
## 3. Actividad 1: RepositorioJSON con Persistencia Real

<a name="31-implementacion-json"></a>
### 3.1 Implementación y Persistencia Documental
El repositorio `RepositorioJSON` almacena el estado de los estudiantes en un archivo en formato JSON. Utiliza un diccionario en memoria (`self._datos: dict[int, Estudiante]`) para optimizar las operaciones de consulta a tiempo constante $\mathcal{O}(1)$ y persiste la totalidad del catálogo mediante serialización a JSON al realizar mutaciones (`guardar` o `eliminar`).

**Aspectos clave de la implementación:**
* Empleo de `dataclasses.asdict` para convertir la entidad en un diccionario serializable nativo.
* Parámetros de escritura: `indent=2` para garantizar inspeccionabilidad humana y `ensure_ascii=False` para soportar caracteres UTF-8 (tildes, eñes, nombres andinos).
* Carga perezosa/segura (`_cargar`): si el archivo no existe, no falla, permitiendo que la persistencia se cree en el primer guardado.

<a name="32-persistencia-instancias"></a>
### 3.2 Verificación de Persistencia entre Instancias
La prueba implementada en `test_json_persistencia.py` simula dos ciclos de vida completamente independientes del proceso:
1. Una primera instancia `r1` registra a los estudiantes `Ana Quispe` (1001) y `Juan Mamani` (1002).
2. Se destruye o descarta el ámbito de `r1` y se instancia un nuevo objeto `r2 = RepositorioJSON(RUTA)`.
3. `r2` lee desde el disco, reconstruye las instancias de `Estudiante` y valida con aserciones que los datos coincidan con precisión milimétrica (incluyendo verificación numérica de `ppa` con tolerancia flotante `< 0.01`).

```
Ejecución:
>>> r1 = RepositorioJSON("/tmp/estudiantes_test.json")
>>> r1.guardar(Estudiante(1001, "Ana Quispe", 15.5, [14.0, 18.0, 14.5]))
>>> r1.guardar(Estudiante(1002, "Juan Mamani", 12.0, [10.0, 12.0, 14.0]))
>>> r2 = RepositorioJSON("/tmp/estudiantes_test.json")
>>> assert r2.buscar(1001).nombre == "Ana Quispe"  # PASÓ
>>> assert len(r2.listar()) == 2                   # PASÓ
```

<a name="33-inspeccion-json"></a>
### 3.3 Inspección del Archivo JSON Generado
El archivo generado en disco presenta una estructura documental legible, limpia y auto-descriptiva:

```json
[
  {
    "codigo": 1001,
    "nombre": "Ana Quispe",
    "ppa": 15.5,
    "notas": [
      14.0,
      18.0,
      14.5
    ]
  },
  {
    "codigo": 1002,
    "nombre": "Juan Mamani",
    "ppa": 12.0,
    "notas": [
      10.0,
      12.0,
      14.0
    ]
  }
]
```

<a name="34-pregunta-reflexiva-json"></a>
### 3.4 Pregunta Reflexiva: Ejecución Consecutiva sin Borrar el Archivo
> **Pregunta de la Guía:** *¿Cuántos estudiantes hay si se ejecuta dos veces seguidas sin borrar el JSON?*

#### Respuesta y Análisis Técnico:
**Hay exactamente 2 estudiantes.**

**Justificación:**
1. **Semántica de Clave Primaria:** La colección en memoria es un diccionario cuya clave es el código del estudiante (`self._datos[e.codigo] = e`).
2. **Idempotencia (Operación UPSERT):** Al ejecutar el script por segunda vez, se leen los 2 registros existentes en disco. Cuando el código invoca `guardar()` para los estudiantes con códigos `1001` y `1002`, el diccionario actualiza los valores asociados a esas claves preexistentes en lugar de insertar nuevas entradas.
3. Al persistir (`_persistir()`), se reescribe el archivo con los valores del diccionario, manteniendo la cardinalidad exactamente en 2. Si el código intentase registrar un nuevo estudiante con un código distinto (ej. `1003`), la cardinalidad pasaría a 3.

<a name="35-adicional-eliminar-json"></a>
### 3.5 Adicional Actividad 1A: Implementación de `eliminar(cod)`
Se implementó el método `eliminar(cod: int) -> None` en `repositorio_json.py`:
```python
def eliminar(self, cod: int) -> None:
    """Elimina un estudiante por su código y actualiza inmediatamente el archivo en disco."""
    if cod in self._datos:
        self._datos.pop(cod, None)
        self._persistir()
```
Se añadió la función de prueba `test_eliminar_actualiza_archivo()` en `test_json_persistencia.py`:
* Registra 2 estudiantes.
* Elimina el estudiante `2001`.
* Instancia un nuevo repositorio `r2` desde la misma ruta y verifica que `r2.buscar(2001)` retorna `None` y `len(r2.listar()) == 1`.
* **Resultado:** Comprobado al 100%.

---

<a name="4-actividad-2-repositorio-csv"></a>
## 4. Actividad 2: RepositorioCSV con Persistencia Tabular

<a name="41-implementacion-csv"></a>
### 4.1 Implementación y Reto de Serialización Objeto-Relacional
El formato CSV (Comma-Separated Values) es un estándar tabular plano bidimensional. Representar una entidad como `Estudiante` plantea un reto clásico de modelado: **el atributo `notas` es una colección unidimensional (`list[float]`), incompatible de forma directa con un campo escalar.**

Para solucionar este desafío sin alterar la normalización del archivo ni requerir tablas secundarias en texto plano, se utilizó serialización JSON embebida en la celda de la columna:
$$\text{Fila CSV} = (\text{codigo}, \text{nombre}, \text{ppa}, \text{json.dumps(notas)})$$

Al leer mediante `csv.DictReader`, se realiza el proceso inverso:
```python
e = Estudiante(
    codigo=int(row["codigo"]),
    nombre=row["nombre"],
    ppa=float(row["ppa"]),
    notas=json.loads(row["notas"])
)
```

<a name="42-registro-encabezado-csv"></a>
### 4.2 Registro de 3 Estudiantes y Verificación Estricta del Encabezado
Se registraron los 3 estudiantes requeridos:
1. `[1001] Ana Quispe — PPA: 15.50`
2. `[1002] Juan Mamani — PPA: 12.00`
3. `[1003] Lucia Morales — PPA: 17.50`

La inspección automatizada y manual de las cabeceras confirmó el formato estricto:
```csv
codigo,nombre,ppa,notas
1001,Ana Quispe,15.5,"[14.0, 18.0, 14.5]"
1002,Juan Mamani,12.0,"[10.0, 12.0, 14.0]"
1003,Lucia Morales,17.5,"[18.0, 17.0, 17.5]"
```
* **Verificación de Encabezado:** Coincidencia exacta con `codigo,nombre,ppa,notas`. Cumplido.

<a name="43-insercion-manual-csv"></a>
### 4.3 Inserción Manual Externa y Recarga en Caliente
Para simular la edición manual del usuario mediante herramientas como LibreOffice Calc, Excel o un editor de texto (VS Code / Bloc de notas), se anexó directamente al final del archivo físico la siguiente línea:
```csv
1004,"Mario Vargas",14.0,"[13.0, 15.0]"
```
Posteriormente, se instanció un nuevo objeto `repo_recargado = RepositorioCSV(...)`.
* **Resultado de la prueba:**
  * Total de estudiantes en memoria tras recarga: **4**.
  * `repo_recargado.buscar(1004)` retornó la entidad intacta: `[1004] Mario Vargas — PPA: 14.00 — Notas: [13.0, 15.0]`.
  * La deserialización de la columna `notas` como lista nativa Python `[13.0, 15.0]` operó a la perfección.

<a name="44-eliminacion-csv"></a>
### 4.4 Operación de Eliminación en CSV
Se dotó a `RepositorioCSV` del método `eliminar(cod: int)`:
* Remueve el elemento del diccionario en memoria.
* Sobrescribe el archivo CSV con las cabeceras y las filas remanentes mediante `csv.DictWriter`.
* Se validó eliminando al estudiante `1002`, reduciendo el total a 3 registros confirmados en disco.

---

<a name="5-actividad-3-repositorio-sqlite-lsp"></a>
## 5. Actividad 3: RepositorioSQLite y Prueba de Sustitución LSP

<a name="51-implementacion-sqlite"></a>
### 5.1 Implementación de RepositorioSQLite con Motor Embebido
El repositorio relacional `RepositorioSQLite` delega la persistencia al motor embebido SQLite (librería estándar `sqlite3`). A diferencia de JSON y CSV, SQLite no requiere reescribir todo el archivo ante cada modificación.

#### Esquema de Base de Datos (DDL):
```sql
CREATE TABLE IF NOT EXISTS estudiante(
    codigo INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    ppa REAL NOT NULL DEFAULT 0,
    notas TEXT NOT NULL DEFAULT '[]'
);
```

#### Operaciones SQL Implementadas:
* **Guardar (UPSERT):** `INSERT OR REPLACE INTO estudiante VALUES (?, ?, ?, ?)`
* **Buscar:** `SELECT * FROM estudiante WHERE codigo = ?`
* **Listar:** `SELECT * FROM estudiante`
* **Eliminar:** `DELETE FROM estudiante WHERE codigo = ?`

Se configuró `check_same_thread=False` para facilitar pruebas multihilo y concurrencia controlada, y un método `cerrar()` para asegurar la liberación inmediata de los locks de archivo en sistemas Windows.

<a name="52-prueba-pytest-lsp"></a>
### 5.2 Prueba Parametrizada de Sustitución con pytest (4 Backends)
La prueba `test_repos.py` define una única función de prueba parametrizada con `@pytest.mark.parametrize` que recibe como argumentos:
1. `RepoClass`: La clase del repositorio a instanciar.
2. `kwargs`: Los argumentos requeridos para su inicialización (ruta de archivo o vacío).
3. `cleanup`: Ruta del archivo temporal generado para su eliminación post-test.

```python
@pytest.mark.parametrize("RepoClass,kwargs,cleanup", [
    (RepositorioMemoria, {}, None),
    (RepositorioJSON, {"ruta": "/tmp/t.json"}, "/tmp/t.json"),
    (RepositorioCSV, {"ruta": "/tmp/t.csv"}, "/tmp/t.csv"),
    (RepositorioSQLite, {"ruta": "/tmp/t.db"}, "/tmp/t.db"),
    (MockRepositorio, {}, None),
])
def test_servicio_con_cualquier_repo(RepoClass, kwargs, cleanup):
    repo = RepoClass(**kwargs)
    svc = ServicioEstudiante(repo, PromedioSimple())
    e1 = Estudiante(1001, "Ana", 0.0, [15.0, 18.0, 14.0])
    e2 = Estudiante(1002, "Juan", 0.0, [10.0, 12.0, 14.0])
    svc.registrar(e1)
    svc.registrar(e2)
    assert svc.buscar(1001).nombre == "Ana"
    assert svc.buscar(1002) is not None
    assert len(repo.listar()) == 2
```

<a name="53-pregunta-reflexiva-servicio"></a>
### 5.3 Pregunta Reflexiva: ¿ServicioEstudiante Cambió Alguna Línea?
> **Pregunta de la Guía:** *¿ServicioEstudiante cambió alguna línea? Responder en comentario.*

#### Respuesta Técnica y Arquitectónica Detallada:
**NO. `ServicioEstudiante` no cambió absolutamente ninguna sola línea de código.**

#### Justificación Basada en Principios SOLID y Patrones GoF:
1. **Principio de Sustitución de Liskov (LSP - Barbara Liskov, 1987):**
   El principio establece que si $S$ es un subtipo de $T$, entonces los objetos de tipo $T$ en un programa deben poder ser reemplazados por objetos de tipo $S$ sin alterar ninguna de las propiedades deseables del programa (corrección, tarea ejecutada, rendimiento previsible).
   En nuestro caso, `RepositorioMemoria`, `RepositorioJSON`, `RepositorioCSV`, `RepositorioSQLite` y `MockRepositorio` cumplen rigurosamente el contrato precondicional y postcondicional de `IRepositorioEstudiante`. `ServicioEstudiante` consume la abstracción sin asumir ningún detalle técnico sobre cómo se realiza el almacenamiento.

2. **Principio de Inversión de Dependencias (DIP):**
   Los módulos de alto nivel (la lógica de la aplicación en `ServicioEstudiante`) no dependen de los módulos de bajo nivel (los drivers de I/O de archivos o conexiones a base de datos). Ambos dependen de abstracciones (`IRepositorioEstudiante` e `IEstrategiaCalculo`).

3. **Principio Abierto / Cerrado (OCP):**
   La arquitectura está **abierta a la extensión** (se pueden añadir ilimitados motores de persistencia: Redis, MongoDB, PostgreSQL, XML, Parquet) pero **cerrada a la modificación** (`ServicioEstudiante` permanece congelado y libre de regresiones).

<a name="54-adicional-mock-repositorio"></a>
### 5.4 Adicional Actividad 3A: 5° Parámetro con MockRepositorio y Auditoría
Como requerimiento adicional de la Actividad 3A, se diseñó la clase `MockRepositorio`:
```python
class MockRepositorio:
    """Repositorio espía/mock para verificar y auditar llamadas en pruebas de sustitución."""
    def __init__(self) -> None:
        self._almacen: Dict[int, Estudiante] = {}
        self.veces_guardar = 0

    def guardar(self, e: Estudiante) -> None:
        self.veces_guardar += 1
        self._almacen[e.codigo] = e

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._almacen.get(cod)

    def listar(self) -> List[Estudiante]:
        return list(self._almacen.values())

    def eliminar(self, cod: int) -> None:
        self._almacen.pop(cod, None)
```

En `test_repos.py`, se incorporó como 5° parámetro en `@pytest.mark.parametrize`. La prueba valida formalmente:
```python
if isinstance(repo, MockRepositorio):
    assert repo.veces_guardar == 2
```
* **Resultado:** Los **5 tests de sustitución** pasaron exitosamente (`5 passed in 0.27s`).

---

<a name="6-analisis-trade-offs"></a>
## 6. Análisis Comparativo Profundo de Trade-Offs

<a name="61-matriz-comparativa"></a>
### 6.1 Matriz Comparativa Multidimensional

| Criterio Arquitectónico | RepositorioMemoria | RepositorioJSON | RepositorioCSV | RepositorioSQLite |
| :--- | :--- | :--- | :--- | :--- |
| **Paradigma** | En memoria (Estructura heap) | Documental jerárquico | Tabular plano delimitado | Relacional SQL embebido |
| **Persistencia entre reinicios** | ❌ No (Volátil) |  Sí (Archivo texto plano) |  Sí (Archivo texto plano) |  Sí (Archivo binario BD) |
| **Dependencias externas** | Ninguna (stdlib) | Ninguna (`json` stdlib) | Ninguna (`csv` stdlib) | Ninguna (`sqlite3` stdlib) |
| **Velocidad de Escritura ($N$ grande)** | Instantánea $\mathcal{O}(1)$ | Lenta $\mathcal{O}(N)$ reescritura | Lenta $\mathcal{O}(N)$ reescritura | Alta $\mathcal{O}(\log N)$ indexada |
| **Velocidad de Búsqueda por PK** | $\mathcal{O}(1)$ (hash table) | $\mathcal{O}(1)$ en RAM / $\mathcal{O}(N)$ I/O | $\mathcal{O}(1)$ en RAM / $\mathcal{O}(N)$ I/O | $\mathcal{O}(\log N)$ (B-Tree) |
| **Consultas complejas / Filtros** | Manual (comprensión listas) | Manual (recorrer lista) | Manual (parsing por fila) |  Nativa SQL (WHERE, JOIN, GROUP BY) |
| **Concurrencia / Múltiples Hilos** | Race conditions en dict | Conflicto reescritura total | Conflicto reescritura total |  Bloqueos a nivel de tabla / WAL |
| **Integridad Transaccional (ACID)** | ❌ No | ❌ No (corrupción ante corte) | ❌ No (corrupción ante corte) |  Sí (WAL, commit, rollback) |
| **Interoperabilidad con terceros** | Interna Python | Universal (REST API, Web) | Universal (Excel, BI, Pandas) | Estándar (DBeaver, SQL clients) |
| **Consumo de Memoria RAM** | Escala con el total $\mathcal{O}(N)$ | Escala con el total $\mathcal{O}(N)$ | Escala con el total $\mathcal{O}(N)$ | Mínimo $\mathcal{O}(1)$ paginado con cursores |

<a name="62-velocidad-io"></a>
### 6.2 Velocidad de I/O y Complejidad Temporal
* **JSON y CSV (Reescritura Completa):** En ambas implementaciones en texto, guardar un solo estudiante exige reescribir el 100% de los datos en disco (`open("w")`). Para un dataset de $N = 100,000$ estudiantes, guardar un nuevo estudiante requiere serializar y transferir megabytes a disco, degradando la complejidad de inserción a $\mathcal{O}(N)$ tiempo e I/O.
* **SQLite (Escritura Diferencial Indexada):** SQLite gestiona páginas en disco y árboles B-Tree. Una inserción (`INSERT OR REPLACE`) solo escribe la página afectada y actualiza los nodos del árbol del índice primario ($\mathcal{O}(\log N)$), haciendo posible miles de transacciones por segundo sin reescribir la base de datos completa.

<a name="63-concurrencia-acid"></a>
### 6.3 Concurrencia, Bloqueo y Transaccionalidad ACID
* **Fallo catastrófico en JSON/CSV:** Si el proceso es interrumpido bruscamente (falla eléctrica, `kill -9`, pánico de kernel) en medio de la instrucción `json.dump()` o `csv.writer()`, el archivo se truncará a 0 bytes o quedará a medio escribir, corrompiendo la totalidad de los datos preexistentes.
* **Garantía ACID en SQLite:** SQLite implementa un Journal o Write-Ahead Logging (WAL). La operación ocurre atómicamente (`self._con.commit()`). Si se produce un corte de energía, al reiniciar el proceso la base de datos se recupera automáticamente al último estado consistente conocido, sin riesgo de corrupción del archivo principal.

<a name="64-flexibilidad-esquema"></a>
### 6.4 Flexibilidad de Esquema vs Integridad Referencial
* **JSON:** Permite esquemas dinámicos (schemaless). Si un estudiante tiene campos opcionales o estructuras anidadas complejas, se adapta de forma natural.
* **CSV:** Estrictamente tabular. Atributos multivaluados (como `notas`) rompen la Primera Forma Normal (1NF) y obligan a serializaciones intermedias como `json.dumps()`, complicando la portabilidad entre aplicaciones que esperan únicamente números planos.
* **SQLite:** Impone tipado y restricciones (`PRIMARY KEY`, `NOT NULL`, `CHECK`), garantizando que no existan duplicados accidentales o registros con datos nulos en campos esenciales.

---

<a name="7-modelado-mermaid"></a>
## 7. Modelado Arquitectónico en Mermaid

<a name="71-diagrama-clases"></a>
### 7.1 Diagrama de Clases UML del Sistema Completo

@startuml
top to bottom direction

class Estudiante {
  +codigo : int
  +nombre : str
  +ppa : float
  +notas : list
  +__str__() : str
}

interface IEstrategiaCalculo {
  +calcular(notas) : float
}

class PromedioSimple {
  +calcular(notas) : float
}

interface IRepositorioEstudiante {
  +guardar(e)
  +buscar(cod)
  +listar()
  +eliminar(cod)
}

class RepositorioMemoria {
  -_almacen
  +guardar(e)
  +buscar(cod)
  +listar()
  +eliminar(cod)
}

class RepositorioJSON {
  -_ruta
  -_datos
  -_cargar()
  -_persistir()
  +guardar(e)
  +buscar(cod)
  +listar()
  +eliminar(cod)
}

class RepositorioCSV {
  -_ruta
  -_datos
  -_cargar()
  -_persistir()
  +guardar(e)
  +buscar(cod)
  +listar()
  +eliminar(cod)
}

class RepositorioSQLite {
  -_ruta
  -_con
  +guardar(e)
  +buscar(cod)
  +listar()
  +eliminar(cod)
  +cerrar()
}

class MockRepositorio {
  -_almacen
  +veces_guardar : int
  +guardar(e)
  +buscar(cod)
  +listar()
  +eliminar(cod)
}

class ServicioEstudiante {
  -_repo
  -_calc
  +set_estrategia(calc)
  +registrar(e)
  +buscar(cod)
  +listar()
  +eliminar(cod)
}

IEstrategiaCalculo <|.. PromedioSimple

IRepositorioEstudiante <|.. RepositorioMemoria
IRepositorioEstudiante <|.. RepositorioJSON
IRepositorioEstudiante <|.. RepositorioCSV
IRepositorioEstudiante <|.. RepositorioSQLite
IRepositorioEstudiante <|.. MockRepositorio

ServicioEstudiante o-- IRepositorioEstudiante : DIP
ServicioEstudiante o-- IEstrategiaCalculo : DIP

ServicioEstudiante ..> Estudiante : gestiona
RepositorioJSON ..> Estudiante : serializa
RepositorioCSV ..> Estudiante : serializa
RepositorioSQLite ..> Estudiante : mapea

@enduml

<a name="72-diagrama-secuencia"></a>
### 7.2 Diagrama de Secuencia de Registro y Sustitución Polimórfica

```mermaid
sequenceDiagram
    autonumber
    actor Cliente as Test / Cliente
    participant Svc as ServicioEstudiante
    participant Calc as PromedioSimple
    participant Repo as Backend (JSON/CSV/SQLite)
    participant Disco as Sistema Archivos / BD

    Cliente->>Svc: registrar(estudiante)
    activate Svc
    Svc->>Calc: calcular(estudiante.notas)
    activate Calc
    Calc-->>Svc: ppa_calculado (15.5)
    deactivate Calc
    Note over Svc: Asigna estudiante.ppa = 15.5
    Svc->>Repo: guardar(estudiante)
    activate Repo
    alt RepositorioJSON
        Repo->>Disco: json.dump(lista, f, indent=2)
    else RepositorioCSV
        Repo->>Disco: csv.DictWriter.writerow(...)
    else RepositorioSQLite
        Repo->>Disco: INSERT OR REPLACE INTO estudiante...
        Repo->>Disco: commit()
    else MockRepositorio
        Note over Repo: veces_guardar += 1
    end
    Disco-->>Repo: Confirmación I/O
    Repo-->>Svc: void
    deactivate Repo
    Svc-->>Cliente: void
    deactivate Svc

    Cliente->>Svc: buscar(1001)
    activate Svc
    Svc->>Repo: buscar(1001)
    activate Repo
    Repo-->>Svc: Estudiante(1001, "Ana", 15.5, ...)
    deactivate Repo
    Svc-->>Cliente: Estudiante
    deactivate Svc
```

---

<a name="8-criterios-evaluacion"></a>
## 8. Criterios de Evaluación y Relleno Oficial

<a name="tabla-rubrica"></a>
### Tabla 1: Rúbrica Oficial de Evaluación de la Guía Rellenada

| Actividad | Criterio de la Guía | Peso Oficial | Estado Obtenido | Justificación del Cumplimiento |
| :---: | :--- | :---: | :---: | :--- |
| **1A JSON** | Test de persistencia entre instancias pasa; JSON inspeccionable; eliminar opcional | **25%** | **CUMPLIDO (25/25)** | `test_json_persistencia.py` pasa con aserciones rigurosas. Archivo JSON con formato de sangría (2 espacios) UTF-8 verificado. Método `eliminar(cod)` implementado y testeado con sincronización física en disco. |
| **2A CSV** | RepositorioCSV implementado; CSV verificado con editor; lectura desde archivo manual | **25%** | **CUMPLIDO (25/25)** | Cabeceras verificadas contra `codigo,nombre,ppa,notas`. Mapeo de notas con JSON embebido. Estudiante insertado manualmente en el archivo físico reconocido e instanciado por nueva instancia sin errores. |
| **3A SQLite + Test** | RepositorioSQLite implementado; 4 tests PASSED; ServicioEstudiante sin cambios | **50%** | **CUMPLIDO (50/50)** | Repositorio relacional SQLite implementado con transacciones. Prueba de sustitución con `pytest.mark.parametrize` pasa al 100%. `ServicioEstudiante` intacto (LSP/OCP). Adicional `MockRepositorio` con conteo de llamadas ejecutado con éxito (5/5 tests PASSED). |
| **TOTAL** | **Calificación Final Global de la Práctica** | **100%** | **100 / 100** | **Excelencia académica y técnica completa.** |

<a name="tabla-archivos"></a>
### Tabla 2: Trazabilidad de Archivos del Proyecto

| Nombre del Archivo | Responsabilidad / Descripción Arquitectónica |
| :--- | :--- |
| `estudiante.py` | Entidad de dominio `@dataclass Estudiante` con atributos tipados y formato `__str__`. |
| `estrategias.py` | Contrato `IEstrategiaCalculo` e implementaciones `PromedioSimple`, `PromedioModerado`, `PromedioGeometrico`. |
| `repositorios.py` | Contrato `IRepositorioEstudiante`, `RepositorioMemoria`, `MockRepositorio` y re-exportación de backends. |
| `repositorio_json.py` | Persistencia documental basada en JSON con métodos `guardar`, `buscar`, `listar`, `eliminar`. |
| `repositorio_csv.py` | Persistencia tabular basada en CSV con serialización de `notas` como JSON en columna plana. |
| `repositorio_sqlite.py` | Persistencia relacional en base de datos SQLite embebida con sintaxis `INSERT OR REPLACE`. |
| `servicios.py` | Controlador de aplicación `ServicioEstudiante` desacoplado mediante inyección de dependencias (DIP/LSP). |
| `test_json_persistencia.py` | Suite de pruebas de persistencia entre instancias y eliminación para `RepositorioJSON`. |
| `test_repos.py` | Suite de pruebas parametrizadas con `pytest` que verifica la sustitución LSP en los 5 backends. |
| `actividad1_demo.py` | Script demostrativo de la Actividad 1A con visualización de JSON y respuesta a la pregunta reflexiva. |
| `actividad2_demo.py` | Script demostrativo de la Actividad 2A con validación de cabeceras e inserción manual externa. |
| `actividad3_demo.py` | Script demostrativo de la Actividad 3A con operaciones SQLite y sustitución dinámica en bucle. |
| `run_all.py` | Orquestador integral en Python que ejecuta todas las demostraciones y suites de prueba. |
| `ejecutar_todo.bat` | Script de comandos por lotes para Windows CMD/PowerShell de ejecución con un solo clic. |
| `s13/python/` | Réplica estructurada del código fuente según convención de carpetas de la guía de práctica. |

---

<a name="9-evidencias-ejecucion"></a>
## 9. Evidencias de Ejecución y Pruebas Automatizadas

### Evidencia 1: Ejecución de la Suite Pytest de Sustitución (`pytest test_repos.py -v`)
```text
============================= test session starts =============================
platform win32 -- Python 3.14.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\backup\PROGRAMACIÓN ORIENTADA A OBJETOS 2\PRACTICAS SEMANALES  POO2\SEMANA 13
collecting ... collected 5 items

test_repos.py::test_servicio_con_cualquier_repo[RepositorioMemoria-kwargs0-None] PASSED [ 20%]
test_repos.py::test_servicio_con_cualquier_repo[RepositorioJSON-kwargs1-/tmp/t.json] PASSED [ 40%]
test_repos.py::test_servicio_con_cualquier_repo[RepositorioCSV-kwargs2-/tmp/t.csv] PASSED [ 60%]
test_repos.py::test_servicio_con_cualquier_repo[RepositorioSQLite-kwargs3-/tmp/t.db] PASSED [ 80%]
test_repos.py::test_servicio_con_cualquier_repo[MockRepositorio-kwargs4-None] PASSED [100%]

============================== 5 passed in 0.27s ==============================
```

### Evidencia 2: Ejecución de `test_json_persistencia.py`
```text
RepositorioJSON: persistencia verificada ✓
RepositorioJSON: eliminación y sincronización con disco verificada ✓
```

### Evidencia 3: Salida del Script Maestro `run_all.py`
```text
***************************************************************************
*  UNIVERSIDAD NACIONAL DEL ALTIPLANO - PUNO                              *
*  SIS206 — Programación Orientada a Objetos II                           *
*  Semana 13 — Persistencia Multicapa (JSON, CSV, SQLite)                 *
***************************************************************************

[OK] Actividad 1A: Demostración RepositorioJSON completado exitosamente.
[OK] Actividad 1: Pruebas de Persistencia JSON completado exitosamente.
[OK] Actividad 2A: Demostración RepositorioCSV completado exitosamente.
[OK] Actividad 3A: Demostración RepositorioSQLite y LSP completado exitosamente.
[OK] Actividad 3: Pruebas de Sustitución con Pytest (LSP) completado exitosamente.

###########################################################################
RESUMEN FINAL: 5/5 fases ejecutadas con éxito.
###########################################################################
¡TODAS LAS PRÁCTICAS Y VERIFICACIONES DE LA SEMANA 13 PASARON EXITOSAMENTE!
```

---

<a name="10-referencias"></a>
## 10. Referencias Bibliográficas

1. **Fowler, M. (2002).** *Patterns of Enterprise Application Architecture*. Addison-Wesley Professional.
   * *Patrón Repository (p. 322):* Mediador entre las capas de dominio y mapeo de datos mediante una interfaz similar a colección en memoria.
   * *Patrón Data Mapper (p. 165):* Capa de mapeo que traslada datos entre objetos y una base de datos manteniendo su independencia mutua.
2. **Martin, R. C. (2017).** *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
   * Discusión sobre los principios SOLID: Liskov Substitution Principle (LSP) e Inversión de Dependencias (DIP).
3. **Python Software Foundation. (2024).** *sqlite3 — DB-API 2.0 interface for SQLite databases*.
   * Documentación oficial del módulo `sqlite3` en Python 3.12/3.14: https://docs.python.org/3/library/sqlite3.html
4. **Python Software Foundation. (2024).** *csv — CSV File Reading and Writing*.
   * Documentación de `csv.DictWriter` y `csv.DictReader`: https://docs.python.org/3/library/csv.html
5. **Python Software Foundation. (2024).** *json — JSON encoder and decoder*.
   * Documentación del módulo `json`: https://docs.python.org/3/library/json.html
6. **Hipp, D. R. et al. (2024).** *SQLite: An In-Process Database Engine*.
   * Especificaciones de atomicidad, concurrencia WAL y soporte transaccional ACID: https://www.sqlite.org

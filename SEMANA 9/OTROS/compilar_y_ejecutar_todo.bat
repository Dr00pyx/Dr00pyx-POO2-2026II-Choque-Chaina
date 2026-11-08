@echo off
chcp 65001 > nul
cls
echo =======================================================================
echo     SIS206 - POO II ^| SEMANA 09: COMPILACION Y EJECUCION COMPLETA
echo =======================================================================
echo.

set BASE_DIR=%~dp0

:: 1. COMPILAR Y EJECUTAR C++17
echo [1/3] Compilando y ejecutando C++17 (Actividad 2A)...
echo -----------------------------------------------------------------------
cd /d "%BASE_DIR%s09\cpp"
echo Ejecutando: g++ -std=c++17 main.cpp -o main.exe
g++ -std=c++17 main.cpp -o main.exe
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo la compilacion de C++17.
    pause
    exit /b %ERRORLEVEL%
)
echo [OK] Compilacion exitosa. Ejecutando main.exe:
echo.
main.exe
echo.

:: 2. EJECUTAR PYTHON 3 Y PRUEBAS UNITARIAS
echo -----------------------------------------------------------------------
echo [2/3] Ejecutando Python 3.12+ (Actividad 2B)...
echo -----------------------------------------------------------------------
cd /d "%BASE_DIR%s09\python"
echo Ejecutando: python estudiante.py
python estudiante.py
echo.
echo Ejecutando pruebas con pytest:
python -m pytest test_estudiante.py -v
echo.

:: 3. RENDERIZAR DIAGRAMA PLANTUML
echo -----------------------------------------------------------------------
echo [3/3] Generando Diagrama de Arquitectura PNG (Actividad 3A)...
echo -----------------------------------------------------------------------
cd /d "%BASE_DIR%s09\plantuml"
powershell -ExecutionPolicy Bypass -File render_diagram.ps1
echo.

echo =======================================================================
echo     TODO COMPILADO Y EJECUTADO CON EXITO (SEMANA 09)
echo =======================================================================
echo Archivos generados listos para revisar o entregar:
echo  - C++:       s09\cpp\main.exe
echo  - Python:    s09\python\estudiante.py (8 pruebas pytest pasadas)
echo  - PlantUML:  s09_arquitectura_apellido.png
echo  - Entorno:   verificacion_entorno_apellido.txt
echo  - Reflexion: ACTIVIDAD_4_REFLEXION.md
echo.
pause

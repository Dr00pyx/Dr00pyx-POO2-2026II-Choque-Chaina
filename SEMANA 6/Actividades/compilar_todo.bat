@echo off
chcp 65001 > nul
echo =====================================================================
echo    COMPILACION Y EJECUCION COMPLETA - SEMANA 6 (POO II - UNAP PUNO)
echo =====================================================================

cd /d "C:\Users\MELVIN\.gemini\antigravity\scratch\semana6"

echo.
echo [1/5] Compilando Actividad 1 (Repositorio C++17)...
g++ -std=c++17 -Wall -Wextra -O2 -o actividad1.exe actividad1_main.cpp
if %errorlevel% neq 0 (echo Error al compilar Actividad 1 & pause & exit /b)
echo Ejecutando Actividad 1:
actividad1.exe

echo.
echo [2/5] Compilando Actividad 3 (PlanillaIterador C++17)...
g++ -std=c++17 -Wall -Wextra -O2 -o actividad3_cpp.exe actividad3_cpp_main.cpp
if %errorlevel% neq 0 (echo Error al compilar Actividad 3 C++ & pause & exit /b)
echo Ejecutando Actividad 3 (C++):
actividad3_cpp.exe

echo.
echo [3/5] Compilando Benchmark C++17 (vector vs unordered_map)...
g++ -std=c++17 -Wall -Wextra -O2 -o benchmark_cpp.exe benchmark_cpp.cpp
if %errorlevel% neq 0 (echo Error al compilar Benchmark C++ & pause & exit /b)
echo Ejecutando Benchmark C++:
benchmark_cpp.exe

echo.
echo [4/5] Compilando Proyecto Integrador C++17 (Actividad 5)...
g++ -std=c++17 -Wall -Wextra -O2 -o proyecto_integrador.exe proyecto_integrador_main.cpp
if %errorlevel% neq 0 (echo Error al compilar Proyecto Integrador & pause & exit /b)
echo Ejecutando Proyecto Integrador (C++):
proyecto_integrador.exe

echo.
echo [5/5] Compilando y ejecutando pruebas unitarias C++ (test_main.cpp)...
g++ -std=c++17 -Wall -Wextra -O2 -o test_main.exe test_main.cpp
if %errorlevel% neq 0 (echo Error al compilar test_main.cpp & pause & exit /b)
test_main.exe

echo.
echo =====================================================================
echo    TODOS LOS PROGRAMAS C++ COMPILARON Y CORRIERON EXITOSAMENTE
echo =====================================================================
pause

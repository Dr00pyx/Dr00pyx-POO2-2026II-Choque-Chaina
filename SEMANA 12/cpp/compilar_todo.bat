@echo off
setlocal enabledelayedexpansion

echo ======================================================================
echo COMPILANDO Y EJECUTANDO PROGRAMAS C++17 - SEMANA 12
echo SIS206 - POO II ^| Dr. Aldo H. Zanabria Galvez ^| UNAP Puno
echo ======================================================================

set CPPDIR=%~dp0
set OUTDIR=%TEMP%\semana12_cpp_build
if not exist "%OUTDIR%" mkdir "%OUTDIR%"

echo [1/3] Compilando actividad1_observer.cpp...
g++ -std=c++17 -Wall -Wextra -O2 "%CPPDIR%actividad1_observer.cpp" -I"%CPPDIR%." -o "%OUTDIR%\actividad1_observer.exe"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo al compilar actividad1_observer.cpp
    exit /b %ERRORLEVEL%
)

echo [2/3] Compilando actividad2_strategy.cpp...
g++ -std=c++17 -Wall -Wextra -O2 "%CPPDIR%actividad2_strategy.cpp" -I"%CPPDIR%." -o "%OUTDIR%\actividad2_strategy.exe"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo al compilar actividad2_strategy.cpp
    exit /b %ERRORLEVEL%
)

echo [3/3] Compilando main_mvc.cpp...
g++ -std=c++17 -Wall -Wextra -O2 "%CPPDIR%main_mvc.cpp" -I"%CPPDIR%." -o "%OUTDIR%\main_mvc.exe"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo al compilar main_mvc.cpp
    exit /b %ERRORLEVEL%
)

echo.
echo ======================================================================
echo COMPILACION EXITOSA. INICIANDO EJECUCION DE CADA ACTIVIDAD:
echo ======================================================================

echo.
echo ======================================================================
echo --- EJECUTANDO ACTIVIDAD 1A (OBSERVER) ---
echo ======================================================================
"%OUTDIR%\actividad1_observer.exe"

echo.
echo ======================================================================
echo --- EJECUTANDO ACTIVIDAD 2A (STRATEGY CON CONTEXTO) ---
echo ======================================================================
"%OUTDIR%\actividad2_strategy.exe"

echo.
echo ======================================================================
echo --- EJECUTANDO ACTIVIDAD 3A (MVC COMPLETO) ---
echo ======================================================================
"%OUTDIR%\main_mvc.exe"

echo.
echo ======================================================================
echo [OK] TODAS LAS ACTIVIDADES C++17 FINALIZARON CON EXITO.
echo ======================================================================

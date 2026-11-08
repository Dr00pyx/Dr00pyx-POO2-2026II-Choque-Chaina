@echo off
echo ====================================================================
echo   Compilando solid_s10.cpp con g++ (C++17)...
echo ====================================================================
g++ -std=c++17 -Wall -Wextra solid_s10.cpp -o solid.exe
if %ERRORLEVEL% EQU 0 (
    echo [EXITO] Compilacion exitosa. Ejecutando solid.exe:
    echo --------------------------------------------------------------------
    solid.exe
) else (
    echo [ERROR] Fallo en la compilacion.
)
pause

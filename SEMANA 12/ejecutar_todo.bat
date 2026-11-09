@echo off
echo ======================================================================
echo SUITE COMPLETA DE PRUEBAS - SEMANA 12 (GoF: Observer, Strategy, MVC)
echo SIS206 - Programacion Orientada a Objetos II ^| UNAP Puno
echo Docente: Dr. Aldo Hernan Zanabria Galvez
echo ======================================================================

echo.
echo [PASO 1] Ejecutando Actividad 1A (Python 3.12/3.14 - Observer)...
python actividad1_demo.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo en actividad1_demo.py
    exit /b %ERRORLEVEL%
)

echo.
echo [PASO 2] Ejecutando Actividad 2A (Python 3.12/3.14 - Strategy)...
python actividad2_demo.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo en actividad2_demo.py
    exit /b %ERRORLEVEL%
)

echo.
echo [PASO 3] Ejecutando Actividad 3A (Python 3.12/3.14 - MVC Completo)...
python main_mvc.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo en main_mvc.py
    exit /b %ERRORLEVEL%
)

echo.
echo [PASO 4] Ejecutando Pruebas Automatizadas con Pytest...
python -m pytest tests -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo en pruebas pytest
    exit /b %ERRORLEVEL%
)

echo.
echo [PASO 5] Compilando y ejecutando suite completa en C++17...
call cpp\compilar_todo.bat

echo.
echo ======================================================================
echo [EXITO TOTAL] TODAS LAS ACTIVIDADES Y PRUEBAS FINALIZARON AL 100%%
echo ======================================================================

@echo off
chcp 65001 > nul
cd /d "%~dp0"
cls
echo ===============================================================================
echo UNIVERSIDAD NACIONAL DEL ALTIPLANO - PUNO
echo SIS206 - Programacion Orientada a Objetos II
echo Practica Semana 14: GUI con Tkinter y PyQt5 - MVC para el Sistema Academico
echo ===============================================================================
echo.

echo [1/2] Ejecutando Suite de Pruebas Unitarias (Tkinter, PyQt5, MVC)...
python -m unittest tests/test_practica14.py
if errorlevel 1 goto error

echo.
echo [2/2] Ejecutando Demostracion de Operaciones y Flujo MVC...
python demo_ejecucion.py
if errorlevel 1 goto error

echo.
echo ===============================================================================
echo EXITO: Todas las actividades y pruebas de la Semana 14 finalizaron correctamente.
echo ===============================================================================
echo.
echo Para abrir la aplicacion grafica:
echo   - Tkinter: python app_tkinter.py
echo   - PyQt5:   python pyqt5_app.py
echo.
pause
goto end

:error
echo.
echo ###############################################################################
echo Ocurrio un error durante la ejecucion de la practica.
echo ###############################################################################
echo.
pause
exit /b 1

:end

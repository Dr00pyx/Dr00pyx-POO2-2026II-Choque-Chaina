@echo off
chcp 65001 > nul
cd /d "%~dp0"
cls
echo ===============================================================================
echo UNIVERSIDAD NACIONAL DEL ALTIPLANO - PUNO
echo SIS206 - Programacion Orientada a Objetos II
echo Practica Semana 13: Persistencia Multicapa (JSON, CSV, SQLite)
echo ===============================================================================
echo.

echo [1/5] Ejecutando Actividad 1A: RepositorioJSON...
python actividad1_demo.py
if errorlevel 1 goto error

echo.
echo [2/5] Ejecutando Pruebas de Persistencia JSON...
python test_json_persistencia.py
if errorlevel 1 goto error

echo.
echo [3/5] Ejecutando Actividad 2A: RepositorioCSV...
python actividad2_demo.py
if errorlevel 1 goto error

echo.
echo [4/5] Ejecutando Actividad 3A: RepositorioSQLite y Sustitucion LSP...
python actividad3_demo.py
if errorlevel 1 goto error

echo.
echo [5/5] Ejecutando Suite Pytest de Sustitucion Polimorfica (LSP)...
python -m pytest test_repos.py -v
if errorlevel 1 goto error

echo.
echo ===============================================================================
echo EXITO: Todas las actividades y pruebas de la Semana 13 finalizaron correctamente.
echo ===============================================================================
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

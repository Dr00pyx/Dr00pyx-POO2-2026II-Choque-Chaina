@echo off
chcp 65001 > nul
echo =====================================================================
echo    EJECUCION DE ARCHIVOS PYTHON - SEMANA 6 (POO II - UNAP PUNO)
echo =====================================================================

cd /d "C:\Users\MELVIN\.gemini\antigravity\scratch\semana6"

echo.
echo [1/5] Verificacion de tipos estaticos con mypy...
python -m mypy repositorio.py actividad2_main.py actividad3_python.py proyecto_integrador.py

echo.
echo [2/5] Ejecutando Actividad 2 (Repositorio Python y consultas de dominio)...
python actividad2_main.py

echo.
echo [3/5] Ejecutando Actividad 3 (Ventana deslizante, Cola FIFO y Benchmark popleft)...
python actividad3_python.py

echo.
echo [4/5] Ejecutando Actividad 5 (Proyecto Integrador Python)...
python proyecto_integrador.py

echo.
echo [5/5] Ejecutando suite de pruebas automatizadas con pytest...
python -m pytest -v test_proyecto.py

echo.
echo =====================================================================
echo    TODAS LAS ACTIVIDADES PYTHON SE COMPLETARON EXITOSAMENTE
echo =====================================================================
pause

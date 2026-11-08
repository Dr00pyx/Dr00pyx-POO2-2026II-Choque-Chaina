@echo off
echo ====================================================================
echo   Ejecutando solid_s10.py en Python...
echo ====================================================================
python solid_s10.py
echo.
echo ====================================================================
echo   Ejecutando Pruebas Unitarias test_solid.py...
echo ====================================================================
python -m unittest test_solid.py
pause

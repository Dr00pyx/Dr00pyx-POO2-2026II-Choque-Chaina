# compilar_todo.ps1 — Compilacion y ejecucion integral de la Semana 09
$ErrorActionPreference = "Stop"

Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "    SIS206 - POO II | SEMANA 09: COMPILACION Y EJECUCION COMPLETA" -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Compilar C++17
Write-Host "`n[1/3] Compilando C++17 (Actividad 2A)..." -ForegroundColor Yellow
$cppDir = Join-Path $baseDir "s09\cpp"
Set-Location $cppDir
Write-Host "Ejecutando: g++ -std=c++17 main.cpp -o main.exe"
g++ -std=c++17 main.cpp -o main.exe
Write-Host "Compilacion exitosa. Ejecutando main.exe:" -ForegroundColor Green
& ".\main.exe"

# 2. Ejecutar Python 3 y pytest
Write-Host "`n[2/3] Ejecutando Python (Actividad 2B)..." -ForegroundColor Yellow
$pyDir = Join-Path $baseDir "s09\python"
Set-Location $pyDir
Write-Host "Ejecutando: python estudiante.py"
python estudiante.py
Write-Host "`nEjecutando suite de pruebas unitarias con pytest:" -ForegroundColor Yellow
python -m pytest test_estudiante.py --rootdir="$pyDir" -o cache_dir="$pyDir\.pytest_cache" -v

# 3. Generar Diagrama PlantUML PNG
Write-Host "`n[3/3] Renderizando Diagrama de Arquitectura (Actividad 3A)..." -ForegroundColor Yellow
$umlDir = Join-Path $baseDir "s09\plantuml"
Set-Location $umlDir
powershell -ExecutionPolicy Bypass -File render_diagram.ps1

Set-Location $baseDir
Write-Host "`n=======================================================================" -ForegroundColor Cyan
Write-Host "    TODO COMPILADO Y EJECUTADO CON EXITO (SEMANA 09)" -ForegroundColor Green
Write-Host "=======================================================================" -ForegroundColor Cyan

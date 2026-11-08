# render_diagram.ps1 - Genera el diagrama de arquitectura en PNG usando System.Drawing (GDI+)
Add-Type -AssemblyName System.Drawing

$width = 1150
$height = 980
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

# Fondo blanco
$bgBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$g.FillRectangle($bgBrush, 0, 0, $width, $height)

# Fuentes
$fontTitle = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
$fontPkg = New-Object System.Drawing.Font("Arial", 11, [System.Drawing.FontStyle]::Bold)
$fontComp = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
$fontNote = New-Object System.Drawing.Font("Consolas", 8, [System.Drawing.FontStyle]::Regular)
$fontLabel = New-Object System.Drawing.Font("Arial", 9, [System.Drawing.FontStyle]::Italic)

# Lapices y Pinceles
$blackPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(40, 40, 40), 1.5)
$dashPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(60, 60, 60), 1.5)
$dashPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
$textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(30, 30, 30))
$noteBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(254, 249, 219))
$notePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(200, 180, 100), 1)

# Funcion para dibujar caja de componente PlantUML
function Draw-Component($graphics, $text, $x, $y, $w, $h, $fillColor) {
    $brush = New-Object System.Drawing.SolidBrush($fillColor)
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(60, 60, 60), 1.5)
    $graphics.FillRectangle($brush, $x, $y, $w, $h)
    $graphics.DrawRectangle($pen, $x, $y, $w, $h)
    
    # Icono de componente UML
    $tabBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
    $graphics.FillRectangle($tabBrush, ($x + $w - 20), ($y + 6), 14, 10)
    $graphics.DrawRectangle($pen, ($x + $w - 20), ($y + 6), 14, 10)
    $graphics.FillRectangle($brush, ($x + $w - 22), ($y + 8), 5, 2)
    $graphics.DrawRectangle($pen, ($x + $w - 22), ($y + 8), 5, 2)
    $graphics.FillRectangle($brush, ($x + $w - 22), ($y + 12), 5, 2)
    $graphics.DrawRectangle($pen, ($x + $w - 22), ($y + 12), 5, 2)

    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $rect = New-Object System.Drawing.RectangleF($x, $y, $w, $h)
    $graphics.DrawString($text, $fontComp, $textBrush, $rect, $sf)
}

# Funcion para dibujar Interface UML (circulo)
function Draw-Interface($graphics, $text, $x, $y, $radius) {
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(40, 40, 40), 1.8)
    $brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
    $graphics.FillEllipse($brush, ($x - $radius), ($y - $radius), ($radius * 2), ($radius * 2))
    $graphics.DrawEllipse($pen, ($x - $radius), ($y - $radius), ($radius * 2), ($radius * 2))
    
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $rect = New-Object System.Drawing.RectangleF(($x - 100), ($y + $radius + 3), 200, 30)
    $graphics.DrawString($text, $fontComp, $textBrush, $rect, $sf)
}

# Titulo
$titleRect = New-Object System.Drawing.RectangleF(0, 20, $width, 35)
$sfTitle = New-Object System.Drawing.StringFormat
$sfTitle.Alignment = [System.Drawing.StringAlignment]::Center
$g.DrawString("Sistema Academico UNAP - Arquitectura Unidad II (Semana 09)", $fontTitle, $textBrush, $titleRect, $sfTitle)

# Subtitulo
$subRect = New-Object System.Drawing.RectangleF(0, 52, $width, 25)
$sfSub = New-Object System.Drawing.StringFormat
$sfSub.Alignment = [System.Drawing.StringAlignment]::Center
$g.DrawString("SIS206 POO II | Extension Actividad 3A con [NotificadorEmail] (Observer S12)", $fontLabel, $textBrush, $subRect, $sfSub)

# 1. Capa de Presentacion #D6E4F0
$pkgPresBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(214, 228, 240))
$pkgPresPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(91, 155, 213), 2)
$g.FillRectangle($pkgPresBrush, 50, 85, 1050, 140)
$g.DrawRectangle($pkgPresPen, 50, 85, 1050, 140)
$g.DrawString("Capa de Presentacion", $fontPkg, $textBrush, 65, 95)

Draw-Component $g "GUIEstudiante" 120 130 180 50 ([System.Drawing.Color]::FromArgb(245, 248, 252))
Draw-Component $g "GUICurso" 360 130 180 50 ([System.Drawing.Color]::FromArgb(245, 248, 252))

# Nota Presentacion
$g.FillRectangle($noteBrush, 620, 130, 170, 50)
$g.DrawRectangle($notePen, 620, 130, 170, 50)
$g.DrawString("Tkinter (S14)`nPyQt5 (S14)", $fontNote, $textBrush, 630, 138)

# 2. Capa de Servicios / Logica #E2EFDA
$pkgServBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(226, 239, 218))
$pkgServPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(112, 173, 71), 2)
$g.FillRectangle($pkgServBrush, 50, 275, 1050, 190)
$g.DrawRectangle($pkgServPen, 50, 275, 1050, 190)
$g.DrawString("Capa de Servicios / Logica", $fontPkg, $textBrush, 65, 285)

Draw-Component $g "ServicioEstudiante" 100 330 190 55 ([System.Drawing.Color]::FromArgb(248, 253, 245))
Draw-Component $g "ServicioMatricula" 340 330 180 55 ([System.Drawing.Color]::FromArgb(248, 253, 245))
Draw-Component $g "CalculadorPPA" 560 330 170 55 ([System.Drawing.Color]::FromArgb(248, 253, 245))

# Actividad 3A: NotificadorEmail agregado
Draw-Component $g "NotificadorEmail" 780 330 180 55 ([System.Drawing.Color]::FromArgb(255, 250, 205))

Draw-Interface $g "IEstrategiaCalculo" 645 430 12

# Nota Servicios
$g.FillRectangle($noteBrush, 980, 290, 110, 50)
$g.DrawRectangle($notePen, 980, 290, 110, 50)
$g.DrawString("SOLID (S10)`nGoF (S11-S12)", $fontNote, $textBrush, 985, 298)

# 3. Capa de Persistencia #FCE4D6
$pkgPersBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(252, 228, 214))
$pkgPersPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(237, 125, 49), 2)
$g.FillRectangle($pkgPersBrush, 50, 520, 680, 250)
$g.DrawRectangle($pkgPersPen, 50, 520, 680, 250)
$g.DrawString("Capa de Persistencia", $fontPkg, $textBrush, 65, 530)

Draw-Interface $g "IRepositorioEstudiante" 195 570 14

Draw-Component $g "RepositorioJSON" 80 680 170 55 ([System.Drawing.Color]::FromArgb(254, 246, 240))
Draw-Component $g "RepositorioSQLite" 280 680 180 55 ([System.Drawing.Color]::FromArgb(254, 246, 240))
Draw-Component $g "RepositorioSA" 490 680 170 55 ([System.Drawing.Color]::FromArgb(254, 246, 240))

# Nota Persistencia
$g.FillRectangle($noteBrush, 360, 540, 190, 65)
$g.DrawRectangle($notePen, 360, 540, 190, 65)
$g.DrawString("DIP (S10)`nRepository (S13)`nSQLAlchemy (S15)", $fontNote, $textBrush, 368, 548)

# 4. C++17 Motor #EAD1F5
$pkgMotorBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(234, 209, 245))
$pkgMotorPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(112, 48, 160), 2)
$g.FillRectangle($pkgMotorBrush, 770, 520, 330, 250)
$g.DrawRectangle($pkgMotorPen, 770, 520, 330, 250)
$g.DrawString("C++17 Motor", $fontPkg, $textBrush, 785, 530)

Draw-Component $g "libcalculo.so" 840 640 180 55 ([System.Drawing.Color]::FromArgb(250, 243, 253))

# Nota Motor
$g.FillRectangle($noteBrush, 850, 560, 160, 50)
$g.DrawRectangle($notePen, 850, 560, 160, 50)
$g.DrawString("extern C (S16)`nctypes (S16)", $fontNote, $textBrush, 858, 568)

# --- FLECHAS Y CONEXIONES ---
$arrowPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(30, 30, 30), 2)
$cap = New-Object System.Drawing.Drawing2D.AdjustableArrowCap(5, 5, $true)
$arrowPen.CustomEndCap = $cap

# GUI --> SVC
$g.DrawLine($arrowPen, 200, 180, 195, 330)

# GUICurso --> SVCM
$g.DrawLine($arrowPen, 440, 180, 440, 330)

# SVC --> REPO
$g.DrawLine($arrowPen, 195, 385, 195, 555)

# SVC --> CALC
$g.DrawLine($arrowPen, 290, 357, 560, 357)

# Actividad 3A: Flecha SVC --> NotificadorEmail : Observer (S12)
$observerPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(180, 40, 40), 2)
$observerPen.CustomEndCap = $cap
$g.DrawLine($observerPen, 250, 330, 250, 305)
$g.DrawLine($observerPen, 250, 305, 870, 305)
$g.DrawLine($observerPen, 870, 305, 870, 330)
$obsBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(180, 40, 40))
$g.DrawString("Observer (S12)", $fontLabel, $obsBrush, 500, 288)

# CALC .> IEST
$dashArrowPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(50, 50, 50), 1.8)
$dashArrowPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
$dashArrowPen.CustomEndCap = $cap
$g.DrawLine($dashArrowPen, 645, 385, 645, 417)

# CALC --> LIB : ctypes
$g.DrawLine($arrowPen, 700, 385, 860, 640)
$g.DrawString("ctypes", $fontLabel, $textBrush, 790, 490)

# REPO <|.. JSON, SQLITE, SA
$realizPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(50, 50, 50), 1.8)
$realizPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
$g.DrawLine($realizPen, 165, 680, 185, 600)
$g.DrawLine($realizPen, 370, 680, 210, 595)
$g.DrawLine($realizPen, 575, 680, 220, 590)

# Leyenda
$g.DrawRectangle($blackPen, 50, 830, 1050, 100)
$g.DrawString("Leyenda y Trazabilidad Curricular:", $fontPkg, $textBrush, 65, 840)
$g.DrawString("S09: Inicio Unidad II - Verificacion, clase Estudiante y Diagrama de Arquitectura.`nS10: Principios SOLID (SRP en Estudiante, DIP en Repositorio) | S11-S12: Patrones GoF (Observer en NotificadorEmail)`nS13: Patron Repository (JSON, SQLite) | S14: GUI Tkinter/PyQt5 | S15: ORM SQLAlchemy`nS16: Integracion C++ con Python via ctypes | S17: Pruebas automatizadas con pytest | S18: Entrega final", $fontComp, $textBrush, 65, 865)

# Guardar imagen en PNG
$output1 = "C:\Users\MELVIN\.gemini\antigravity\scratch\SEMANA 9\s09\plantuml\s09_arquitectura_apellido.png"
$output2 = "C:\Users\MELVIN\.gemini\antigravity\scratch\SEMANA 9\s09_arquitectura_apellido.png"
$bmp.Save($output1, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Save($output2, [System.Drawing.Imaging.ImageFormat]::Png)

$g.Dispose()
$bmp.Dispose()

Write-Host "Diagrama renderizado exitosamente en:"
Write-Host " - $output1"
Write-Host " - $output2"

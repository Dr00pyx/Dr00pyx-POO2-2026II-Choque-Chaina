# generate_svg.py
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1150 980" width="1150" height="980">
  <defs>
    <style>
      .title { font-family: 'Arial', sans-serif; font-size: 20px; font-weight: bold; fill: #1f2937; text-anchor: middle; }
      .subtitle { font-family: 'Arial', sans-serif; font-size: 13px; font-style: italic; fill: #4b5563; text-anchor: middle; }
      .pkg-title { font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold; fill: #111827; }
      .comp-text { font-family: 'Arial', sans-serif; font-size: 13px; font-weight: bold; fill: #1f2937; text-anchor: middle; }
      .note-text { font-family: 'Consolas', monospace; font-size: 11px; fill: #374151; }
      .label-text { font-family: 'Arial', sans-serif; font-size: 12px; font-style: italic; fill: #1f2937; }
      .legend-title { font-family: 'Arial', sans-serif; font-size: 13px; font-weight: bold; fill: #1f2937; }
      .legend-desc { font-family: 'Arial', sans-serif; font-size: 11px; fill: #374151; }
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#1f2937"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#b91c1c"/>
    </marker>
    <marker id="realize" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
      <polygon points="0,0 12,6 0,12" fill="#ffffff" stroke="#374151" stroke-width="1.5"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1150" height="980" fill="#ffffff"/>

  <!-- Titles -->
  <text x="575" y="42" class="title">Sistema Académico UNAP — Arquitectura Unidad II (Semana 09)</text>
  <text x="575" y="65" class="subtitle">SIS206 POO II | Extensión Actividad 3A con [NotificadorEmail] (Observer S12)</text>

  <!-- 1. Capa de Presentación -->
  <rect x="50" y="90" width="1050" height="140" rx="8" fill="#D6E4F0" stroke="#5B9BD5" stroke-width="2"/>
  <text x="70" y="118" class="pkg-title">Capa de Presentación</text>

  <!-- GUIEstudiante -->
  <g transform="translate(120, 135)">
    <rect width="180" height="50" rx="4" fill="#F8FAFC" stroke="#475569" stroke-width="1.5"/>
    <rect x="156" y="8" width="16" height="12" fill="#ffffff" stroke="#475569" stroke-width="1"/>
    <rect x="153" y="10" width="5" height="3" fill="#F8FAFC" stroke="#475569" stroke-width="1"/>
    <rect x="153" y="15" width="5" height="3" fill="#F8FAFC" stroke="#475569" stroke-width="1"/>
    <text x="80" y="30" class="comp-text">GUIEstudiante</text>
  </g>

  <!-- GUICurso -->
  <g transform="translate(360, 135)">
    <rect width="180" height="50" rx="4" fill="#F8FAFC" stroke="#475569" stroke-width="1.5"/>
    <rect x="156" y="8" width="16" height="12" fill="#ffffff" stroke="#475569" stroke-width="1"/>
    <rect x="153" y="10" width="5" height="3" fill="#F8FAFC" stroke="#475569" stroke-width="1"/>
    <rect x="153" y="15" width="5" height="3" fill="#F8FAFC" stroke="#475569" stroke-width="1"/>
    <text x="80" y="30" class="comp-text">GUICurso</text>
  </g>

  <!-- Note Presentation -->
  <g transform="translate(640, 135)">
    <path d="M 0 0 L 155 0 L 170 15 L 170 50 L 0 50 Z" fill="#FEF9DB" stroke="#D4AF37" stroke-width="1.2"/>
    <path d="M 155 0 L 155 15 L 170 15 Z" fill="#E6C875" stroke="#D4AF37" stroke-width="1.2"/>
    <text x="12" y="22" class="note-text">Tkinter (S14)</text>
    <text x="12" y="38" class="note-text">PyQt5 (S14)</text>
  </g>

  <!-- 2. Capa de Servicios / Lógica -->
  <rect x="50" y="275" width="1050" height="190" rx="8" fill="#E2EFDA" stroke="#70AD47" stroke-width="2"/>
  <text x="70" y="303" class="pkg-title">Capa de Servicios / Lógica</text>

  <!-- ServicioEstudiante -->
  <g transform="translate(90, 330)">
    <rect width="195" height="55" rx="4" fill="#F8FDF5" stroke="#475569" stroke-width="1.5"/>
    <rect x="170" y="8" width="16" height="12" fill="#ffffff" stroke="#475569" stroke-width="1"/>
    <rect x="167" y="10" width="5" height="3" fill="#F8FDF5" stroke="#475569" stroke-width="1"/>
    <rect x="167" y="15" width="5" height="3" fill="#F8FDF5" stroke="#475569" stroke-width="1"/>
    <text x="88" y="33" class="comp-text">ServicioEstudiante</text>
  </g>

  <!-- ServicioMatricula -->
  <g transform="translate(330, 330)">
    <rect width="180" height="55" rx="4" fill="#F8FDF5" stroke="#475569" stroke-width="1.5"/>
    <rect x="156" y="8" width="16" height="12" fill="#ffffff" stroke="#475569" stroke-width="1"/>
    <rect x="153" y="10" width="5" height="3" fill="#F8FDF5" stroke="#475569" stroke-width="1"/>
    <rect x="153" y="15" width="5" height="3" fill="#F8FDF5" stroke="#475569" stroke-width="1"/>
    <text x="80" y="33" class="comp-text">ServicioMatricula</text>
  </g>

  <!-- CalculadorPPA -->
  <g transform="translate(550, 330)">
    <rect width="170" height="55" rx="4" fill="#F8FDF5" stroke="#475569" stroke-width="1.5"/>
    <rect x="146" y="8" width="16" height="12" fill="#ffffff" stroke="#475569" stroke-width="1"/>
    <rect x="143" y="10" width="5" height="3" fill="#F8FDF5" stroke="#475569" stroke-width="1"/>
    <rect x="143" y="15" width="5" height="3" fill="#F8FDF5" stroke="#475569" stroke-width="1"/>
    <text x="75" y="33" class="comp-text">CalculadorPPA</text>
  </g>

  <!-- NotificadorEmail (Actividad 3A) -->
  <g transform="translate(760, 330)">
    <rect width="180" height="55" rx="4" fill="#FFFBEB" stroke="#B45309" stroke-width="2"/>
    <rect x="156" y="8" width="16" height="12" fill="#ffffff" stroke="#B45309" stroke-width="1"/>
    <rect x="153" y="10" width="5" height="3" fill="#FFFBEB" stroke="#B45309" stroke-width="1"/>
    <rect x="153" y="15" width="5" height="3" fill="#FFFBEB" stroke="#B45309" stroke-width="1"/>
    <text x="80" y="33" class="comp-text" fill="#92400E">NotificadorEmail</text>
  </g>

  <!-- Interface IEstrategiaCalculo -->
  <circle cx="635" cy="430" r="12" fill="#ffffff" stroke="#374151" stroke-width="2"/>
  <text x="635" y="456" class="comp-text" font-size="12px">IEstrategiaCalculo</text>

  <!-- Note Services -->
  <g transform="translate(980, 290)">
    <path d="M 0 0 L 95 0 L 110 15 L 110 50 L 0 50 Z" fill="#FEF9DB" stroke="#D4AF37" stroke-width="1.2"/>
    <path d="M 95 0 L 95 15 L 110 15 Z" fill="#E6C875" stroke="#D4AF37" stroke-width="1.2"/>
    <text x="10" y="22" class="note-text">SOLID (S10)</text>
    <text x="10" y="38" class="note-text">GoF (S11-S12)</text>
  </g>

  <!-- 3. Capa de Persistencia -->
  <rect x="50" y="520" width="680" height="260" rx="8" fill="#FCE4D6" stroke="#ED7D31" stroke-width="2"/>
  <text x="70" y="548" class="pkg-title">Capa de Persistencia</text>

  <!-- Interface IRepositorioEstudiante -->
  <circle cx="200" cy="580" r="14" fill="#ffffff" stroke="#374151" stroke-width="2"/>
  <text x="200" y="610" class="comp-text" font-size="12px">IRepositorioEstudiante</text>

  <!-- RepositorioJSON -->
  <g transform="translate(80, 690)">
    <rect width="170" height="55" rx="4" fill="#FEF6F0" stroke="#475569" stroke-width="1.5"/>
    <rect x="146" y="8" width="16" height="12" fill="#ffffff" stroke="#475569" stroke-width="1"/>
    <rect x="143" y="10" width="5" height="3" fill="#FEF6F0" stroke="#475569" stroke-width="1"/>
    <rect x="143" y="15" width="5" height="3" fill="#FEF6F0" stroke="#475569" stroke-width="1"/>
    <text x="75" y="33" class="comp-text">RepositorioJSON</text>
  </g>

  <!-- RepositorioSQLite -->
  <g transform="translate(290, 690)">
    <rect width="180" height="55" rx="4" fill="#FEF6F0" stroke="#475569" stroke-width="1.5"/>
    <rect x="156" y="8" width="16" height="12" fill="#ffffff" stroke="#475569" stroke-width="1"/>
    <rect x="153" y="10" width="5" height="3" fill="#FEF6F0" stroke="#475569" stroke-width="1"/>
    <rect x="153" y="15" width="5" height="3" fill="#FEF6F0" stroke="#475569" stroke-width="1"/>
    <text x="80" y="33" class="comp-text">RepositorioSQLite</text>
  </g>

  <!-- RepositorioSA -->
  <g transform="translate(510, 690)">
    <rect width="170" height="55" rx="4" fill="#FEF6F0" stroke="#475569" stroke-width="1.5"/>
    <rect x="146" y="8" width="16" height="12" fill="#ffffff" stroke="#475569" stroke-width="1"/>
    <rect x="143" y="10" width="5" height="3" fill="#FEF6F0" stroke="#475569" stroke-width="1"/>
    <rect x="143" y="15" width="5" height="3" fill="#FEF6F0" stroke="#475569" stroke-width="1"/>
    <text x="75" y="33" class="comp-text">RepositorioSA</text>
  </g>

  <!-- Note Persistence -->
  <g transform="translate(370, 540)">
    <path d="M 0 0 L 195 0 L 210 15 L 210 65 L 0 65 Z" fill="#FEF9DB" stroke="#D4AF37" stroke-width="1.2"/>
    <path d="M 195 0 L 195 15 L 210 15 Z" fill="#E6C875" stroke="#D4AF37" stroke-width="1.2"/>
    <text x="12" y="20" class="note-text">DIP (S10)</text>
    <text x="12" y="37" class="note-text">Repository (S13)</text>
    <text x="12" y="54" class="note-text">SQLAlchemy (S15)</text>
  </g>

  <!-- 4. C++17 Motor -->
  <rect x="760" y="520" width="340" height="260" rx="8" fill="#EAD1F5" stroke="#7030A0" stroke-width="2"/>
  <text x="780" y="548" class="pkg-title">C++17 Motor</text>

  <!-- libcalculo.so -->
  <g transform="translate(830, 650)">
    <rect width="200" height="55" rx="4" fill="#FAF3FD" stroke="#7030A0" stroke-width="1.5"/>
    <rect x="176" y="8" width="16" height="12" fill="#ffffff" stroke="#7030A0" stroke-width="1"/>
    <rect x="173" y="10" width="5" height="3" fill="#FAF3FD" stroke="#7030A0" stroke-width="1"/>
    <rect x="173" y="15" width="5" height="3" fill="#FAF3FD" stroke="#7030A0" stroke-width="1"/>
    <text x="92" y="33" class="comp-text">libcalculo.so</text>
  </g>

  <!-- Note Motor -->
  <g transform="translate(850, 560)">
    <path d="M 0 0 L 165 0 L 180 15 L 180 50 L 0 50 Z" fill="#FEF9DB" stroke="#D4AF37" stroke-width="1.2"/>
    <path d="M 165 0 L 165 15 L 180 15 Z" fill="#E6C875" stroke="#D4AF37" stroke-width="1.2"/>
    <text x="12" y="22" class="note-text">extern C (S16)</text>
    <text x="12" y="38" class="note-text">ctypes (S16)</text>
  </g>

  <!-- Connections / Arrows -->
  <!-- GUI --> SVC -->
  <line x1="200" y1="185" x2="195" y2="330" stroke="#1f2937" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- GUICurso --> SVCM -->
  <line x1="440" y1="185" x2="430" y2="330" stroke="#1f2937" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- SVC --> REPO -->
  <line x1="195" y1="385" x2="198" y2="564" stroke="#1f2937" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- SVC --> CALC -->
  <line x1="285" y1="357" x2="550" y2="357" stroke="#1f2937" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Actividad 3A: Flecha SVC --> NotificadorEmail : Observer (S12) -->
  <path d="M 240 330 L 240 305 L 850 305 L 850 330" fill="none" stroke="#b91c1c" stroke-width="2.2" marker-end="url(#arrow-red)"/>
  <rect x="475" y="293" width="145" height="22" rx="3" fill="#ffffff" stroke="#b91c1c" stroke-width="1"/>
  <text x="547" y="308" class="label-text" fill="#b91c1c" font-weight="bold" text-anchor="middle">Observer (S12)</text>

  <!-- CALC .> IEST -->
  <line x1="635" y1="385" x2="635" y2="416" stroke="#4b5563" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrow)"/>

  <!-- CALC --> LIB : ctypes -->
  <line x1="690" y1="385" x2="850" y2="650" stroke="#1f2937" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="785" y="500" class="label-text" font-weight="bold">ctypes</text>

  <!-- REPO <|.. JSON, SQLITE, SA -->
  <line x1="165" y1="690" x2="190" y2="600" stroke="#4b5563" stroke-width="1.8" stroke-dasharray="5,5" marker-end="url(#realize)"/>
  <line x1="380" y1="690" x2="215" y2="595" stroke="#4b5563" stroke-width="1.8" stroke-dasharray="5,5" marker-end="url(#realize)"/>
  <line x1="595" y1="690" x2="220" y2="588" stroke="#4b5563" stroke-width="1.8" stroke-dasharray="5,5" marker-end="url(#realize)"/>

  <!-- Legend Box -->
  <rect x="50" y="810" width="1050" height="135" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="70" y="835" class="legend-title">Leyenda y Trazabilidad Curricular — SIS206 POO II (Unidad II: S09 a S18):</text>
  <text x="70" y="860" class="legend-desc">• S09: Inicio Unidad II — Verificación del entorno, clase Estudiante encapsulada y Diagrama de Componentes inicial.</text>
  <text x="70" y="880" class="legend-desc">• S10: Principios SOLID — Refactorización con Responsabilidad Única (SRP) en Estudiante e Inversión de Dependencias (DIP) con IRepositorioEstudiante.</text>
  <text x="70" y="900" class="legend-desc">• S11-S12: Patrones de Diseño GoF — Patrón Estrategia (Strategy) en IEstrategiaCalculo y Patrón Observador (Observer) con NotificadorEmail.</text>
  <text x="70" y="920" class="legend-desc">• S13-S18: Patrón Repositorio (JSON/SQLite), GUI con Tkinter/PyQt5, ORM SQLAlchemy, Interoperabilidad C++/Python con ctypes y Testing con pytest.</text>
</svg>
"""

svg_path1 = r"C:\Users\MELVIN\.gemini\antigravity\scratch\SEMANA 9\s09\plantuml\s09_arquitectura_diagrama.svg"
svg_path2 = r"C:\Users\MELVIN\.gemini\antigravity\scratch\SEMANA 9\s09_arquitectura_diagrama.svg"

with open(svg_path1, "w", encoding="utf-8") as f:
    f.write(svg_content)
with open(svg_path2, "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Diagramas SVG guardados exitosamente.")

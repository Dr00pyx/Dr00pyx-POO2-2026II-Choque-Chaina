# Código monolítico defectuoso (Base para la Parte 2)

class GestorAcademicoMonolitico:
    def __init__(self):
        self.estudiantes = []  # Lista pública (Estado expuesto)

    def agregar_estudiante(self, codigo, nombre):
        self.estudiantes.append({"codigo": codigo, "nombre": nombre, "notas": []})
        # Auditoría acoplada directamente a un archivo de texto
        with open("auditoria.txt", "a", encoding="utf-8") as f:
            f.write(f"Estudiante agregado: {codigo} - {nombre}\n")

    def agregar_nota(self, codigo, nota):
        # Sin validación de rango de nota ([0, 20])
        for est in self.estudiantes:
            if est["codigo"] == codigo:
                est["notas"].append(nota)
                with open("auditoria.txt", "a", encoding="utf-8") as f:
                    f.write(f"Nota {nota} agregada a {codigo}\n")

    def generar_reporte(self):
        # Múltiples responsabilidades: cálculo + generación de archivo I/O
        with open("reporte.csv", "w", encoding="utf-8") as f:
            f.write("codigo,nombre,promedio,estado\n")
            for est in self.estudiantes:
                notas = est["notas"]
                promedio = sum(notas) / len(notas) if notas else 0.0
                estado = "APROBADO" if promedio >= 10.5 else "DESAPROBADO"
                f.write(f"{est['codigo']},{est['nombre']},{promedio:.2f},{estado}\n")
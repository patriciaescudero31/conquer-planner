import math
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk

from interfaz_componentes import *
from interfaz_datos import *
from interfaz_datos import _entero_no_negativo
from tareas import cargar_tareas
from planificador import calcular_carga_pendiente, generar_planificacion


class InicioMixin:
    def mostrar_inicio(self):
        limpiar(self.contenido)
        self.planificacion = cargar_planificacion()
        titulo(self.contenido, "Inicio", "Tu progreso real, la carga pendiente y el ritmo para llegar al objetivo.")

        grid = tk.Frame(self.contenido, bg=BG)
        grid.pack(fill="x")
        for col in range(4):
            grid.columnconfigure(col, weight=1)
        objetivo = obtener_fecha_objetivo(self.planificacion)
        cards = [
            ("Objetivo", objetivo.strftime("%d/%m/%Y"), f"{dias_restantes(self.planificacion)} días restantes", TEXT),
            ("Máster", f"{float(self.planificacion.get('porcentaje_master', 36)):.0f}%", "Progreso global editable", ACCENT),
            ("Inglés", f"{self.planificacion.get('porcentaje_ingles', 40):.0f}%", f"{self.planificacion.get('clases_ingles_completadas', 41)}/102 clases", ACCENT),
            ("Capacidad", f"{obtener_capacidad_hasta_objetivo(self.planificacion):.0f} h", "Horas disponibles hasta el objetivo", TEXT),
        ]
        for i, (a, b, c, color) in enumerate(cards):
            frame = tarjeta(grid, a, b, c, color)
            frame.grid(row=0, column=i, padx=(0 if i == 0 else 6, 0), sticky="nsew")
            frame.configure(height=120)

        master_restante = horas_master_restantes(self.planificacion)
        capacidad = obtener_capacidad_hasta_objetivo(self.planificacion)
        margen = capacidad - master_restante
        semanas = max(1, (dias_restantes(self.planificacion) + 6) // 7)
        ritmo_necesario = master_restante / semanas
        ritmo_disponible = obtener_horas_disponibles_semana(self.planificacion)
        color = SUCCESS if margen >= 20 else WARNING if margen >= 0 else DANGER
        diagnostico = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=22, pady=20)
        diagnostico.pack(fill="x", pady=18)
        tk.Label(diagnostico, text="DIAGNÓSTICO DE VIABILIDAD", font=(FONT_FAMILY, 10, "bold"), fg=MUTED, bg=CARD).pack(anchor="w")
        tk.Label(diagnostico, text=("Ritmo viable" if margen >= 20 else "Margen estrecho" if margen >= 0 else "Riesgo de retraso"), font=(FONT_FAMILY, 23, "bold"), fg=color, bg=CARD).pack(anchor="w", pady=(5, 2))
        tk.Label(diagnostico, text=f"Máster pendiente estimado: {master_restante:.1f} h · Capacidad restante: {capacidad:.1f} h · Margen: {margen:+.1f} h", font=(FONT_FAMILY, 12), fg=TEXT, bg=CARD).pack(anchor="w")
        tk.Label(
            diagnostico,
            text=(
                f"Ritmo mínimo: {ritmo_necesario:.1f} h/semana de máster · "
                f"Disponibilidad configurada: {ritmo_disponible:.1f} h/semana · "
                f"Quedan {semanas} semanas."
            ),
            font=(FONT_FAMILY, 10),
            fg=MUTED,
            bg=CARD,
        ).pack(anchor="w", pady=(6, 0))

        tk.Label(self.contenido, text="Siguiente acción", font=(FONT_FAMILY, 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(5, 10))
        self._mostrar_recomendacion(self.contenido)

        carga = calcular_carga_pendiente(CATALOGO, self.planificacion)
        tk.Label(
            self.contenido,
            text="Carga académica pendiente",
            font=(FONT_FAMILY, 18, "bold"),
            fg=TEXT,
            bg=BG,
        ).pack(anchor="w", pady=(22, 8))
        resumen_carga = " · ".join(
            f"{categoria}: {horas:.0f} h estimadas"
            for categoria, horas in carga.items()
        )
        tk.Label(
            self.contenido,
            text=(
                resumen_carga
                or "No quedan unidades pendientes en el temario."
            ),
            font=(FONT_FAMILY, 11),
            fg=MUTED,
            bg=BG,
            wraplength=900,
            justify="left",
        ).pack(anchor="w")

    def _mostrar_recomendacion(self, parent):
        master, ingles, bonus = obtener_pendientes_desbloqueados(self.planificacion)
        if master:
            item = master[0]
            titulo_accion = f"Máster · {item['nombre']}"
            detalle = item["pendiente"]
            nivel = "PRIORIDAD 1"
        elif ingles:
            item = ingles[0]
            titulo_accion = f"Inglés · {item['nombre']}"
            detalle = item["pendiente"]
            nivel = "PRIORIDAD 2"
        elif bonus:
            item = bonus[0]
            titulo_accion = f"Bonus · {item['nombre']}"
            detalle = item["pendiente"]
            nivel = "PRIORIDAD 3"
        else:
            titulo_accion = "Repaso / TFM"
            detalle = "No quedan contenidos desbloqueados pendientes en el catálogo."
            nivel = "MANTENIMIENTO"
        frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=20, pady=18)
        frame.pack(fill="x")
        tk.Label(frame, text=nivel, font=(FONT_FAMILY, 9, "bold"), fg=ACCENT_DARK, bg=SOFT_TEAL, padx=8, pady=4).pack(anchor="w")
        tk.Label(frame, text=titulo_accion, font=(FONT_FAMILY, 17, "bold"), fg=TEXT, bg=CARD).pack(anchor="w", pady=(10, 2))
        tk.Label(frame, text=detalle, font=(FONT_FAMILY, 12), fg=MUTED, bg=CARD).pack(anchor="w")

    def mostrar_plan_hoy(self):
        limpiar(self.contenido)
        self.planificacion = cargar_planificacion()
        hoy = date.today()
        dia = DIAS_SEMANA[hoy.weekday()]
        horas = max(0.0, float(self.planificacion.get("disponibilidad", {}).get(dia, 0) or 0))
        hechas = obtener_horas_registradas_dia(self.planificacion, hoy)
        restantes = max(0.0, horas - hechas)
        plan = generar_planificacion(
            CATALOGO,
            self.planificacion,
            hoy,
            cargar_tareas(ARCHIVO_TAREAS),
        )
        asignaciones = plan.get(hoy.isoformat(), [])
        titulo(self.contenido, "Plan de hoy", f"{dia} {hoy.strftime('%d/%m/%Y')} · el plan se genera con tus datos actuales")

        resumen = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=22, pady=20)
        resumen.pack(fill="x", pady=(0, 16))
        tk.Label(resumen, text=f"{restantes:.1f} h", font=(FONT_FAMILY, 32, "bold"), fg=ACCENT, bg=CARD).pack(anchor="w")
        tk.Label(resumen, text=f"de {horas:.1f} h disponibles hoy · {hechas:.1f} h ya registradas", font=(FONT_FAMILY, 11), fg=MUTED, bg=CARD).pack(anchor="w")

        tk.Label(
            self.contenido,
            text="Agenda de hoy",
            font=(FONT_FAMILY, 18, "bold"),
            fg=TEXT,
            bg=BG,
        ).pack(anchor="w", pady=(8, 8))
        if asignaciones:
            for numero, asignacion in enumerate(asignaciones, start=1):
                if asignacion["modulo"] == "Google Antigravity":
                    color = ACCENT_DARK
                elif asignacion["categoria"] == "Máster":
                    color = ACCENT
                elif asignacion["categoria"] == "Inglés":
                    color = "#60747b"
                elif asignacion["categoria"] == "Tarea":
                    color = ACCENT_DARK
                else:
                    color = WARNING
                self._fila_plan(
                    self.contenido,
                    str(numero),
                    asignacion["categoria"],
                    asignacion["modulo"],
                    " · ".join(asignacion["detalles"]),
                    asignacion["horas"],
                    color,
                )
        elif obtener_fecha_objetivo(self.planificacion) < hoy:
            tk.Label(
                self.contenido,
                text="La fecha objetivo ya ha pasado. Actualízala en Configuración para generar una nueva planificación.",
                font=(FONT_FAMILY, 11),
                fg=DANGER,
                bg=BG,
                wraplength=850,
                justify="left",
            ).pack(anchor="w", pady=8)
        elif restantes < 1:
            tk.Label(
                self.contenido,
                text="Ya has utilizado las horas disponibles de hoy.",
                font=(FONT_FAMILY, 11),
                fg=MUTED,
                bg=BG,
            ).pack(anchor="w", pady=8)
        else:
            tk.Label(
                self.contenido,
                text="No queda trabajo pendiente en el temario desbloqueado. Puedes registrar repaso, tutorías o trabajo del TFM.",
                font=(FONT_FAMILY, 11),
                fg=MUTED,
                bg=BG,
                wraplength=850,
                justify="left",
            ).pack(anchor="w", pady=8)

        tk.Label(self.contenido, text="Cómo se prioriza", font=(FONT_FAMILY, 17, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(22, 8))
        tk.Label(
            self.contenido,
            text="Las tareas manuales pendientes se programan primero, por prioridad Alta → Media → Baja. Cada una usa la estimación por tarea de Configuración; el tiempo restante se dedica al temario. Se mantienen la sesión semanal de Google Antigravity los miércoles, el inglés cuando cabe y los bonus después del contenido obligatorio.",
            font=(FONT_FAMILY, 11),
            fg=MUTED,
            bg=BG,
            wraplength=850,
            justify="left",
        ).pack(anchor="w")

    def _fila_plan(self, parent, numero, categoria, nombre, detalle, horas, color):
        frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=14)
        frame.pack(fill="x", pady=5)
        tk.Label(frame, text=numero, font=(FONT_FAMILY, 12, "bold"), fg="#ffffff", bg=color, width=3, pady=4).pack(side="left", padx=(0, 14))
        centro = tk.Frame(frame, bg=CARD)
        centro.pack(side="left", fill="x", expand=True)
        tk.Label(centro, text=categoria.upper(), font=(FONT_FAMILY, 9, "bold"), fg=color, bg=CARD).pack(anchor="w")
        tk.Label(centro, text=nombre, font=(FONT_FAMILY, 14, "bold"), fg=TEXT, bg=CARD).pack(anchor="w")
        tk.Label(centro, text=detalle, font=(FONT_FAMILY, 10), fg=MUTED, bg=CARD).pack(anchor="w")
        tk.Label(frame, text=f"{horas:.1f} h", font=(FONT_FAMILY, 16, "bold"), fg=TEXT, bg=CARD).pack(side="right")

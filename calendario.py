import calendar
import tkinter as tk
from collections import defaultdict
from datetime import date


MESES = (
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
)
DIAS = ("L", "M", "X", "J", "V", "S", "D")
BG = "#f8fafc"
CARD = "#ffffff"
TEXT = "#111827"
MUTED = "#64748b"
ACCENT = "#0d9488"
BORDER = "#e2e8f0"


class CalendarioAcademico:
    def __init__(self, parent, actividades=None, plan=None, fecha_objetivo=None):
        self.parent = parent
        self.actividades = actividades or []
        self.plan = plan or {}
        self.fecha_objetivo = fecha_objetivo
        self.fecha_inicio = date.today()
        hoy = date.today()
        self.ano = hoy.year
        self.mes = hoy.month
        self.seleccionada = hoy
        self.horas_por_fecha = defaultdict(float)
        self.actividades_por_fecha = defaultdict(list)

        for actividad in self.actividades:
            try:
                fecha = date.fromisoformat(actividad.get("fecha", ""))
                horas = float(actividad.get("horas", 0) or 0)
            except (TypeError, ValueError):
                continue
            self.horas_por_fecha[fecha] += max(0.0, horas)
            self.actividades_por_fecha[fecha].append(actividad)

        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="x", pady=20)
        tk.Label(
            self.frame,
            text="El calendario combina el plan previsto con tus sesiones reales.",
            font=("Helvetica", 10),
            fg=MUTED,
            bg=BG,
        ).pack(anchor="w", pady=(0, 10))

        cabecera = tk.Frame(self.frame, bg=BG)
        cabecera.pack(fill="x", pady=(0, 12))
        tk.Button(cabecera, text="‹", width=3, command=lambda: self._cambiar_mes(-1)).pack(side="left")
        self.titulo = tk.Label(
            cabecera,
            font=("Helvetica", 18, "bold"),
            fg=TEXT,
            bg=BG,
        )
        self.titulo.pack(side="left", expand=True)
        tk.Button(cabecera, text="›", width=3, command=lambda: self._cambiar_mes(1)).pack(side="right")

        self.grilla = tk.Frame(self.frame, bg=BG)
        self.grilla.pack(fill="x")
        self.detalle = tk.Frame(self.frame, bg=CARD, padx=14, pady=12)
        self.detalle.pack(fill="x", pady=(16, 0))
        self._dibujar_mes()

    def _cambiar_mes(self, cambio):
        indice = self.ano * 12 + self.mes - 1 + cambio
        nuevo_ano, mes_cero = divmod(indice, 12)
        nuevo_mes = mes_cero + 1
        primer_dia = date(nuevo_ano, nuevo_mes, 1)
        if (
            self.fecha_objetivo is not None
            and primer_dia > self.fecha_objetivo.replace(day=1)
        ):
            return
        if (nuevo_ano, nuevo_mes) < (self.fecha_inicio.year, self.fecha_inicio.month):
            return
        self.ano = nuevo_ano
        self.mes = nuevo_mes
        self.seleccionada = date(self.ano, self.mes, 1)
        if (self.ano, self.mes) == (self.fecha_inicio.year, self.fecha_inicio.month):
            self.seleccionada = self.fecha_inicio
        self._dibujar_mes()

    def _dibujar_mes(self):
        self.titulo.config(text=f"{MESES[self.mes - 1]} {self.ano}")
        for widget in self.grilla.winfo_children():
            widget.destroy()
        for columna, nombre_dia in enumerate(DIAS):
            self.grilla.columnconfigure(columna, weight=1)
            tk.Label(
                self.grilla,
                text=nombre_dia,
                font=("Helvetica", 9, "bold"),
                fg=MUTED,
                bg=BG,
            ).grid(row=0, column=columna, sticky="nsew", padx=2, pady=3)

        semanas = calendar.Calendar(firstweekday=0).monthdayscalendar(self.ano, self.mes)
        for fila, semana in enumerate(semanas, start=1):
            for columna, numero_dia in enumerate(semana):
                if numero_dia == 0:
                    tk.Label(self.grilla, text="", bg=BG).grid(
                        row=fila, column=columna, sticky="nsew", padx=2, pady=2
                    )
                    continue
                fecha = date(self.ano, self.mes, numero_dia)
                total_horas = self.horas_por_fecha.get(fecha, 0.0)
                plan_dia = self.plan.get(fecha.isoformat(), [])
                horas_planificadas = sum(item.get("horas", 0) for item in plan_dia)
                en_periodo = (
                    fecha >= self.fecha_inicio
                    and (self.fecha_objetivo is None or fecha <= self.fecha_objetivo)
                )
                texto = str(numero_dia)
                if en_periodo and horas_planificadas:
                    texto += f"\nPlan {horas_planificadas:g} h"
                if total_horas:
                    texto += f"\nReal {total_horas:g} h"
                color_fondo = ACCENT if fecha == self.seleccionada else CARD
                color_texto = "#ffffff" if fecha == self.seleccionada else TEXT
                if fecha == date.today() and fecha != self.seleccionada:
                    color_fondo = "#ccfbf1"
                if not en_periodo and fecha != date.today():
                    color_texto = "#cbd5e1"
                tk.Button(
                    self.grilla,
                    text=texto,
                    command=lambda dia=fecha: self._seleccionar(dia),
                    font=("Helvetica", 10, "bold" if fecha == date.today() else "normal"),
                    fg=color_texto,
                    bg=color_fondo,
                    activebackground=ACCENT,
                    activeforeground="#ffffff",
                    relief="flat",
                    height=3,
                    wraplength=70,
                ).grid(row=fila, column=columna, sticky="nsew", padx=2, pady=2)
        self._mostrar_detalle()

    def _seleccionar(self, fecha):
        self.seleccionada = fecha
        self._dibujar_mes()

    def _mostrar_detalle(self):
        for widget in self.detalle.winfo_children():
            widget.destroy()
        fecha_texto = self.seleccionada.strftime("%d/%m/%Y")
        tk.Label(
            self.detalle,
            text=f"Sesiones del {fecha_texto}",
            font=("Helvetica", 12, "bold"),
            fg=TEXT,
            bg=CARD,
        ).pack(anchor="w")
        actividades = self.actividades_por_fecha.get(self.seleccionada, [])
        plan_dia = self.plan.get(self.seleccionada.isoformat(), [])
        if plan_dia:
            tk.Label(
                self.detalle,
                text="Plan previsto",
                font=("Helvetica", 10, "bold"),
                fg=ACCENT,
                bg=CARD,
            ).pack(anchor="w", pady=(7, 0))
            for asignacion in plan_dia:
                tk.Label(
                    self.detalle,
                    text=(
                        f"{asignacion.get('horas', 0):g} h · "
                        f"{asignacion.get('modulo', '')} · "
                        f"{', '.join(asignacion.get('detalles', []))}"
                    ),
                    font=("Helvetica", 10),
                    fg=TEXT,
                    bg=CARD,
                    anchor="w",
                ).pack(anchor="w", pady=(3, 0))
        if not actividades:
            tk.Label(
                self.detalle,
                text="No hay sesiones reales registradas para este día.",
                font=("Helvetica", 10),
                fg=MUTED,
                bg=CARD,
            ).pack(anchor="w", pady=(5, 0))
            return
        for actividad in actividades:
            modulo = actividad.get("modulo", "").strip() or "Sin módulo"
            texto = (
                f"{actividad.get('horas', 0)} h · "
                f"{actividad.get('tipo', 'Estudio')} · "
                f"{actividad.get('actividad', 'Estudio')} · {modulo}"
            )
            tk.Label(
                self.detalle,
                text=texto,
                font=("Helvetica", 10),
                fg=TEXT,
                bg=CARD,
                anchor="w",
            ).pack(anchor="w", pady=(5, 0))

import math
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk

from interfaz_componentes import *
from interfaz_datos import *
from interfaz_datos import _entero_no_negativo
from calendario import CalendarioAcademico
from estadisticas import horas_por_modulo, horas_totales, horas_ultima_semana
from copias_seguridad import (
    ErrorCopiaSeguridad,
    listar_copias,
    restaurar_copia,
)
from planificador import calcular_carga_pendiente, generar_planificacion
from tareas import cargar_tareas


class OtrasVistasMixin:
    def mostrar_progreso(self):
        limpiar(self.contenido)
        self.planificacion = cargar_planificacion()
        titulo(self.contenido, "Progreso", "Una lectura clara de lo que has hecho, lo que queda y el tiempo disponible.")
        grid = tk.Frame(self.contenido, bg=BG)
        grid.pack(fill="x")
        for c in range(3):
            grid.columnconfigure(c, weight=1)
        valores = [
            ("Máster", f"{float(self.planificacion.get('porcentaje_master', 36)):.0f}%", "Progreso global", ACCENT),
            ("Inglés", f"{self.planificacion.get('porcentaje_ingles', 40):.0f}%", f"{self.planificacion.get('clases_ingles_completadas', 41)}/102 clases", ACCENT),
            ("Horas registradas", f"{obtener_horas_realizadas_totales(self.planificacion):.1f} h", "Sesiones guardadas", TEXT),
        ]
        for i, item in enumerate(valores):
            f = tarjeta(grid, *item)
            f.grid(row=0, column=i, padx=(0 if i == 0 else 6, 0), sticky="nsew")
            f.configure(height=120)

        tk.Label(self.contenido, text="Hitos actuales", font=(FONT_FAMILY, 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(22, 8))
        clases_ingles = self.planificacion["clases_ingles_completadas"]
        progreso_antigravity = self.planificacion["progreso_tema"].get(
            "MÁSTER · PREWORK|Google Antigravity", {}
        )
        clases_antigravity = min(
            10, _entero_no_negativo(progreso_antigravity.get("clases", 0))
        )
        apuntes_antigravity = self.planificacion["detalle_modulo"]["Google Antigravity"]["apuntes"]
        html = self.planificacion["detalle_modulo"]["HTML"]
        hitos = [
            (
                "Inglés",
                "Unidad 12 completada" if clases_ingles >= 41 else f"{clases_ingles}/41 clases hasta completar la unidad 12",
                SUCCESS if clases_ingles >= 41 else WARNING,
            ),
            ("Creación de agentes", "Apuntes terminados", SUCCESS),
            (
                "Google Antigravity",
                f"Clases {clases_antigravity}/10 · apuntes {apuntes_antigravity}/10",
                SUCCESS if clases_antigravity >= 10 and apuntes_antigravity >= 10 else WARNING,
            ),
            (
                "HTML",
                f"Tema 1: {html['tema_1']}/7 · Tema 2: {html['tema_2']}/6",
                ACCENT,
            ),
        ]
        for nombre, detalle, color in hitos:
            fila = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=11)
            fila.pack(fill="x", pady=3)
            tk.Label(fila, text="●", font=(FONT_FAMILY, 12), fg=color, bg=CARD).pack(side="left", padx=(0, 9))
            tk.Label(fila, text=nombre, font=(FONT_FAMILY, 11, "bold"), fg=TEXT, bg=CARD, width=22, anchor="w").pack(side="left")
            tk.Label(fila, text=detalle, font=(FONT_FAMILY, 10), fg=MUTED, bg=CARD, anchor="w").pack(side="left", fill="x", expand=True)

        objetivo = obtener_fecha_objetivo(self.planificacion)
        capacidad = obtener_capacidad_hasta_objetivo(self.planificacion)
        restante = horas_master_restantes(self.planificacion)
        tk.Label(self.contenido, text="Viabilidad hasta el objetivo", font=(FONT_FAMILY, 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(22, 8))
        frame = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=18)
        frame.pack(fill="x")
        tk.Label(frame, text=f"Te quedan {restante:.1f} h estimadas de máster hasta el {objetivo.strftime('%d/%m/%Y')}. La capacidad disponible configurada es de {capacidad:.1f} h.", font=(FONT_FAMILY, 12), fg=TEXT, bg=CARD, wraplength=900, justify="left").pack(anchor="w")

    def mostrar_configuracion(self):
        limpiar(self.contenido)
        self.planificacion = cargar_planificacion()
        titulo(self.contenido, "Configuración", "Aquí puedes corregir los datos globales sin abrir VS Code.")
        frame = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=20, pady=20)
        frame.pack(fill="x")
        campos = {}
        definiciones = [
            ("Fecha objetivo", "fecha_objetivo", self.planificacion.get("fecha_objetivo", "31/03/2027")),
            ("Progreso global del máster (%)", "porcentaje_master", str(self.planificacion.get("porcentaje_master", 36))),
            ("Horas estimadas del máster", "horas_estimadas", str(self.planificacion.get("horas_estimadas", 500))),
            ("Clases de inglés completadas", "clases_ingles_completadas", str(self.planificacion.get("clases_ingles_completadas", 41))),
            ("Estimación por clase (h)", "estimacion_clase", str(self.planificacion["estimaciones"]["clase"])),
            ("Estimación por apuntes (h)", "estimacion_apuntes", str(self.planificacion["estimaciones"]["apuntes"])),
            ("Estimación por clase + apuntes (h)", "estimacion_clase_apuntes", str(self.planificacion["estimaciones"]["clase_apuntes"])),
            ("Estimación por tarea (h)", "estimacion_tarea", str(self.planificacion["estimaciones"]["tarea"])),
            ("Estimación por evaluación (h)", "estimacion_evaluacion", str(self.planificacion["estimaciones"]["evaluacion"])),
            ("Estimación por tutoría (h)", "estimacion_tutoria", str(self.planificacion["estimaciones"]["tutoria"])),
            ("Estimación por clase en directo (h)", "estimacion_clase_directo", str(self.planificacion["estimaciones"]["clase_directo"])),
            ("Estimación por práctica (h)", "estimacion_practica", str(self.planificacion["estimaciones"]["practica"])),
            ("Estimación por TFM (h)", "estimacion_tfm", str(self.planificacion["estimaciones"]["tfm"])),
        ]
        for fila, (etiqueta, clave, valor) in enumerate(definiciones):
            tk.Label(frame, text=etiqueta, font=(FONT_FAMILY, 10, "bold"), fg=TEXT, bg=CARD).grid(row=fila, column=0, sticky="w", pady=7)
            entrada = ttk.Entry(frame, width=20)
            entrada.insert(0, valor)
            entrada.grid(row=fila, column=1, sticky="w", padx=18, pady=7)
            campos[clave] = entrada
        boton(frame, "Guardar configuración", lambda: self._guardar_configuracion(campos), True).grid(row=len(definiciones), column=1, sticky="w", pady=(12, 0))

        info = tk.Frame(self.contenido, bg=SOFT_AMBER, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=15)
        info.pack(fill="x", pady=18)
        tk.Label(info, text="Cómo se genera la planificación", font=(FONT_FAMILY, 13, "bold"), fg=TEXT, bg=SOFT_AMBER).pack(anchor="w")
        tk.Label(info, text="• Cada tipo de actividad tiene su estimación editable. Al registrar una sesión, el campo de horas se rellena con la estimación del tipo elegido.\n• Los tiempos reales de las últimas cinco sesiones del mismo módulo y tipo ajustan automáticamente la previsión de las actividades del temario.\n• El plan asigna primero las tareas manuales Alta → Media → Baja y reserva el tiempo disponible restante para el temario hasta la fecha objetivo.\n• El máster ocupa primero el tiempo académico; mientras siga pendiente, se planifica además una actividad diaria de inglés si cabe.\n• Registrar una clase, tarea o evaluación actualiza el progreso correspondiente; una clase de HTML también avanza su siguiente lección y un registro de TFM actualiza su tarea.\n• Antigravity se planifica los miércoles con la disponibilidad restante. Los bonus se planifican después del contenido obligatorio.\n• El porcentaje global del máster es una estimación manual; se recalcula el tiempo pendiente al cambiarlo.", font=(FONT_FAMILY, 10), fg=TEXT, bg=SOFT_AMBER, justify="left").pack(anchor="w", pady=(7, 0))

        self._mostrar_copias_seguridad()

    def _mostrar_copias_seguridad(self):
        copias = listar_copias()
        marco = tk.Frame(
            self.contenido,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=18,
            pady=16,
        )
        marco.pack(fill="x", pady=(0, 20))
        tk.Label(
            marco,
            text="Copias de seguridad",
            font=(FONT_FAMILY, 16, "bold"),
            fg=TEXT,
            bg=CARD,
        ).pack(anchor="w")
        tk.Label(
            marco,
            text=(
                "Se guarda automáticamente una copia antes de cada cambio "
                "en la planificación, las tareas o el temario. Se conservan "
                "las 30 más recientes en este Mac."
            ),
            font=(FONT_FAMILY, 10),
            fg=MUTED,
            bg=CARD,
            wraplength=850,
            justify="left",
        ).pack(anchor="w", pady=(4, 10))
        if not copias:
            tk.Label(
                marco,
                text="Aún no hay copias. Se creará la primera al guardar un cambio.",
                font=(FONT_FAMILY, 10),
                fg=MUTED,
                bg=CARD,
            ).pack(anchor="w")
            return
        identificadores = {}
        for copia in copias:
            try:
                fecha = datetime.fromisoformat(copia["fecha"])
                etiqueta = fecha.strftime("%d/%m/%Y %H:%M:%S")
            except ValueError:
                etiqueta = copia["id"]
            identificadores[etiqueta] = copia["id"]
        seleccion = ttk.Combobox(
            marco,
            values=list(identificadores),
            state="readonly",
        )
        seleccion.current(0)
        seleccion.pack(side="left", fill="x", expand=True, padx=(0, 12))
        boton(
            marco,
            "Restaurar copia",
            lambda: self._restaurar_copia(
                identificadores.get(seleccion.get(), "")
            ),
        ).pack(side="right")

    def _restaurar_copia(self, identificador):
        if not identificador:
            return
        confirmar = messagebox.askyesno(
            "Restaurar copia de seguridad",
            "Se reemplazarán tus archivos actuales de planificación, tareas "
            "y temario por los de la copia seleccionada. Antes se guardará "
            "otra copia del estado actual. ¿Quieres continuar?",
            parent=self.ventana,
        )
        if not confirmar:
            return
        try:
            restaurar_copia(identificador)
        except ErrorCopiaSeguridad as error:
            messagebox.showerror(
                "Restaurar copia",
                str(error),
                parent=self.ventana,
            )
            return
        self.planificacion = cargar_planificacion()
        aplicar_catalogo_local()
        messagebox.showinfo(
            "Restauración completada",
            "Se han restaurado los datos de la copia seleccionada.",
            parent=self.ventana,
        )
        self.mostrar_configuracion()

    def _guardar_configuracion(self, campos):
        try:
            fecha = datetime.strptime(campos["fecha_objetivo"].get().strip(), "%d/%m/%Y").date()
            master = float(campos["porcentaje_master"].get())
            horas = float(campos["horas_estimadas"].get())
            ingles = int(campos["clases_ingles_completadas"].get())
            tipos_estimacion = (
                "clase",
                "apuntes",
                "clase_apuntes",
                "tarea",
                "evaluacion",
                "tutoria",
                "clase_directo",
                "practica",
                "tfm",
            )
            estimaciones = {
                tipo: float(campos[f"estimacion_{tipo}"].get())
                for tipo in tipos_estimacion
            }
            if not (
                math.isfinite(master)
                and math.isfinite(horas)
                and                                 all(math.isfinite(valor) and valor > 0 for valor in estimaciones.values())
                and 0 <= master <= 100
                and horas >= 0
                and 0 <= ingles <= 102
            ):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Configuración",
                "Revisa la fecha, los porcentajes, las horas y las estimaciones (deben ser mayores que 0).",
            )
            return
        self.planificacion.update({"fecha_objetivo": fecha.strftime("%d/%m/%Y"), "porcentaje_master": master, "horas_estimadas": horas})
        self.planificacion["estimaciones"] = estimaciones
        establecer_clases_ingles(self.planificacion, ingles)
        if not self.guardar():
            self.planificacion = cargar_planificacion()
            return
        messagebox.showinfo("Guardado", "Configuración actualizada.")
        self.mostrar_inicio()

    def mostrar_calendario(self):
        limpiar(self.contenido)
        self.planificacion = cargar_planificacion()
        titulo(
            self.contenido,
            "Calendario",
            "Plan previsto y sesiones reales por día, hasta tu fecha objetivo.",
        )
        calendario = generar_planificacion(
            CATALOGO,
            self.planificacion,
            tareas=cargar_tareas(ARCHIVO_TAREAS),
        )
        CalendarioAcademico(
            self.contenido,
            self.planificacion.get("actividades_realizadas", []),
            calendario,
            obtener_fecha_objetivo(self.planificacion),
        )

    def mostrar_estadisticas(self):
        limpiar(self.contenido)
        self.planificacion = cargar_planificacion()

        titulo(self.contenido, "Estadísticas", "Resumen real de tu esfuerzo acumulado")

        actividades = self.planificacion.get("actividades_realizadas", [])
        total = horas_totales(actividades)
        semana = horas_ultima_semana(actividades)

        cards = [
            ("Horas totales", f"{total:.1f} h", "Desde el inicio"),
            ("Últimos 7 días", f"{semana:.1f} h", "Estudio reciente"),
            ("Sesiones", str(len(actividades)), "Registradas"),
        ]

        grid = tk.Frame(self.contenido, bg=BG)
        grid.pack(fill="x")
        for i in range(len(cards)):
            grid.columnconfigure(i, weight=1)

        for i, (titulo_card, valor, detalle) in enumerate(cards):
            frame = tarjeta(grid, titulo_card, valor, detalle, ACCENT)
            frame.grid(row=0, column=i, padx=6, sticky="nsew")
            frame.configure(height=120)

        tk.Label(self.contenido, text="Horas por módulo", font=(FONT_FAMILY, 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(25, 10))

        modulos = horas_por_modulo(actividades)
        if not modulos:
            tk.Label(self.contenido, text="Todavía no hay datos.", fg=MUTED, bg=BG).pack(anchor="w")
            return

        ordenados = sorted(modulos.items(), key=lambda x: x[1], reverse=True)
        for nombre, horas in ordenados:
            fila = tk.Frame(
                self.contenido,
                bg=CARD,
                highlightbackground=BORDER,
                highlightthickness=1,
                padx=14,
                pady=10,
            )
            fila.pack(fill="x", pady=3)
            tk.Label(fila, text=nombre, font=(FONT_FAMILY, 11, "bold"), bg=CARD, fg=TEXT).pack(side="left")
            tk.Label(fila, text=f"{horas:.1f} h", font=(FONT_FAMILY, 11), bg=CARD, fg=ACCENT).pack(side="right")

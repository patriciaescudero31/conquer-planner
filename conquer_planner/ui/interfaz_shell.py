import math
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk

from .interfaz_componentes import *
from .interfaz_datos import *
from .interfaz_datos import _entero_no_negativo


class ShellMixin:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Conquer Planner · Executive Academic Intelligence")
        self.ventana.geometry("1250x800")
        self.ventana.minsize(1000, 680)
        self.ventana.configure(bg=BG)
        self.planificacion = cargar_planificacion()
        aplicar_catalogo_local()
        self.pagina_actual = None
        self._configurar_estilos()
        self._construir_shell()

    def _configurar_estilos(self):
        style = ttk.Style(self.ventana)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure(
            "Title.TLabel",
            background=BG,
            foreground=TEXT,
            font=(FONT_FAMILY, 27, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=BG,
            foreground=MUTED,
            font=(FONT_FAMILY, 11),
        )
        style.configure(
            "TEntry",
            padding=8,
            fieldbackground=CARD,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
        )
        style.map(
            "TEntry",
            bordercolor=[("focus", ACCENT)],
            lightcolor=[("focus", ACCENT)],
            darkcolor=[("focus", ACCENT)],
        )
        style.configure(
            "TCombobox",
            padding=8,
            font=(FONT_FAMILY, 10),
            fieldbackground=CARD,
            background=CARD,
            foreground=TEXT,
            arrowcolor=ACCENT_DARK,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", CARD), ("disabled", BG)],
            foreground=[("readonly", TEXT), ("disabled", MUTED)],
            selectbackground=[("readonly", CARD)],
            selectforeground=[("readonly", TEXT)],
        )
        style.configure(
            "Treeview",
            background=CARD,
            fieldbackground=CARD,
            foreground=TEXT,
            bordercolor=BORDER,
            rowheight=30,
            font=(FONT_FAMILY, 10),
        )
        style.map(
            "Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", CARD)],
        )
        style.configure(
            "Treeview.Heading",
            background=BG,
            foreground=MUTED,
            relief="flat",
            font=(FONT_FAMILY, 9, "bold"),
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#e8f4f4")],
            foreground=[("active", TEXT)],
        )
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=BORDER,
            background=ACCENT,
            bordercolor=BORDER,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
        )

    def _construir_shell(self):
        self.sidebar = tk.Frame(self.ventana, bg=SIDEBAR, width=235)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = tk.Frame(self.sidebar, bg=SIDEBAR)
        logo.pack(fill="x", padx=22, pady=(28, 28))
        tk.Label(logo, text="CONQUER", font=(FONT_FAMILY, 18, "bold"), fg=CARD, bg=SIDEBAR).pack(anchor="w")
        tk.Label(logo, text="PLANNER", font=(FONT_FAMILY, 11, "bold"), fg="#62d4d0", bg=SIDEBAR).pack(anchor="w")
        tk.Label(logo, text="Executive Academic Intelligence", font=(FONT_FAMILY, 8), fg="#9aa9ad", bg=SIDEBAR).pack(anchor="w", pady=(5, 0))

        self.nav = tk.Frame(self.sidebar, bg=SIDEBAR)
        self.nav.pack(fill="x", padx=12)
        opciones = [
            ("⌂", "Inicio", self.mostrar_inicio),
            ("▣", "Plan de hoy", self.mostrar_plan_hoy),
            ("✓", "Tareas", self.mostrar_tareas),
            ("▤", "Temario", self.mostrar_temario),
            ("◷", "Planificación", self.mostrar_planificacion),
            ("◉", "Progreso", self.mostrar_progreso),
            ("📅", "Calendario", self.mostrar_calendario),
            ("📊", "Estadísticas", self.mostrar_estadisticas),
            ("⚙", "Configuración", self.mostrar_configuracion),

        ]
        self.nav_buttons = []
        self.nav_activo = None
        for icono, nombre, funcion in opciones:
            b = tk.Button(self.nav, text=f"  {icono}   {nombre}", command=lambda pagina=funcion: pagina(), anchor="w", font=(FONT_FAMILY, 10, "bold"), fg="#c3ced0", bg=SIDEBAR, activeforeground=CARD, activebackground="#1e3437", relief="flat", bd=0, padx=8, pady=10, cursor="hand2")
            b.pack(fill="x", pady=2)
            b.configure(
                command=lambda pagina=funcion, boton_nav=b: self._navegar(
                    pagina,
                    boton_nav,
                )
            )
            self.nav_buttons.append(b)
            if nombre == "Inicio":
                self.nav_activo = b
                b.configure(bg="#1e3437", fg=CARD)
            b.bind(
                "<Enter>",
                lambda _event, boton_nav=b: boton_nav.configure(
                    bg="#1b292d" if boton_nav is not self.nav_activo else "#1e3437"
                ),
            )
            b.bind(
                "<Leave>",
                lambda _event, boton_nav=b: boton_nav.configure(
                    bg="#1e3437" if boton_nav is self.nav_activo else SIDEBAR,
                    fg=CARD if boton_nav is self.nav_activo else "#c3ced0",
                ),
            )

        objetivo = obtener_fecha_objetivo(self.planificacion)
        pie = tk.Frame(self.sidebar, bg="#1b292d", padx=15, pady=14)
        pie.pack(side="bottom", fill="x", padx=12, pady=15)
        tk.Label(pie, text="OBJETIVO", font=(FONT_FAMILY, 8, "bold"), fg="#9aa9ad", bg="#1b292d").pack(anchor="w")
        tk.Label(pie, text=objetivo.strftime("%d/%m/%Y"), font=(FONT_FAMILY, 13, "bold"), fg=CARD, bg="#1b292d").pack(anchor="w", pady=(3, 0))
        tk.Label(pie, text=f"{dias_restantes(self.planificacion)} días restantes", font=(FONT_FAMILY, 9), fg="#62d4d0", bg="#1b292d").pack(anchor="w", pady=(2, 0))

        self.main = tk.Frame(self.ventana, bg=BG)
        self.main.pack(side="right", fill="both", expand=True)
        self.contenido = crear_scroll(self.main)
        self.mostrar_inicio()
        self.ventana.after_idle(self._revisar_disponibilidad_dominical)

    def _navegar(self, pagina, boton_activo):
        self.nav_activo = boton_activo
        for boton_nav in self.nav_buttons:
            seleccionado = boton_nav is boton_activo
            boton_nav.configure(
                bg="#1e3437" if seleccionado else SIDEBAR,
                fg=CARD if seleccionado else "#c3ced0",
            )
        pagina()

    def _revisar_disponibilidad_dominical(self):
        hoy = date.today()
        if hoy.weekday() == 6 and (
            self.planificacion.get("ultima_revision_disponibilidad")
            != hoy.isoformat()
        ):
            self._preguntar_disponibilidad_dominical(hoy)
        self._programar_revision_dominical(hoy)

    def _programar_revision_dominical(self, hoy):
        dias_hasta_domingo = (6 - hoy.weekday()) % 7 or 7
        proximo_domingo = hoy + timedelta(days=dias_hasta_domingo)
        proxima_revision = datetime.combine(
            proximo_domingo,
            datetime.min.time(),
        ).replace(hour=9)
        demora = max(
            1,
            int((proxima_revision - datetime.now()).total_seconds() * 1000),
        )
        self.ventana.after(
            demora,
            self._revisar_disponibilidad_dominical,
        )

    def _preguntar_disponibilidad_dominical(self, hoy):
        inicio = hoy + timedelta(days=1)
        fin = inicio + timedelta(days=6)
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Disponibilidad de la próxima semana")
        ventana.transient(self.ventana)
        ventana.resizable(False, False)
        ventana.configure(bg=BG)
        marco = tk.Frame(
            ventana,
            bg=CARD,
            padx=22,
            pady=20,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        marco.pack(fill="both", expand=True, padx=16, pady=16)
        tk.Label(
            marco,
            text="¿Cuántas horas tendrás para estudiar?",
            font=(FONT_FAMILY, 17, "bold"),
            fg=TEXT,
            bg=CARD,
        ).pack(anchor="w")
        tk.Label(
            marco,
            text=(
                f"Disponibilidad del {inicio.strftime('%d/%m')} "
                f"al {fin.strftime('%d/%m')}. Ajusta cada día y el plan "
                "se recalculará con este horario."
            ),
            font=(FONT_FAMILY, 10),
            fg=MUTED,
            bg=CARD,
            wraplength=420,
            justify="left",
        ).pack(anchor="w", pady=(5, 14))
        campos = {}
        formulario = tk.Frame(marco, bg=CARD)
        formulario.pack(fill="x")
        for indice, dia in enumerate(DIAS_SEMANA):
            fila, columna = divmod(indice, 4)
            celda = tk.Frame(formulario, bg=CARD)
            celda.grid(row=fila, column=columna, padx=5, pady=5, sticky="ew")
            tk.Label(
                celda,
                text=dia,
                font=(FONT_FAMILY, 9, "bold"),
                fg=TEXT,
                bg=CARD,
            ).pack(anchor="w")
            entrada = ttk.Entry(celda, width=8, justify="center")
            entrada.insert(
                0,
                str(self.planificacion["disponibilidad"].get(dia, 0)),
            )
            entrada.pack(fill="x", pady=(3, 0))
            campos[dia] = entrada
        for columna in range(4):
            formulario.columnconfigure(columna, weight=1)
        acciones = tk.Frame(marco, bg=CARD)
        acciones.pack(fill="x", pady=(14, 0))
        boton(acciones, "Ahora no", ventana.destroy).pack(side="right", padx=(8, 0))
        boton(
            acciones,
            "Guardar y recalcular",
            lambda: self._guardar_disponibilidad_dominical(
                campos,
                ventana,
                hoy,
            ),
            True,
        ).pack(side="right")
        ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)
        ventana.grab_set()
        ventana.focus_set()

    def _guardar_disponibilidad_dominical(self, campos, ventana, domingo):
        try:
            disponibilidad = {
                dia: float(entrada.get().strip())
                for dia, entrada in campos.items()
            }
            aplicar_disponibilidad_semanal(
                self.planificacion,
                disponibilidad,
                domingo,
            )
        except (TypeError, ValueError, OverflowError):
            messagebox.showerror(
                "Disponibilidad",
                "Introduce entre 0 y 24 horas para cada día.",
                parent=ventana,
            )
            return
        if not self.guardar():
            self.planificacion = cargar_planificacion()
            return
        ventana.destroy()
        self.mostrar_inicio()

    def refrescar(self, funcion=None):
        self.planificacion = cargar_planificacion()
        if funcion:
            funcion()

    def guardar(self):
        if not guardar_planificacion(self.planificacion):
            messagebox.showerror("Error", "No se han podido guardar los cambios.")
            return False
        return True

    def ejecutar(self):
        self.ventana.mainloop()

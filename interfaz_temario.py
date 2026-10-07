import math
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk

from interfaz_componentes import *
from interfaz_datos import *
from interfaz_datos import _entero_no_negativo


class TemarioMixin:
    def mostrar_temario(self):
        limpiar(self.contenido)
        self.planificacion = cargar_planificacion()
        titulo(self.contenido, "Temario", "Marca aquí lo que realmente has terminado. Los porcentajes se actualizan solos.")

        clases_ingles = self.planificacion["clases_ingles_completadas"]
        clases_antigravity = _entero_no_negativo(
            self.planificacion["progreso_tema"]
            .get("MÁSTER · PREWORK|Google Antigravity", {})
            .get("clases", 0)
        )
        apuntes_antigravity = self.planificacion["detalle_modulo"]["Google Antigravity"]["apuntes"]
        detalle_html = self.planificacion["detalle_modulo"]["HTML"]
        aviso = tk.Frame(self.contenido, bg=SOFT_TEAL, highlightbackground="#b5e7e4", highlightthickness=1, padx=18, pady=14)
        aviso.pack(fill="x", pady=(0, 18))
        tk.Label(aviso, text="ESTADO ACTUAL", font=(FONT_FAMILY, 9, "bold"), fg=ACCENT_DARK, bg=SOFT_TEAL).pack(anchor="w")
        unidad_12 = "Unidad 12 completada" if clases_ingles >= 41 else "Unidad 12 pendiente"
        tk.Label(
            aviso,
            text=(
                f"Inglés: {clases_ingles}/102 · {unidad_12} · "
                f"Google Antigravity: {clases_antigravity}/10 clases, "
                f"{apuntes_antigravity}/10 apuntes · "
                f"HTML: tema 1 {detalle_html['tema_1']}/7, "
                f"tema 2 {detalle_html['tema_2']}/6."
            ),
            font=(FONT_FAMILY, 11, "bold"),
            fg=TEXT,
            bg=SOFT_TEAL,
            wraplength=900,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

        for bloque, modulos in CATALOGO.items():
            cab = tk.Frame(self.contenido, bg=SIDEBAR, padx=15, pady=9)
            cab.pack(fill="x", pady=(12, 5))
            tk.Label(cab, text=bloque, font=(FONT_FAMILY, 13, "bold"), fg="#ffffff", bg=SIDEBAR).pack(anchor="w")
            for nombre, datos in modulos.items():
                self._fila_modulo(bloque, nombre, datos)

    def _fila_modulo(self, bloque, nombre, datos):
        clave = f"{bloque}|{nombre}"
        guardado = self.planificacion.get("progreso_tema", {}).get(clave, {})
        frame = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=12)
        frame.pack(fill="x", pady=3)
        progreso = progreso_modulo(self.planificacion, bloque, nombre, datos)
        estado = estado_modulo(self.planificacion, bloque, nombre, datos)
        color = SUCCESS if estado == "Completado" else ACCENT if estado == "En curso" else MUTED
        top = tk.Frame(frame, bg=CARD)
        top.pack(fill="x")
        tk.Label(top, text=nombre, font=(FONT_FAMILY, 12, "bold"), fg=TEXT, bg=CARD).pack(side="left")
        tk.Label(top, text=f"{estado} · {progreso:.0f}%", font=(FONT_FAMILY, 9, "bold"), fg=color, bg=CARD).pack(side="right")
        tk.Label(frame, text=f"{datos.get('clases', 0)} clases · {datos.get('tareas', 0)} tareas · {datos.get('evaluaciones', 0)} evaluaciones", font=(FONT_FAMILY, 9), fg=MUTED, bg=CARD).pack(anchor="w", pady=(3, 7))
        if nombre == "Google Antigravity":
            apuntes = self.planificacion["detalle_modulo"]["Google Antigravity"]["apuntes"]
            clases = _entero_no_negativo(guardado.get("clases", 0))
            estado_apuntes = "apuntes pendientes" if apuntes < 10 else "apuntes completados"
            tk.Label(
                frame,
                text=f"Clases: {clases}/10 · apuntes: {apuntes}/10 · {estado_apuntes}",
                font=(FONT_FAMILY, 9, "bold"),
                fg=WARNING if apuntes < 10 or clases < 10 else SUCCESS,
                bg=CARD,
            ).pack(anchor="w", pady=(0, 7))
        if nombre == "HTML":
            detalle = self.planificacion["detalle_modulo"]["HTML"]
            tk.Label(frame, text=f"Tema 1: {detalle.get('tema_1', 7)}/7 · Tema 2: {detalle.get('tema_2', 0)}/6", font=(FONT_FAMILY, 9, "bold"), fg=ACCENT, bg=CARD).pack(anchor="w", pady=(0, 7))
        barra = ttk.Progressbar(frame, style="Horizontal.TProgressbar", maximum=100, value=progreso)
        barra.pack(fill="x", pady=(0, 10))

        controles = tk.Frame(frame, bg=CARD)
        controles.pack(fill="x")
        entradas = {}
        for campo, etiqueta in (("clases", "Clases hechas"), ("tareas", "Tareas hechas"), ("evaluaciones", "Evaluaciones hechas")):
            total = int(datos.get(campo, 0) or 0)
            if not total:
                continue
            celda = tk.Frame(controles, bg=CARD)
            celda.pack(side="left", padx=(0, 16))
            tk.Label(celda, text=etiqueta, font=(FONT_FAMILY, 8), fg=MUTED, bg=CARD).pack(anchor="w")
            entrada = ttk.Entry(celda, width=7)
            entrada.insert(0, str(guardado.get(campo, 0)))
            entrada.pack()
            entradas[campo] = entrada
        if nombre == "HTML":
            detalle = self.planificacion.setdefault("detalle_modulo", {}).setdefault("HTML", {"tema_1": 7, "tema_2": 0})
            detalle_frame = tk.Frame(frame, bg=CARD)
            detalle_frame.pack(fill="x", pady=(8, 0))
            for campo, etiqueta, maximo in (("tema_1", "Tema 1 / 7", 7), ("tema_2", "Tema 2 / 6", 6)):
                celda = tk.Frame(detalle_frame, bg=CARD)
                celda.pack(side="left", padx=(0, 16))
                tk.Label(celda, text=etiqueta, font=(FONT_FAMILY, 8), fg=MUTED, bg=CARD).pack(anchor="w")
                entrada = ttk.Entry(celda, width=7)
                entrada.insert(0, str(detalle.get(campo, 0)))
                entrada.pack()
                entradas[campo] = entrada
        if nombre == "Google Antigravity":
            detalle = self.planificacion.setdefault("detalle_modulo", {}).setdefault("Google Antigravity", {"apuntes": 6})
            celda = tk.Frame(frame, bg=CARD)
            celda.pack(anchor="w", pady=(8, 0))
            tk.Label(celda, text="Apuntes hechos / 10", font=(FONT_FAMILY, 8), fg=MUTED, bg=CARD).pack(anchor="w")
            entrada = ttk.Entry(celda, width=7)
            entrada.insert(0, str(detalle.get("apuntes", 6)))
            entrada.pack()
            entradas["apuntes"] = entrada
        acciones = tk.Frame(frame, bg=CARD)
        acciones.pack(fill="x", pady=(8, 0))
        if nombre == "Google Antigravity":
            tk.Label(
                acciones,
                text="Clases y apuntes semanales fijos",
                font=(FONT_FAMILY, 9),
                fg=MUTED,
                bg=CARD,
            ).pack(side="left")
        else:
            boton(
                acciones,
                "Editar sección",
                lambda: self._editar_seccion(bloque, nombre, datos),
            ).pack(side="left")
        boton(
            acciones,
            "Guardar progreso",
            lambda: self._guardar_modulo(clave, entradas, datos),
        ).pack(side="right")

    def _editar_seccion(self, bloque, nombre, datos):
        ventana = tk.Toplevel(self.ventana)
        ventana.title(f"Editar {nombre}")
        ventana.geometry("460x390")
        ventana.resizable(False, False)
        ventana.configure(bg=BG)
        marco = tk.Frame(
            ventana,
            bg=CARD,
            padx=22,
            pady=22,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        marco.pack(fill="both", expand=True, padx=18, pady=18)
        tk.Label(
            marco,
            text=f"Editar sección · {nombre}",
            font=(FONT_FAMILY, 17, "bold"),
            fg=TEXT,
            bg=CARD,
        ).pack(anchor="w", pady=(0, 6))
        tk.Label(
            marco,
            text=bloque,
            font=(FONT_FAMILY, 10),
            fg=MUTED,
            bg=CARD,
        ).pack(anchor="w", pady=(0, 14))

        entradas = {}
        for campo, etiqueta in (
            ("clases", "Número total de clases"),
            ("tareas", "Número total de tareas"),
            ("evaluaciones", "Número total de evaluaciones"),
        ):
            tk.Label(
                marco,
                text=etiqueta,
                font=(FONT_FAMILY, 10, "bold"),
                fg=TEXT,
                bg=CARD,
            ).pack(anchor="w", pady=(7, 2))
            entrada = ttk.Entry(marco)
            entrada.insert(0, str(datos.get(campo, 0) or 0))
            entrada.pack(fill="x")
            entradas[campo] = entrada

        completada = tk.BooleanVar(
            value=estado_modulo(
                self.planificacion,
                bloque,
                nombre,
                datos,
            )
            == "Completado"
        )
        tk.Checkbutton(
            marco,
            text="Marcar como completada si no tiene actividades",
            variable=completada,
            font=(FONT_FAMILY, 10),
            fg=TEXT,
            bg=CARD,
            activebackground=CARD,
            selectcolor=CARD,
        ).pack(anchor="w", pady=(14, 4))

        def guardar():
            try:
                totales = {}
                for campo, entrada in entradas.items():
                    texto = entrada.get().strip()
                    valor = int(texto)
                    if valor < 0:
                        raise ValueError
                    totales[campo] = valor
            except ValueError:
                messagebox.showerror(
                    "Temario",
                    "Introduce números enteros iguales o mayores que cero.",
                    parent=ventana,
                )
                return

            datos.update(totales)
            if not any(totales.values()):
                datos["estado"] = (
                    "Completado" if completada.get() else "Pendiente"
                )
            else:
                datos.pop("estado", None)
            if not guardar_catalogo_local(bloque, nombre, datos):
                messagebox.showerror(
                    "Temario",
                    "No se han podido guardar los cambios del temario.",
                    parent=ventana,
                )
                return
            ventana.destroy()
            self.mostrar_temario()

        boton(marco, "Guardar cambios", guardar, True).pack(
            anchor="e",
            pady=(16, 0),
        )

    def _guardar_modulo(self, clave, entradas, datos):
        valores = {}
        bloque, nombre = clave.split("|", 1)
        especiales = {"tema_1": 7, "tema_2": 6, "apuntes": 10}
        for campo, entrada in entradas.items():
            try:
                valor = int(entrada.get())
                total = especiales.get(campo, int(datos.get(campo, 0) or 0))
                if valor < 0 or valor > total:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Progreso", "Introduce valores enteros dentro del total disponible.")
                return
            valores[campo] = valor
        especiales_guardados = {
            campo: valor for campo, valor in valores.items() if campo in especiales
        }
        valores_normales = {
            campo: valor for campo, valor in valores.items() if campo not in especiales
        }
        if especiales_guardados:
            detalle = self.planificacion.setdefault("detalle_modulo", {}).setdefault(nombre, {})
            detalle.update(especiales_guardados)
        if valores_normales:
            self.planificacion.setdefault("progreso_tema", {})[clave] = valores_normales
        if bloque == "INGLÉS":
            self.planificacion["clases_ingles_completadas"] = total_clases_ingles(
                self.planificacion
            )
        if not self.guardar():
            self.planificacion = cargar_planificacion()
            return
        self.mostrar_temario()

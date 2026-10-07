import math
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk

from interfaz_componentes import *
from interfaz_datos import *
from interfaz_datos import _entero_no_negativo
from tareas import cargar_tareas
from planificador import calcular_carga_pendiente, generar_planificacion


class PlanificacionMixin:
    def mostrar_planificacion(self):
        limpiar(self.contenido)
        self.planificacion = cargar_planificacion()
        titulo(self.contenido, "Planificación", "Capacidad, horas realizadas y previsión hasta tu fecha objetivo.")

        objetivo = obtener_fecha_objetivo(self.planificacion)
        capacidad = obtener_capacidad_hasta_objetivo(self.planificacion)
        restante = horas_master_restantes(self.planificacion)
        margen = capacidad - restante
        grid = tk.Frame(self.contenido, bg=BG)
        grid.pack(fill="x")
        for c in range(3):
            grid.columnconfigure(c, weight=1)
        datos = [
            (
                "Horas máster restantes",
                f"{restante:.1f} h",
                (
                    f"Basado en {self.planificacion['horas_estimadas']:g} h "
                    f"y {self.planificacion['porcentaje_master']:g}% completado"
                ),
                TEXT,
            ),
            ("Capacidad hasta objetivo", f"{capacidad:.1f} h", f"Hasta {objetivo.strftime('%d/%m/%Y')}", ACCENT),
            ("Margen", f"{margen:+.1f} h", "Capacidad menos máster pendiente", SUCCESS if margen >= 20 else WARNING if margen >= 0 else DANGER),
        ]
        for i, item in enumerate(datos):
            frame = tarjeta(grid, *item)
            frame.grid(row=0, column=i, padx=(0 if i == 0 else 6, 0), sticky="nsew")
            frame.configure(height=125)

        ritmo = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=18)
        ritmo.pack(fill="x", pady=18)
        semanas = max(1, (dias_restantes(self.planificacion) + 6) // 7)
        necesario = restante / semanas
        semanal = obtener_horas_disponibles_semana(self.planificacion)
        tk.Label(ritmo, text="RITMO NECESARIO", font=(FONT_FAMILY, 9, "bold"), fg=MUTED, bg=CARD).pack(anchor="w")
        tk.Label(ritmo, text=f"{necesario:.1f} h/semana de máster", font=(FONT_FAMILY, 21, "bold"), fg=TEXT, bg=CARD).pack(anchor="w", pady=(4, 2))
        tk.Label(ritmo, text=f"Disponibilidad semanal configurada: {semanal:.1f} h · {semanas} semanas aproximadas.", font=(FONT_FAMILY, 10), fg=MUTED, bg=CARD).pack(anchor="w")

        carga_proyectada = sum(
            calcular_carga_pendiente(
                CATALOGO,
                self.planificacion,
                incluir_bonuses_futuros=True,
            ).values()
        )
        tareas = cargar_tareas(ARCHIVO_TAREAS)
        tareas_pendientes = [
            tarea for tarea in tareas if not tarea.get("completada")
        ]
        carga_proyectada += (
            len(tareas_pendientes)
            * self.planificacion["estimaciones"]["tarea"]
        )
        calendario_proyectado = generar_planificacion(
            CATALOGO,
            self.planificacion,
            tareas=tareas,
        )
        horas_asignadas = sum(
            item["horas"]
            for asignaciones in calendario_proyectado.values()
            for item in asignaciones
        )
        fuera_objetivo = max(0.0, carga_proyectada - horas_asignadas)
        estado_plan = tk.Frame(
            self.contenido,
            bg=SOFT_RED if fuera_objetivo > 0 else SOFT_TEAL,
            highlightbackground="#eccaca" if fuera_objetivo > 0 else "#b5e7e4",
            highlightthickness=1,
            padx=16,
            pady=12,
        )
        estado_plan.pack(fill="x", pady=(0, 18))
        if fuera_objetivo > 0:
            estado_texto = (
                f"Con las estimaciones actuales quedarían {fuera_objetivo:.1f} h "
                "de contenido pendiente sin colocar antes de la fecha objetivo. "
                "Aumenta disponibilidad, revisa estimaciones o ajusta el objetivo."
            )
            estado_color = DANGER
        else:
            estado_texto = (
                f"El calendario puede colocar las {carga_proyectada:.1f} h "
                f"estimadas de contenido antes del objetivo. "
                f"Hay {max(0.0, capacidad - horas_asignadas):.1f} h de capacidad libre."
            )
            estado_color = ACCENT_DARK
        tk.Label(
            estado_plan,
            text=estado_texto,
            font=(FONT_FAMILY, 10, "bold"),
            fg=estado_color,
            bg=estado_plan["bg"],
            wraplength=900,
            justify="left",
        ).pack(anchor="w")

        tk.Label(self.contenido, text="Disponibilidad semanal", font=(FONT_FAMILY, 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(5, 8))
        disponibilidad = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=16)
        disponibilidad.pack(fill="x")
        entradas = {}
        for dia in DIAS_SEMANA:
            celda = tk.Frame(disponibilidad, bg=CARD)
            celda.pack(side="left", fill="x", expand=True, padx=3)
            tk.Label(celda, text=dia[:3], font=(FONT_FAMILY, 9, "bold"), fg=MUTED, bg=CARD).pack()
            entrada = ttk.Entry(celda, width=7, justify="center")
            entrada.insert(0, str(self.planificacion.get("disponibilidad", {}).get(dia, 0)))
            entrada.pack(pady=(5, 0))
            entradas[dia] = entrada
        boton(disponibilidad, "Guardar disponibilidad", lambda: self._guardar_disponibilidad(entradas), True).pack(anchor="e", pady=(12, 0))

        tk.Label(self.contenido, text="Registro de estudio", font=(FONT_FAMILY, 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(24, 8))
        self._registro_estudio()

        tk.Label(self.contenido, text="Plan de la semana", font=(FONT_FAMILY, 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(24, 8))
        self._mostrar_plan_semana()

    def _guardar_disponibilidad(self, entradas):
        datos = {}
        try:
            for dia, entrada in entradas.items():
                valor = float(entrada.get() or 0)
                if not math.isfinite(valor) or valor < 0:
                    raise ValueError
                datos[dia] = valor
        except ValueError:
            messagebox.showerror("Disponibilidad", "Las horas deben ser números no negativos.")
            return
        self.planificacion["disponibilidad"] = datos
        self.planificacion["horas_semanales_objetivo"] = round(sum(datos.values()), 1)
        if not self.guardar():
            self.planificacion = cargar_planificacion()
            return
        self.mostrar_planificacion()

    def _registro_estudio(self):
        frame = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=16)
        frame.pack(fill="x")
        campos = {}
        modulos = [
            f"{bloque} | {nombre}"
            for bloque, contenidos in CATALOGO.items()
            for nombre in contenidos
        ]
        def agregar_campo(etiqueta, clave, valor, fila, columna, ancho=0, span=1, tipo="entry"):
            celda = tk.Frame(frame, bg=CARD)
            celda.grid(
                row=fila,
                column=columna,
                columnspan=span,
                padx=5,
                pady=5,
                sticky="ew",
            )
            tk.Label(
                celda,
                text=etiqueta,
                font=(FONT_FAMILY, 10, "bold"),
                fg=TEXT,
                bg=CARD,
            ).pack(anchor="w", pady=(0, 3))
            if tipo == "combo":
                entrada = ttk.Combobox(
                    celda,
                    values=valor,
                    state="readonly",
                    width=ancho,
                )
            else:
                entrada = ttk.Entry(celda, width=ancho or 24)
                entrada.insert(0, valor)
            entrada.pack(fill="x")
            campos[clave] = entrada
            return entrada

        for columna in range(6):
            frame.columnconfigure(columna, weight=1)
        tipo = agregar_campo(
            "Tipo de actividad",
            "tipo",
            (
                "Clase",
                "Apuntes",
                "Clase + apuntes",
                "Tarea",
                "Evaluación",
                "Tutoría",
                "Clase en directo",
                "Práctica",
                "TFM",
            ),
            0,
            0,
            ancho=24,
            span=3,
            tipo="combo",
        )
        tipo.set("Clase")
        agregar_campo(
            "Fecha (AAAA-MM-DD)",
            "fecha",
            date.today().isoformat(),
            0,
            3,
            ancho=18,
            span=3,
        )
        modulo = agregar_campo(
            "Asignatura o módulo",
            "modulo",
            modulos,
            1,
            0,
            ancho=64,
            span=6,
            tipo="combo",
        )
        modulo.set("MÁSTER · FRONTEND | HTML")
        agregar_campo(
            "Qué has hecho",
            "actividad",
            "",
            2,
            0,
            ancho=44,
            span=6,
        )
        agregar_campo("Horas reales", "horas", "1", 3, 0, ancho=12, span=2)
        agregar_campo(
            "Hora de inicio (opcional)",
            "inicio",
            "",
            3,
            2,
            ancho=16,
            span=2,
        )
        agregar_campo(
            "Hora de fin (opcional)",
            "fin",
            "",
            3,
            4,
            ancho=16,
            span=2,
        )
        campos["tipo"].bind(
            "<<ComboboxSelected>>",
            lambda _evento: self._actualizar_estimacion_sesion(campos),
        )
        self._actualizar_estimacion_sesion(campos)
        boton(
            frame,
            "Registrar sesión y actualizar progreso",
            lambda: self._guardar_sesion(campos),
            True,
        ).grid(row=4, column=0, columnspan=6, sticky="e", padx=5, pady=(10, 0))

        actividades = self.planificacion.get("actividades_realizadas", [])
        if actividades:
            for i in reversed(range(max(0, len(actividades) - 10), len(actividades))):
                actividad = actividades[i]
                fila = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=9)
                fila.pack(fill="x", pady=3)
                texto = (
                    f"{actividad.get('fecha', '')} · "
                    f"{actividad.get('horas', 0)} h · "
                    f"{actividad.get('tipo', 'Estudio')} · "
                    f"{actividad.get('actividad', '')} · "
                    f"{actividad.get('modulo', '')}"
                )
                tk.Label(fila, text=texto, font=(FONT_FAMILY, 10), fg=TEXT, bg=CARD, anchor="w").pack(side="left", fill="x", expand=True)
                boton(fila, "Eliminar", lambda i=i: self._eliminar_sesion(i)).pack(side="right")

    def _actualizar_estimacion_sesion(self, campos):
        claves = {
            "Clase": "clase",
            "Apuntes": "apuntes",
            "Clase + apuntes": "clase_apuntes",
            "Tarea": "tarea",
            "Evaluación": "evaluacion",
            "Tutoría": "tutoria",
            "Clase en directo": "clase_directo",
            "Práctica": "practica",
            "TFM": "tfm",
        }
        tipo = campos["tipo"].get()
        horas = self.planificacion.get("estimaciones", {}).get(
            claves.get(tipo, "clase"),
            1.0,
        )
        campos["horas"].delete(0, tk.END)
        campos["horas"].insert(0, str(horas))

    def _guardar_sesion(self, campos):
        try:
            fecha = datetime.strptime(campos["fecha"].get().strip(), "%Y-%m-%d").date()
            horas = float(campos["horas"].get().strip())
            if not math.isfinite(horas) or horas <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Registro", "Usa fecha AAAA-MM-DD y horas mayores que 0.")
            return
        actividad = campos["actividad"].get().strip()
        modulo_seleccionado = campos["modulo"].get().strip()
        if not actividad:
            messagebox.showerror("Registro", "Escribe qué has hecho.")
            return
        bloque, separador, modulo = modulo_seleccionado.partition(" | ")
        if not separador:
            bloque, modulo = "", modulo_seleccionado
        tipo = campos["tipo"].get()
        registro = {
            "fecha": fecha.isoformat(),
            "actividad": actividad,
            "tipo": tipo,
            "bloque": bloque,
            "modulo": modulo,
            "horas": horas,
            "inicio": campos["inicio"].get().strip(),
            "fin": campos["fin"].get().strip(),
        }
        progreso_anterior = self._aplicar_progreso_sesion(registro)
        if progreso_anterior:
            registro["progreso_aplicado"] = progreso_anterior
        self.planificacion.setdefault("actividades_realizadas", []).append(registro)
        horas_dia = self.planificacion.setdefault("horas_realizadas", {})
        horas_dia[fecha.isoformat()] = round(float(horas_dia.get(fecha.isoformat(), 0) or 0) + horas, 2)
        if not self.guardar():
            self.planificacion = cargar_planificacion()
            return
        self.mostrar_planificacion()

    def _aplicar_progreso_sesion(self, sesion):
        bloque = sesion["bloque"]
        modulo = sesion["modulo"]
        tipo = sesion["tipo"]
        datos = CATALOGO.get(bloque, {}).get(modulo)
        if not datos:
            return {}

        clave = f"{bloque}|{modulo}"
        progreso = self.planificacion.setdefault("progreso_tema", {}).setdefault(clave, {})
        detalle = self.planificacion.setdefault("detalle_modulo", {}).setdefault(modulo, {})
        cambios = {}

        if tipo in (
            "Clase",
            "Clase + apuntes",
            "Clase en directo",
        ) and int(datos.get("clases", 0) or 0):
            anterior = min(
                int(datos["clases"]),
                _entero_no_negativo(
                    progreso.get(
                        "clases",
                        self.planificacion.get("clases_ingles_completadas", 0)
                        if bloque == "INGLÉS" and modulo == "Unidades 1–9"
                        else 0,
                    )
                ),
            )
            if anterior < int(datos["clases"]):
                progreso["clases"] = anterior + 1
                cambios["clases"] = anterior
                if bloque == "MÁSTER · FRONTEND" and modulo == "HTML":
                    for campo, total in (("tema_1", 7), ("tema_2", 6)):
                        hechas = min(
                            total,
                            _entero_no_negativo(detalle.get(campo, 0)),
                        )
                        if hechas < total:
                            detalle[campo] = hechas + 1
                            cambios[campo] = hechas
                            break

        if tipo in ("Tarea", "TFM") and int(datos.get("tareas", 0) or 0):
            anterior = min(
                int(datos["tareas"]),
                _entero_no_negativo(progreso.get("tareas", 0)),
            )
            if anterior < int(datos["tareas"]):
                progreso["tareas"] = anterior + 1
                cambios["tareas"] = anterior

        if tipo == "Evaluación" and int(datos.get("evaluaciones", 0) or 0):
            anterior = min(
                int(datos["evaluaciones"]),
                _entero_no_negativo(progreso.get("evaluaciones", 0)),
            )
            if anterior < int(datos["evaluaciones"]):
                progreso["evaluaciones"] = anterior + 1
                cambios["evaluaciones"] = anterior

        if tipo in ("Apuntes", "Clase + apuntes") and modulo == "Google Antigravity":
            anterior = min(10, _entero_no_negativo(detalle.get("apuntes", 6)))
            if anterior < 10:
                detalle["apuntes"] = anterior + 1
                cambios["apuntes"] = anterior

        if bloque == "INGLÉS":
            self.planificacion["clases_ingles_completadas"] = total_clases_ingles(
                self.planificacion
            )
        return {
            "bloque": bloque,
            "modulo": modulo,
            "antes": cambios,
        } if cambios else {}

    def _revertir_progreso_sesion(self, sesion):
        aplicado = sesion.get("progreso_aplicado")
        if not isinstance(aplicado, dict):
            return
        clave = f"{aplicado.get('bloque')}|{aplicado.get('modulo')}"
        progreso = self.planificacion.setdefault("progreso_tema", {}).setdefault(clave, {})
        detalle = self.planificacion.setdefault("detalle_modulo", {}).setdefault(
            aplicado.get("modulo"), {}
        )
        for campo in aplicado.get("antes", {}):
            if campo in ("apuntes", "tema_1", "tema_2"):
                detalle[campo] = max(0, _entero_no_negativo(detalle.get(campo, 0)) - 1)
            else:
                progreso[campo] = max(
                    0,
                    _entero_no_negativo(progreso.get(campo, 0)) - 1,
                )
        if aplicado.get("bloque") == "INGLÉS":
            self.planificacion["clases_ingles_completadas"] = total_clases_ingles(
                self.planificacion
            )

    def _eliminar_sesion(self, indice):
        actividades = self.planificacion.get("actividades_realizadas", [])
        if not (0 <= indice < len(actividades)):
            return
        actividad = actividades.pop(indice)
        self._revertir_progreso_sesion(actividad)
        fecha = actividad.get("fecha")
        try:
            horas = float(actividad.get("horas", 0) or 0)
            actuales = float(self.planificacion.get("horas_realizadas", {}).get(fecha, 0) or 0)
            nuevo = max(0, actuales - horas)
            if nuevo:
                self.planificacion["horas_realizadas"][fecha] = round(nuevo, 2)
            else:
                self.planificacion["horas_realizadas"].pop(fecha, None)
        except (ValueError, TypeError):
            pass
        if not self.guardar():
            self.planificacion = cargar_planificacion()
            return
        self.mostrar_planificacion()

    def _mostrar_plan_semana(self):
        hoy = date.today()
        calendario = generar_planificacion(
            CATALOGO,
            self.planificacion,
            hoy,
            cargar_tareas(ARCHIVO_TAREAS),
        )
        horas_registradas = horas_registradas_por_fecha(self.planificacion)
        for offset in range(7):
            fecha = hoy + timedelta(days=offset)
            dia = DIAS_SEMANA[fecha.weekday()]
            horas_totales_dia = max(
                0.0,
                float(self.planificacion.get("disponibilidad", {}).get(dia, 0) or 0),
            )
            horas = max(
                0.0,
                horas_totales_dia - horas_registradas.get(fecha.isoformat(), 0.0),
            )
            asignaciones = calendario.get(fecha.isoformat(), [])
            plan_texto = " · ".join(
                f"{asignacion['horas']:.0f} h {asignacion['modulo']}: "
                f"{', '.join(asignacion['detalles'])}"
                for asignacion in asignaciones
            )
            if not plan_texto:
                texto = (
                    "Sin capacidad disponible"
                    if horas < 1
                    else (
                        "Sin contenido desbloqueado pendiente"
                        if not calcular_carga_pendiente(CATALOGO, self.planificacion)
                        else "Sin unidad asignada; Antigravity se reserva para el miércoles"
                    )
                )
            else:
                texto = plan_texto
            reales = horas_registradas.get(fecha.isoformat(), 0.0)
            if reales:
                texto = f"Real: {reales:.1f} h · {texto}"
            fila = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=10)
            fila.pack(fill="x", pady=2)
            tk.Label(fila, text=f"{dia[:3]} {fecha.strftime('%d/%m')}", width=12, anchor="w", font=(FONT_FAMILY, 10, "bold"), fg=TEXT, bg=CARD).pack(side="left")
            horas_planificadas = sum(item["horas"] for item in asignaciones)
            tk.Label(fila, text=f"{horas_planificadas:.1f}/{horas:.1f} h", width=9, anchor="w", font=(FONT_FAMILY, 10, "bold"), fg=ACCENT, bg=CARD).pack(side="left")
            tk.Label(fila, text=texto, anchor="w", font=(FONT_FAMILY, 10), fg=MUTED, bg=CARD).pack(side="left", fill="x", expand=True)

    def _texto_para_horas(self, bolsas, horas):
        restante = horas
        partes = []
        for categoria, lista in bolsas:
            if not lista or restante <= 0:
                continue
            item = lista[0]
            bloque = min(restante, item.get("horas", 1))
            partes.append(f"{bloque:.1f} h · {categoria}: {item['nombre']} ({item['pendiente']})")
            restante -= bloque
        if restante > 0:
            partes.append(f"{restante:.1f} h · repaso/apuntes")
        return " + ".join(partes)

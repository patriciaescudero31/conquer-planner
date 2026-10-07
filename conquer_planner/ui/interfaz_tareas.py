import math
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk

from .interfaz_componentes import *
from .interfaz_datos import *
from .interfaz_datos import _entero_no_negativo
from ..core.tareas import cargar_tareas, guardar_tareas


class TareasMixin:
    def mostrar_tareas(self):
        limpiar(self.contenido)
        titulo(self.contenido, "Tareas", "Las tareas manuales pendientes aparecen en el plan diario por prioridad; no se generan tareas duplicadas desde el temario.")
        tareas_originales = cargar_tareas(ARCHIVO_TAREAS)
        tareas = self._limpiar_duplicados_tareas(tareas_originales)
        if tareas != tareas_originales and not self._guardar_tareas(tareas):
            return

        form = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=18)
        form.pack(fill="x", pady=(0, 16))
        tk.Label(form, text="Nueva tarea personal", font=(FONT_FAMILY, 16, "bold"), fg=TEXT, bg=CARD).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))
        nombre = ttk.Entry(form)
        nombre.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 8))
        nombre.insert(0, "")
        categoria = ttk.Entry(form)
        categoria.grid(row=1, column=2, sticky="ew", padx=8)
        categoria.insert(0, "General")
        prioridad = ttk.Combobox(form, values=("Alta", "Media", "Baja"), state="readonly", width=10)
        prioridad.set("Media")
        prioridad.grid(row=1, column=3, padx=(8, 0))
        tk.Label(form, text="Tarea", font=(FONT_FAMILY, 9), fg=MUTED, bg=CARD).grid(row=2, column=0, sticky="w", pady=(4, 0))
        tk.Label(form, text="Categoría", font=(FONT_FAMILY, 9), fg=MUTED, bg=CARD).grid(row=2, column=2, sticky="w", padx=8, pady=(4, 0))
        boton(form, "Añadir", lambda: self._crear_tarea(nombre, categoria, prioridad), True).grid(row=1, column=4, padx=(12, 0))
        for c in range(3):
            form.columnconfigure(c, weight=1)

        pendientes = [t for t in tareas if not t.get("completada")]
        completadas = [t for t in tareas if t.get("completada")]
        tk.Label(self.contenido, text=f"Pendientes ({len(pendientes)})", font=(FONT_FAMILY, 17, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(4, 8))
        for i, tarea in enumerate(pendientes):
            self._fila_tarea(tarea, tareas.index(tarea))
        if completadas:
            tk.Label(self.contenido, text=f"Completadas ({len(completadas)})", font=(FONT_FAMILY, 17, "bold"), fg=MUTED, bg=BG).pack(anchor="w", pady=(22, 8))
            for tarea in completadas:
                self._fila_tarea(tarea, tareas.index(tarea))

    def _limpiar_duplicados_tareas(self, tareas):
        resultado = []
        vistos = set()
        for tarea in tareas:
            clave = (
                tarea.get("nombre", "").strip().casefold(),
                tarea.get("categoria", "General").strip().casefold(),
            )
            if not clave[0] or clave in vistos:
                continue
            vistos.add(clave)
            resultado.append(tarea)
        return resultado

    def _crear_tarea(self, nombre, categoria, prioridad):
        texto = nombre.get().strip()
        if not texto:
            messagebox.showerror("Tarea", "Escribe una tarea.")
            return
        tareas = cargar_tareas(ARCHIVO_TAREAS)
        tareas = self._limpiar_duplicados_tareas(tareas)
        categoria_texto = categoria.get().strip() or "General"
        clave_nueva = (texto.casefold(), categoria_texto.casefold())
        if any(
            (
                tarea.get("nombre", "").casefold(),
                tarea.get("categoria", "General").casefold(),
            ) == clave_nueva
            for tarea in tareas
        ):
            messagebox.showwarning(
                "Tarea", "Ya existe una tarea con ese nombre y categoría."
            )
            return
        tareas.append({"nombre": texto, "fecha_limite": "", "prioridad": prioridad.get(), "categoria": categoria_texto, "completada": False, "tipo": "Manual"})
        if not self._guardar_tareas(tareas):
            return
        self.mostrar_tareas()

    def _guardar_tareas(self, tareas):
        if not guardar_tareas(tareas, ARCHIVO_TAREAS):
            messagebox.showerror(
                "Error", "No se han podido guardar las tareas.", parent=self.ventana
            )
            return False
        return True

    def _fila_tarea(self, tarea, indice):
        frame = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=11)
        frame.pack(fill="x", pady=3)
        estado = "✓" if tarea.get("completada") else "○"
        color = SUCCESS if tarea.get("completada") else TEXT
        centro = tk.Frame(frame, bg=CARD)
        centro.pack(side="left", fill="x", expand=True)
        tk.Label(centro, text=f"{estado}  {tarea.get('nombre', '')}", font=(FONT_FAMILY, 12, "bold"), fg=color, bg=CARD, anchor="w").pack(anchor="w")
        tk.Label(centro, text=f"{tarea.get('categoria', 'General')} · prioridad {tarea.get('prioridad', 'Media')}", font=(FONT_FAMILY, 9), fg=MUTED, bg=CARD).pack(anchor="w", pady=(3, 0))
        if not tarea.get("completada"):
            boton(frame, "Completar", lambda i=indice: self._completar_tarea(i), True).pack(side="right", padx=3)
        boton(frame, "Editar", lambda i=indice: self._editar_tarea(i)).pack(side="right", padx=3)
        boton(frame, "Eliminar", lambda i=indice: self._eliminar_tarea(i)).pack(side="right", padx=3)

    def _completar_tarea(self, indice):
        tareas = cargar_tareas(ARCHIVO_TAREAS)
        if 0 <= indice < len(tareas):
            tareas[indice]["completada"] = True
            if not self._guardar_tareas(tareas):
                return
        self.mostrar_tareas()

    def _eliminar_tarea(self, indice):
        tareas = cargar_tareas(ARCHIVO_TAREAS)
        if not (0 <= indice < len(tareas)):
            return
        if messagebox.askyesno("Eliminar", f"¿Eliminar «{tareas[indice].get('nombre', '')}»?"):
            tareas.pop(indice)
            if not self._guardar_tareas(tareas):
                return
            self.mostrar_tareas()

    def _editar_tarea(self, indice):
        tareas = cargar_tareas(ARCHIVO_TAREAS)
        if not (0 <= indice < len(tareas)):
            return
        tarea = tareas[indice]
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Editar tarea")
        ventana.geometry("520x300")
        ventana.configure(bg=BG)
        marco = tk.Frame(ventana, bg=CARD, padx=22, pady=22, highlightbackground=BORDER, highlightthickness=1)
        marco.pack(fill="both", expand=True, padx=18, pady=18)
        tk.Label(marco, text="Editar tarea", font=(FONT_FAMILY, 18, "bold"), fg=TEXT, bg=CARD).pack(anchor="w", pady=(0, 14))
        nombre = ttk.Entry(marco)
        nombre.insert(0, tarea.get("nombre", ""))
        nombre.pack(fill="x", pady=4)
        categoria = ttk.Entry(marco)
        categoria.insert(0, tarea.get("categoria", "General"))
        categoria.pack(fill="x", pady=4)
        prioridad = ttk.Combobox(marco, values=("Alta", "Media", "Baja"), state="readonly")
        prioridad.set(tarea.get("prioridad", "Media"))
        prioridad.pack(anchor="w", pady=4)

        def guardar():
            tarea.update({"nombre": nombre.get().strip(), "categoria": categoria.get().strip() or "General", "prioridad": prioridad.get()})
            if not tarea["nombre"]:
                messagebox.showerror("Tarea", "El nombre no puede estar vacío.", parent=ventana)
                return
            if not self._guardar_tareas(tareas):
                return
            ventana.destroy()
            self.mostrar_tareas()

        boton(marco, "Guardar cambios", guardar, True).pack(anchor="w", pady=(12, 0))

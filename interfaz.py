import json
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime, date, timedelta

from tareas import cargar_tareas, guardar_tareas
from utilidades import calcular_horas_hasta_objetivo


ARCHIVO_TAREAS = Path("tareas.json")
ARCHIVO_PLANIFICACION = Path("planificacion.json")

DIAS_SEMANA = [
    "Lunes", "Martes", "Miércoles", "Jueves",
    "Viernes", "Sábado", "Domingo",
]

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]

# Datos académicos que ya tenemos confirmados.
TEMARIO = {
    "MÁSTER · PREWORK": {
        "Pseudocódigo": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "Linux y terminal": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "Python": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "GitHub": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "SQL": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "Automatizaciones y agentes": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Apuntes pendientes"},
        "IA · Google Antigravity": {"temas": 0, "clases": 7, "tareas": 0, "evaluaciones": 0, "estado": "7 clases pendientes"},
    },
    "MÁSTER · FRONTEND": {
        "HTML": {"temas": 8, "clases": 27, "tareas": 2, "evaluaciones": 3},
        "CSS": {"temas": 12, "clases": 56, "tareas": 5, "evaluaciones": 3},
        "JavaScript": {"temas": 11, "clases": 51, "tareas": 2, "evaluaciones": 3},
        "React JS": {"temas": 4, "clases": 16, "tareas": 2, "evaluaciones": 0},
        "Diseña con IA": {"temas": 1, "clases": 7, "tareas": 0, "evaluaciones": 0},
    },
    "MÁSTER · BACKEND": {
        "Django": {"temas": 13, "clases": 61, "tareas": 2, "evaluaciones": 2},
        "Agentes CLI": {"temas": 1, "clases": 12, "tareas": 0, "evaluaciones": 1},
        "Despliegue": {"temas": 11, "clases": 17, "tareas": 0, "evaluaciones": 0},
        "SEO": {"temas": 1, "clases": 3, "tareas": 0, "evaluaciones": 0},
    },
    "MÁSTER · DESARROLLO PROFESIONAL": {
        "Preparación de entrevistas": {"temas": 8, "clases": 28, "tareas": 0, "evaluaciones": 0},
        "Metodologías ágiles y Scrum": {"temas": 3, "clases": 3, "tareas": 0, "evaluaciones": 1},
        "Soft Skills": {"temas": 5, "clases": 8, "tareas": 0, "evaluaciones": 1},
        "Propuestas laborales": {"temas": 3, "clases": 10, "tareas": 0, "evaluaciones": 0},
        "Proyecto de Fin de Máster": {"temas": 1, "clases": 0, "tareas": 1, "evaluaciones": 0},
    },
    "BONUS · BACKEND EXPERTO": {
        "SQL avanzado": {"temas": 5, "clases": 14, "tareas": 0, "evaluaciones": 1},
        "WordPress": {"temas": 9, "clases": 22, "tareas": 1, "evaluaciones": 1},
        "Streamlit": {"temas": 3, "clases": 6, "tareas": 0, "evaluaciones": 1},
        "Java": {"temas": 5, "clases": 16, "tareas": 0, "evaluaciones": 1},
        "Node.js": {"temas": 6, "clases": 16, "tareas": 0, "evaluaciones": 0},
        "Rust": {"temas": 7, "clases": 14, "tareas": 0, "evaluaciones": 1},
        "Go": {"temas": 7, "clases": 8, "tareas": 0, "evaluaciones": 0},
    },
    "BONUS · FRONTEND EXPERTO": {
        "React con TypeScript": {"temas": 9, "clases": 16, "tareas": 0, "evaluaciones": 1},
        "React JS avanzado con TypeScript": {"temas": 7, "clases": 7, "tareas": 0, "evaluaciones": 0},
        "Astro": {"temas": 9, "clases": 12, "tareas": 0, "evaluaciones": 1},
        "Angular": {"temas": 8, "clases": 8, "tareas": 0, "evaluaciones": 1},
        "Vue JS": {"temas": 5, "clases": 5, "tareas": 0, "evaluaciones": 0},
    },
    "INGLÉS": {
        "Unidad 10": {"temas": 1, "clases": 4, "tareas": 0, "evaluaciones": 0},
        "Unidad 11": {"temas": 1, "clases": 3, "tareas": 0, "evaluaciones": 0},
        "Unidad 12": {"temas": 1, "clases": 4, "tareas": 0, "evaluaciones": 0},
        "Unidad 13": {"temas": 1, "clases": 3, "tareas": 0, "evaluaciones": 0},
        "Unidad 14": {"temas": 1, "clases": 4, "tareas": 0, "evaluaciones": 0},
        "Unidad 15": {"temas": 1, "clases": 2, "tareas": 0, "evaluaciones": 0},
        "Unidad 16": {"temas": 1, "clases": 5, "tareas": 0, "evaluaciones": 0},
        "Unidad 17": {"temas": 1, "clases": 3, "tareas": 0, "evaluaciones": 0},
        "Unidad 18": {"temas": 1, "clases": 4, "tareas": 0, "evaluaciones": 0},
        "Unidad 19": {"temas": 1, "clases": 4, "tareas": 0, "evaluaciones": 0},
        "Unidad 20": {"temas": 1, "clases": 6, "tareas": 0, "evaluaciones": 0},
        "Actividades": {"temas": 0, "clases": 18, "tareas": 0, "evaluaciones": 0},
        "Bonus inglés": {"temas": 0, "clases": 12, "tareas": 0, "evaluaciones": 0},
        "Evaluación final": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 1},
    },
    "BONUS · PRODUCTIVIDAD": {
        "Productividad": {"temas": 1, "clases": 7, "tareas": 0, "evaluaciones": 0},
    },
    "BONUS · IA PARA EL DESARROLLO": {
        "Uso de inteligencia artificial para el desarrollo": {"temas": 3, "clases": 4, "tareas": 0, "evaluaciones": 0},
    },
    "BONUS · DOCKER": {
        "Docker al completo": {"temas": 1, "clases": 20, "tareas": 0, "evaluaciones": 1},
    },
}


def cargar_planificacion():
    if not ARCHIVO_PLANIFICACION.exists():
        return {}
    try:
        with open(ARCHIVO_PLANIFICACION, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return datos if isinstance(datos, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def guardar_planificacion_datos(planificacion):
    try:
        with open(ARCHIVO_PLANIFICACION, "w", encoding="utf-8") as archivo:
            json.dump(planificacion, archivo, ensure_ascii=False, indent=4)
        return True
    except OSError:
        messagebox.showerror("Error", "No se pudo guardar la planificación.")
        return False


def preparar_planificacion(planificacion):
    planificacion.setdefault("fecha_objetivo", "31/03/2027")
    planificacion.setdefault("horas_semanales_objetivo", 33.0)
    planificacion.setdefault("horas_realizadas", {})
    planificacion.setdefault("actividades_realizadas", [])
    planificacion.setdefault("disponibilidad", {dia: 0.0 for dia in DIAS_SEMANA})
    planificacion.setdefault("porcentaje_master", 35.0)
    planificacion.setdefault("porcentaje_ingles", 29.0)
    planificacion.setdefault("clases_ingles_completadas", 30)
    planificacion.setdefault("progreso_tema", {})
    planificacion.setdefault("horas_totales_master", 0.0)
    guardar_planificacion_datos(planificacion)
    return planificacion


def crear_titulo(contenido, titulo, subtitulo):
    tk.Label(contenido, text=titulo, font=("Helvetica", 28, "bold"), fg="#222222", bg="#f7f7f7").pack(anchor="w", pady=(10, 5))
    tk.Label(contenido, text=subtitulo, font=("Helvetica", 14), fg="#555555", bg="#f7f7f7").pack(anchor="w", pady=(0, 25))


def limpiar_contenido(contenido):
    for widget in contenido.winfo_children():
        widget.destroy()


def obtener_fecha_objetivo(planificacion):
    try:
        return datetime.strptime(planificacion.get("fecha_objetivo", "31/03/2027"), "%d/%m/%Y").date()
    except (ValueError, TypeError):
        return date(2027, 3, 31)


def obtener_progreso_academico(planificacion):
    try:
        return max(0.0, min(100.0, float(planificacion.get("porcentaje_master", 35.0))))
    except (ValueError, TypeError):
        return 35.0


def obtener_progreso_ingles(planificacion):
    try:
        return max(0.0, min(100.0, float(planificacion.get("porcentaje_ingles", 29.0))))
    except (ValueError, TypeError):
        return 29.0


def calcular_semanas_restantes(fecha_objetivo):
    dias = (fecha_objetivo - date.today()).days
    return 0 if dias <= 0 else max(1, (dias + 6) // 7)


def calcular_horas_necesarias(planificacion, fecha_objetivo):
    semanas = calcular_semanas_restantes(fecha_objetivo)
    try:
        horas_totales = float(planificacion.get("horas_totales_master", 0))
    except (ValueError, TypeError):
        horas_totales = 0.0
    if horas_totales <= 0 or semanas <= 0:
        return 0.0
    return horas_totales * (100 - obtener_progreso_academico(planificacion)) / 100 / semanas


def obtener_semana_actual():
    hoy = date.today()
    inicio = hoy - timedelta(days=hoy.weekday())
    return inicio, inicio + timedelta(days=6)


def obtener_horas_registradas_semana(planificacion, inicio):
    total = 0.0
    registros = planificacion.get("horas_realizadas", {})
    for i in range(7):
        try:
            total += float(registros.get((inicio + timedelta(days=i)).isoformat(), 0))
        except (ValueError, TypeError):
            pass
    return total


def obtener_horas_disponibles_semana(planificacion):
    total = 0.0
    for dia in DIAS_SEMANA:
        try:
            total += max(0.0, float(planificacion.get("disponibilidad", {}).get(dia, 0)))
        except (ValueError, TypeError):
            pass
    return total


def crear_tarjeta(contenedor, titulo, valor, fila, columna):
    tarjeta = tk.Frame(contenedor, relief="solid", borderwidth=1, padx=20, pady=20, bg="#ffffff")
    tarjeta.grid(row=fila, column=columna, padx=8, pady=8, sticky="nsew")
    tk.Label(tarjeta, text=titulo, font=("Helvetica", 12), fg="#555555", bg="#ffffff").pack(anchor="w")
    tk.Label(tarjeta, text=valor, font=("Helvetica", 22, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w", pady=(10, 0))


def obtener_datos_inicio():
    tareas = cargar_tareas(ARCHIVO_TAREAS)
    planificacion = preparar_planificacion(cargar_planificacion())
    completadas = sum(1 for tarea in tareas if tarea.get("completada", False))
    fecha = obtener_fecha_objetivo(planificacion)
    return {
        "fecha": fecha.strftime("%d/%m/%Y"),
        "progreso": obtener_progreso_academico(planificacion),
        "ingles": obtener_progreso_ingles(planificacion),
        "pendientes": len(tareas) - completadas,
        "horas_semana": obtener_horas_registradas_semana(planificacion, obtener_semana_actual()[0]),
    }


def mostrar_inicio(contenido):
    limpiar_contenido(contenido)
    datos = obtener_datos_inicio()
    crear_titulo(contenido, "Inicio", "Tu planificación académica de un vistazo")
    tarjetas = tk.Frame(contenido, bg="#f7f7f7")
    tarjetas.pack(fill="x")
    for c in range(2):
        tarjetas.columnconfigure(c, weight=1)
    crear_tarjeta(tarjetas, "Objetivo", datos["fecha"], 0, 0)
    crear_tarjeta(tarjetas, "Máster", f'{datos["progreso"]:.0f}%', 0, 1)
    crear_tarjeta(tarjetas, "Inglés", f'{datos["ingles"]:.0f}%', 1, 0)
    crear_tarjeta(tarjetas, "Horas esta semana", f'{datos["horas_semana"]:g} h', 1, 1)

    aviso = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=20, pady=20)
    aviso.pack(fill="x", pady=15)
    tk.Label(aviso, text="Plan de estudio", font=("Helvetica", 17, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w")
    tk.Label(aviso, text=("La aplicación ahora puede calcular un plan diario a partir de las horas disponibles de cada día, "
                          "registrar qué has hecho realmente y mantener separado el contenido obligatorio de los bonus."),
             font=("Helvetica", 13), justify="left", fg="#333333", bg="#ffffff", wraplength=850).pack(anchor="w", pady=(8, 0))


def normalizar_tarea(nombre, fecha_limite, prioridad, categoria, tipo="Tarea"):
    return {
        "nombre": nombre.strip(),
        "fecha_limite": fecha_limite.strip(),
        "prioridad": prioridad,
        "categoria": categoria.strip() or "General",
        "completada": False,
        "tipo": tipo,
    }


def guardar_nueva_tarea(contenido, entradas):
    nombre = entradas["nombre"].get().strip()
    fecha = entradas["fecha"].get().strip()
    if not nombre:
        messagebox.showerror("Dato incorrecto", "Escribe el nombre de la tarea.")
        return
    if fecha:
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Fecha incorrecta", "Usa el formato dd/mm/aaaa.")
            return
    tareas = cargar_tareas(ARCHIVO_TAREAS)
    tareas.append(normalizar_tarea(nombre, fecha, entradas["prioridad"].get(), entradas["categoria"].get()))
    guardar_tareas(tareas, ARCHIVO_TAREAS)
    mostrar_tareas_en_interfaz(contenido)


def completar_tarea_interfaz(indice, contenido):
    tareas = cargar_tareas(ARCHIVO_TAREAS)
    if 0 <= indice < len(tareas):
        tareas[indice]["completada"] = True
        guardar_tareas(tareas, ARCHIVO_TAREAS)
        mostrar_tareas_en_interfaz(contenido)


def eliminar_tarea_interfaz(indice, contenido):
    tareas = cargar_tareas(ARCHIVO_TAREAS)
    if 0 <= indice < len(tareas):
        if not messagebox.askyesno("Eliminar tarea", "¿Seguro que quieres eliminar esta tarea?"):
            return
        tareas.pop(indice)
        guardar_tareas(tareas, ARCHIVO_TAREAS)
        mostrar_tareas_en_interfaz(contenido)


def editar_tarea_interfaz(indice, contenido):
    tareas = cargar_tareas(ARCHIVO_TAREAS)
    if not (0 <= indice < len(tareas)):
        return
    tarea = tareas[indice]
    ventana = tk.Toplevel(contenido.winfo_toplevel())
    ventana.title("Editar tarea")
    ventana.geometry("520x330")
    ventana.configure(bg="#f7f7f7")
    marco = tk.Frame(ventana, bg="#ffffff", relief="solid", borderwidth=1, padx=20, pady=20)
    marco.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(marco, text="Editar tarea", font=("Helvetica", 18, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w", pady=(0, 15))
    tk.Label(marco, text="Qué tienes que hacer", fg="#222222", bg="#ffffff").pack(anchor="w")
    nombre = tk.Entry(marco, width=55, fg="#000000", bg="#ffffff")
    nombre.insert(0, tarea.get("nombre", ""))
    nombre.pack(fill="x", pady=(3, 10))

    tk.Label(marco, text="Fecha límite (dd/mm/aaaa)", fg="#222222", bg="#ffffff").pack(anchor="w")
    fecha = tk.Entry(marco, width=25, fg="#000000", bg="#ffffff")
    fecha.insert(0, tarea.get("fecha_limite", ""))
    fecha.pack(anchor="w", pady=(3, 10))

    tk.Label(marco, text="Prioridad", fg="#222222", bg="#ffffff").pack(anchor="w")
    prioridad = tk.StringVar(value=tarea.get("prioridad", "Media"))
    tk.OptionMenu(marco, prioridad, "Alta", "Media", "Baja").pack(anchor="w", pady=(3, 10))

    tk.Label(marco, text="Categoría / módulo", fg="#222222", bg="#ffffff").pack(anchor="w")
    categoria = tk.Entry(marco, width=40, fg="#000000", bg="#ffffff")
    categoria.insert(0, tarea.get("categoria", "General"))
    categoria.pack(fill="x", pady=(3, 10))

    def guardar():
        nuevo_nombre = nombre.get().strip()
        nueva_fecha = fecha.get().strip()
        if not nuevo_nombre:
            messagebox.showerror("Dato incorrecto", "Escribe el nombre de la tarea.", parent=ventana)
            return
        if nueva_fecha:
            try:
                datetime.strptime(nueva_fecha, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Fecha incorrecta", "Usa el formato dd/mm/aaaa.", parent=ventana)
                return
        tareas[indice].update({
            "nombre": nuevo_nombre,
            "fecha_limite": nueva_fecha,
            "prioridad": prioridad.get(),
            "categoria": categoria.get().strip() or "General",
        })
        guardar_tareas(tareas, ARCHIVO_TAREAS)
        ventana.destroy()
        mostrar_tareas_en_interfaz(contenido)

    tk.Button(marco, text="Guardar cambios", fg="#000000", bg="#eeeeee", activeforeground="#000000", command=guardar).pack(anchor="w")


def crear_formulario_tarea(contenido, padre):
    formulario = tk.Frame(padre, bg="#ffffff", relief="solid", borderwidth=1, padx=15, pady=15)
    formulario.pack(fill="x", pady=(0, 15))
    tk.Label(formulario, text="Nueva tarea", font=("Helvetica", 16, "bold"), fg="#222222", bg="#ffffff").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
    tk.Label(formulario, text="Qué tienes que hacer", fg="#222222", bg="#ffffff").grid(row=1, column=0, sticky="w")
    nombre = tk.Entry(formulario, width=40, fg="#000000", bg="#ffffff")
    nombre.grid(row=1, column=1, sticky="ew", padx=8, pady=4)
    tk.Label(formulario, text="Fecha límite (dd/mm/aaaa)", fg="#222222", bg="#ffffff").grid(row=2, column=0, sticky="w")
    fecha = tk.Entry(formulario, width=20, fg="#000000", bg="#ffffff")
    fecha.grid(row=2, column=1, sticky="w", padx=8, pady=4)
    tk.Label(formulario, text="Prioridad", fg="#222222", bg="#ffffff").grid(row=3, column=0, sticky="w")
    prioridad = tk.StringVar(value="Media")
    tk.OptionMenu(formulario, prioridad, "Alta", "Media", "Baja").grid(row=3, column=1, sticky="w", padx=8, pady=4)
    tk.Label(formulario, text="Categoría / módulo", fg="#222222", bg="#ffffff").grid(row=4, column=0, sticky="w")
    categoria = tk.Entry(formulario, width=30, fg="#000000", bg="#ffffff")
    categoria.grid(row=4, column=1, sticky="ew", padx=8, pady=4)
    formulario.columnconfigure(1, weight=1)
    tk.Label(formulario, text="Ejemplo: 'Terminar tarea de Django' · categoría: 'Django'", font=("Helvetica", 9), fg="#666666", bg="#ffffff").grid(row=5, column=1, sticky="w", padx=8)
    tk.Button(formulario, text="Añadir tarea", fg="#000000", bg="#eeeeee", activeforeground="#000000",
              command=lambda: guardar_nueva_tarea(contenido, {"nombre": nombre, "fecha": fecha, "prioridad": prioridad, "categoria": categoria})).grid(row=6, column=1, sticky="w", padx=8, pady=(8, 0))


def mostrar_tareas_en_interfaz(contenido):
    planificacion = preparar_planificacion(cargar_planificacion())
    generar_tareas_automaticas(planificacion)
    limpiar_contenido(contenido)
    crear_titulo(contenido, "Tareas", "Crea, completa, edita y elimina tareas académicas")
    crear_formulario_tarea(contenido, contenido)
    tareas = cargar_tareas(ARCHIVO_TAREAS)
    if not tareas:
        tk.Label(contenido, text="No tienes tareas todavía. Añade la primera arriba.", font=("Helvetica", 15), fg="#222222", bg="#f7f7f7").pack(pady=30)
        return

    prioridad_orden = {"Alta": 0, "Media": 1, "Baja": 2}
    indices = sorted(range(len(tareas)), key=lambda i: (tareas[i].get("completada", False), prioridad_orden.get(tareas[i].get("prioridad", "Media"), 1)))
    for indice in indices:
        tarea = tareas[indice]
        fila = tk.Frame(contenido, relief="solid", borderwidth=1, padx=12, pady=10, bg="#ffffff")
        fila.pack(fill="x", pady=4)
        estado = "✓" if tarea.get("completada", False) else "○"
        texto = (f"{estado} {tarea.get('nombre', 'Sin nombre')}\n"
                 f"Fecha: {tarea.get('fecha_limite') or 'Sin fecha'} | "
                 f"Prioridad: {tarea.get('prioridad', 'Media')} | "
                 f"Categoría: {tarea.get('categoria', 'General')}")
        tk.Label(fila, text=texto, font=("Helvetica", 12), justify="left", fg="#222222", bg="#ffffff", anchor="w").pack(side="left", anchor="w", fill="x", expand=True)
        tk.Button(fila, text="Editar", fg="#000000", bg="#eeeeee", activeforeground="#000000",
                  command=lambda i=indice: editar_tarea_interfaz(i, contenido)).pack(side="right", padx=4)
        if not tarea.get("completada", False):
            tk.Button(fila, text="Completar", fg="#000000", bg="#eeeeee", activeforeground="#000000",
                      command=lambda i=indice: completar_tarea_interfaz(i, contenido)).pack(side="right", padx=4)
        tk.Button(fila, text="Eliminar", fg="#000000", bg="#eeeeee", activeforeground="#000000",
                  command=lambda i=indice: eliminar_tarea_interfaz(i, contenido)).pack(side="right", padx=4)

def registrar_horas_hoy(planificacion, entrada):
    try:
        horas = float(entrada.get())
        if horas < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Dato incorrecto", "Introduce un número de horas válido.")
        return
    planificacion.setdefault("horas_realizadas", {})[date.today().isoformat()] = horas
    guardar_planificacion_datos(planificacion)
    messagebox.showinfo("Guardado", f"Se han registrado {horas:g} horas para hoy.")


def cambiar_objetivo_semanal(planificacion, entrada):
    try:
        horas = float(entrada.get())
        if horas <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Dato incorrecto", "Introduce un número de horas válido.")
        return
    planificacion["horas_semanales_objetivo"] = horas
    guardar_planificacion_datos(planificacion)
    messagebox.showinfo("Guardado", f"Objetivo semanal actualizado a {horas:g} horas.")


def guardar_disponibilidad(planificacion, entradas):
    disponibilidad = {}
    for dia, entrada in entradas.items():
        try:
            valor = float(entrada.get() or 0)
            if valor < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Dato incorrecto", f"Horas no válidas para {dia}.")
            return
        disponibilidad[dia] = valor
    planificacion["disponibilidad"] = disponibilidad
    guardar_planificacion_datos(planificacion)
    messagebox.showinfo("Guardado", f"Disponibilidad guardada: {sum(disponibilidad.values()):g} h/semana.")


def recalcular_horas_realizadas(planificacion):
    """Reconstruye las horas diarias a partir del historial editable."""
    horas = {}
    for actividad in planificacion.get("actividades_realizadas", []):
        fecha = actividad.get("fecha", "")
        try:
            valor = float(actividad.get("horas", 0))
        except (ValueError, TypeError):
            valor = 0.0
        if fecha and valor > 0:
            horas[fecha] = round(horas.get(fecha, 0.0) + valor, 2)
    planificacion["horas_realizadas"] = horas


def registrar_actividad(planificacion, actividad, horas, inicio, fin, modulo, fecha_texto=None):
    try:
        horas = float(horas)
        if horas <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Dato incorrecto", "Introduce una duración válida.")
        return False
    fecha = date.today().isoformat()
    if fecha_texto:
        try:
            fecha = datetime.strptime(fecha_texto.strip(), "%d/%m/%Y").date().isoformat()
        except ValueError:
            messagebox.showerror("Fecha incorrecta", "Usa el formato dd/mm/aaaa.")
            return False
    planificacion.setdefault("actividades_realizadas", []).append({
        "fecha": fecha,
        "actividad": actividad.strip(),
        "modulo": modulo.strip(),
        "horas": horas,
        "inicio": inicio.strip(),
        "fin": fin.strip(),
    })
    recalcular_horas_realizadas(planificacion)
    guardar_planificacion_datos(planificacion)
    return True


def obtener_horas_del_dia(planificacion, fecha):
    total = 0.0
    for actividad in planificacion.get("actividades_realizadas", []):
        if actividad.get("fecha") == fecha.isoformat():
            try:
                total += float(actividad.get("horas", 0))
            except (ValueError, TypeError):
                pass
    if total == 0:
        try:
            total = float(planificacion.get("horas_realizadas", {}).get(fecha.isoformat(), 0))
        except (ValueError, TypeError):
            total = 0.0
    return round(total, 2)


def editar_actividad(planificacion, indice, contenido):
    actividades = planificacion.get("actividades_realizadas", [])
    if not (0 <= indice < len(actividades)):
        return
    actividad = actividades[indice]
    ventana = tk.Toplevel(contenido.winfo_toplevel())
    ventana.title("Editar actividad")
    ventana.geometry("600x430")
    ventana.configure(bg="#f7f7f7")
    marco = tk.Frame(ventana, bg="#ffffff", relief="solid", borderwidth=1, padx=20, pady=20)
    marco.pack(fill="both", expand=True, padx=20, pady=20)
    tk.Label(marco, text="Editar actividad realizada", font=("Helvetica", 18, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w", pady=(0, 15))

    campos = {}
    definiciones = [
        ("Qué hiciste", "actividad", actividad.get("actividad", "")),
        ("Módulo", "modulo", actividad.get("modulo", "")),
        ("Fecha (dd/mm/aaaa)", "fecha", datetime.strptime(actividad.get("fecha", date.today().isoformat()), "%Y-%m-%d").strftime("%d/%m/%Y")),
        ("Horas", "horas", str(actividad.get("horas", ""))),
        ("Desde", "inicio", actividad.get("inicio", "")),
        ("Hasta", "fin", actividad.get("fin", "")),
    ]
    for etiqueta, clave, valor in definiciones:
        tk.Label(marco, text=etiqueta, fg="#222222", bg="#ffffff").pack(anchor="w", pady=(4, 0))
        e = tk.Entry(marco, fg="#000000", bg="#ffffff")
        e.insert(0, valor)
        e.pack(fill="x", pady=(2, 6))
        campos[clave] = e

    def guardar():
        try:
            fecha = datetime.strptime(campos["fecha"].get().strip(), "%d/%m/%Y").date().isoformat()
            horas = float(campos["horas"].get())
            if horas <= 0 or not campos["actividad"].get().strip():
                raise ValueError
        except ValueError:
            messagebox.showerror("Dato incorrecto", "Revisa la actividad, la fecha y las horas.", parent=ventana)
            return
        actividades[indice] = {
            "fecha": fecha,
            "actividad": campos["actividad"].get().strip(),
            "modulo": campos["modulo"].get().strip(),
            "horas": horas,
            "inicio": campos["inicio"].get().strip(),
            "fin": campos["fin"].get().strip(),
        }
        recalcular_horas_realizadas(planificacion)
        guardar_planificacion_datos(planificacion)
        ventana.destroy()
        mostrar_planificacion(contenido)

    tk.Button(marco, text="Guardar cambios", fg="#000000", bg="#eeeeee", activeforeground="#000000", command=guardar).pack(anchor="w", pady=(8, 0))


def eliminar_actividad(planificacion, indice, contenido):
    actividades = planificacion.get("actividades_realizadas", [])
    if not (0 <= indice < len(actividades)):
        return
    if not messagebox.askyesno("Eliminar actividad", "¿Quieres eliminar este registro?", parent=contenido.winfo_toplevel()):
        return
    actividades.pop(indice)
    recalcular_horas_realizadas(planificacion)
    guardar_planificacion_datos(planificacion)
    mostrar_planificacion(contenido)


def crear_registro_actividad(contenido, planificacion):
    marco = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=15, pady=15)
    marco.pack(fill="x", pady=(15, 10))
    tk.Label(marco, text="Registrar qué has hecho", font=("Helvetica", 17, "bold"), fg="#222222", bg="#ffffff").grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 10))
    etiquetas = [("Actividad", 1, 0), ("Módulo", 1, 2), ("Horas", 2, 0), ("Desde", 2, 2), ("Hasta", 3, 2), ("Fecha", 3, 0)]
    for texto, fila, col in etiquetas:
        tk.Label(marco, text=texto, fg="#222222", bg="#ffffff").grid(row=fila, column=col, sticky="w")
    actividad = tk.Entry(marco, width=28, fg="#000000", bg="#ffffff")
    actividad.grid(row=1, column=1, padx=5, pady=4)
    modulo = tk.Entry(marco, width=24, fg="#000000", bg="#ffffff")
    modulo.grid(row=1, column=3, padx=5, pady=4)
    horas = tk.Entry(marco, width=10, fg="#000000", bg="#ffffff")
    horas.grid(row=2, column=1, sticky="w", padx=5, pady=4)
    inicio = tk.Entry(marco, width=10, fg="#000000", bg="#ffffff")
    inicio.grid(row=2, column=3, sticky="w", padx=5, pady=4)
    fin = tk.Entry(marco, width=10, fg="#000000", bg="#ffffff")
    fin.grid(row=3, column=3, sticky="w", padx=5, pady=4)
    fecha = tk.Entry(marco, width=12, fg="#000000", bg="#ffffff")
    fecha.insert(0, date.today().strftime("%d/%m/%Y"))
    fecha.grid(row=3, column=1, sticky="w", padx=5, pady=4)
    tk.Button(marco, text="Guardar actividad", fg="#000000", bg="#eeeeee", activeforeground="#000000",
              command=lambda: guardar_actividad_y_refrescar(contenido, planificacion, actividad, horas, inicio, fin, modulo, fecha)).grid(row=4, column=1, sticky="w", pady=(8, 0))


def guardar_actividad_y_refrescar(contenido, planificacion, actividad, horas, inicio, fin, modulo, fecha):
    if not actividad.get().strip():
        messagebox.showerror("Dato incorrecto", "Escribe qué has hecho.")
        return
    if registrar_actividad(planificacion, actividad.get(), horas.get(), inicio.get(), fin.get(), modulo.get(), fecha.get()):
        mostrar_planificacion(contenido)


def mostrar_historial_actividades(contenido, planificacion):
    actividades = planificacion.get("actividades_realizadas", [])
    if not actividades:
        return
    tk.Label(contenido, text="Historial editable", font=("Helvetica", 18, "bold"), fg="#222222", bg="#f7f7f7").pack(anchor="w", pady=(10, 8))
    for indice in reversed(range(len(actividades))):
        actividad = actividades[indice]
        try:
            fecha = datetime.strptime(actividad.get("fecha", ""), "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            fecha = actividad.get("fecha", "")
        fila = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=10, pady=8)
        fila.pack(fill="x", pady=3)
        texto = f"{fecha} · {actividad.get('horas', 0):g} h · {actividad.get('actividad', '')} · {actividad.get('modulo', '')}"
        tk.Label(fila, text=texto, font=("Helvetica", 11), fg="#222222", bg="#ffffff", anchor="w", justify="left", wraplength=650).pack(side="left", fill="x", expand=True)
        tk.Button(fila, text="Editar", fg="#000000", bg="#eeeeee", activeforeground="#000000", command=lambda i=indice: editar_actividad(planificacion, i, contenido)).pack(side="right", padx=3)
        tk.Button(fila, text="Eliminar", fg="#000000", bg="#eeeeee", activeforeground="#000000", command=lambda i=indice: eliminar_actividad(planificacion, i, contenido)).pack(side="right", padx=3)


def obtener_pendientes_academicos(planificacion):
    """Obtiene el siguiente trabajo pendiente de cada módulo, sin inventar nombres de clases."""
    pendientes_master, pendientes_ingles, pendientes_bonus = [], [], []
    progreso = planificacion.get("progreso_tema", {})
    for bloque, modulos in TEMARIO.items():
        destino = pendientes_master if bloque.startswith("MÁSTER") else pendientes_ingles if bloque == "INGLÉS" else pendientes_bonus if bloque.startswith("BONUS") else None
        if destino is None:
            continue
        for nombre, datos in modulos.items():
            clave = f"{bloque}|{nombre}"
            hecho = progreso.get(clave, {})
            total_clases = int(datos.get("clases", 0) or 0)
            hechas_clases = min(total_clases, int(hecho.get("clases", 0) or 0))
            total_tareas = int(datos.get("tareas", 0) or 0)
            hechas_tareas = min(total_tareas, int(hecho.get("tareas", 0) or 0))
            total_eval = int(datos.get("evaluaciones", 0) or 0)
            hechas_eval = min(total_eval, int(hecho.get("evaluaciones", 0) or 0))
            pendientes = []
            if total_clases > hechas_clases:
                pendientes.append(f"siguiente clase ({hechas_clases + 1}/{total_clases})")
            if total_tareas > hechas_tareas:
                pendientes.append(f"tarea ({hechas_tareas + 1}/{total_tareas})")
            if total_eval > hechas_eval:
                pendientes.append(f"evaluación ({hechas_eval + 1}/{total_eval})")
            if datos.get("estado") and datos.get("estado") != "Completado" and not pendientes:
                pendientes.append(datos["estado"])
            if pendientes:
                destino.append({"nombre": nombre, "bloque": bloque, "pendiente": ", ".join(pendientes), "clases_restantes": total_clases - hechas_clases})
    if not pendientes_ingles and obtener_progreso_ingles(planificacion) < 100:
        hechas = int(planificacion.get("clases_ingles_completadas", 30))
        pendientes_ingles.append({"nombre": "Inglés", "bloque": "INGLÉS", "pendiente": f"continuar desde la clase {hechas + 1}/102", "clases_restantes": max(0, 102 - hechas)})
    return pendientes_master, pendientes_ingles, pendientes_bonus


def sincronizar_tareas_automaticas(planificacion):
    """Marca como completadas las tareas automáticas cuyo módulo ya no tiene ese pendiente."""
    tareas = cargar_tareas(ARCHIVO_TAREAS)
    master, ingles, bonus = obtener_pendientes_academicos(planificacion)
    pendientes = {f"{item['bloque']}|{item['nombre']}" for item in master + ingles + bonus}
    cambio = False
    for tarea in tareas:
        clave = tarea.get("id_automatico")
        if clave and clave not in pendientes and not tarea.get("completada", False):
            tarea["completada"] = True
            cambio = True
    if cambio:
        guardar_tareas(tareas, ARCHIVO_TAREAS)


def generar_tareas_automaticas(planificacion):
    """Crea una tarea automática solo para el siguiente paso de cada módulo pendiente."""
    sincronizar_tareas_automaticas(planificacion)
    tareas = cargar_tareas(ARCHIVO_TAREAS)
    existentes = {t.get("id_automatico") for t in tareas if t.get("id_automatico")}
    master, ingles, bonus = obtener_pendientes_academicos(planificacion)
    candidatos = master[:1] + ingles[:1] + bonus[:1]
    creadas = 0
    for item in candidatos:
        clave = f"{item['bloque']}|{item['nombre']}"
        if clave in existentes:
            continue
        tareas.append({
            "nombre": f"{item['nombre']} · {item['pendiente']}",
            "fecha_limite": "",
            "prioridad": "Alta" if item in master else "Media",
            "categoria": item["bloque"],
            "completada": False,
            "tipo": "Plan automático",
            "id_automatico": clave,
        })
        creadas += 1
    if creadas:
        guardar_tareas(tareas, ARCHIVO_TAREAS)
    return creadas


def calcular_plan_diario(planificacion):
    """Distribuye las horas disponibles entre trabajo pendiente y descuenta lo ya realizado."""
    disponibilidad = planificacion.get("disponibilidad", {})
    master, ingles, bonus = obtener_pendientes_academicos(planificacion)
    bolsas = [("Máster", master), ("Inglés", ingles), ("Bonus", bonus)]
    resultado = []
    hoy = date.today()
    for i, dia in enumerate(DIAS_SEMANA):
        try:
            horas = max(0.0, float(disponibilidad.get(dia, 0) or 0))
        except (ValueError, TypeError):
            horas = 0.0
        fecha_dia = hoy + timedelta(days=(i - hoy.weekday()) % 7)
        realizadas = obtener_horas_del_dia(planificacion, fecha_dia)
        disponibles = max(0.0, horas - realizadas) if fecha_dia == hoy else horas
        if disponibles <= 0:
            actividad = "Tiempo ya utilizado / descanso"
        else:
            elegida = None
            for etiqueta, lista in bolsas:
                if lista:
                    elegida = (etiqueta, lista[0])
                    break
            if elegida:
                etiqueta, item = elegida
                bloques = max(1, int(round(disponibles)))
                actividad = f"{etiqueta} · {item['nombre']} · {item['pendiente']} · {bloques} h orientativas"
            else:
                actividad = "Repaso, apuntes o Proyecto de Fin de Máster"
        if fecha_dia == hoy:
            actividad = "HOY → " + actividad
        resultado.append((dia, actividad, horas))
    return resultado


def mostrar_plan_diario(contenido, planificacion):
    marco = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=15, pady=15)
    marco.pack(fill="x", pady=(15, 10))
    tk.Label(marco, text="Plan diario automático", font=("Helvetica", 18, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w")
    tk.Label(marco, text="La aplicación reparte tus horas disponibles y descuenta automáticamente el tiempo que ya has registrado.", font=("Helvetica", 12), fg="#555555", bg="#ffffff", wraplength=850, justify="left").pack(anchor="w", pady=(5, 10))
    for dia, actividad, horas in calcular_plan_diario(planificacion):
        fila = tk.Frame(marco, bg="#ffffff")
        fila.pack(fill="x", pady=4)
        tk.Label(fila, text=dia, width=13, anchor="w", font=("Helvetica", 12, "bold"), fg="#000000", bg="#ffffff").pack(side="left")
        tk.Label(fila, text=f"{horas:g} h", width=8, anchor="w", font=("Helvetica", 12, "bold"), fg="#222222", bg="#ffffff").pack(side="left")
        tk.Label(fila, text=actividad, anchor="w", font=("Helvetica", 12), fg="#333333", bg="#ffffff", wraplength=700, justify="left").pack(side="left", fill="x", expand=True)


def mostrar_plan_de_hoy(contenido):
    limpiar_contenido(contenido)
    planificacion = preparar_planificacion(cargar_planificacion())
    hoy = date.today()
    crear_titulo(contenido, "Plan de hoy", f"Qué hacer hoy · {hoy.strftime('%d/%m/%Y')}")

    dia_hoy = DIAS_SEMANA[hoy.weekday()]
    try:
        horas_hoy = max(0.0, float(planificacion.get("disponibilidad", {}).get(dia_hoy, 0) or 0))
    except (ValueError, TypeError):
        horas_hoy = 0.0
    realizadas = obtener_horas_del_dia(planificacion, hoy)
    restantes_hoy = max(0.0, horas_hoy - realizadas)

    tarjeta = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=20, pady=20)
    tarjeta.pack(fill="x", pady=(0, 15))
    tk.Label(tarjeta, text=f"{dia_hoy}: {horas_hoy:g} h disponibles", font=("Helvetica", 18, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w")
    tk.Label(tarjeta, text=f"Realizadas: {realizadas:g} h · Pendientes hoy: {restantes_hoy:g} h", font=("Helvetica", 13), fg="#333333", bg="#ffffff").pack(anchor="w", pady=(8, 0))

    master, ingles, bonus = obtener_pendientes_academicos(planificacion)
    tk.Label(tarjeta, text="Orden de prioridad", font=("Helvetica", 15, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w", pady=(18, 8))

    prioridades = []
    if master:
        prioridades.append(("1 · Máster", master[0]["nombre"], master[0]["pendiente"]))
    if ingles:
        prioridades.append(("2 · Inglés", ingles[0]["nombre"], ingles[0]["pendiente"]))
    if bonus:
        prioridades.append(("3 · Bonus", bonus[0]["nombre"], bonus[0]["pendiente"]))

    if not prioridades:
        prioridades.append(("✓ Todo registrado", "No quedan contenidos pendientes registrados", "Puedes dedicar el tiempo a repaso o al proyecto de fin de máster."))

    for nivel, nombre, detalle in prioridades:
        fila = tk.Frame(tarjeta, bg="#ffffff")
        fila.pack(fill="x", pady=4)
        tk.Label(fila, text=nivel, width=15, anchor="w", font=("Helvetica", 12, "bold"), fg="#000000", bg="#ffffff").pack(side="left")
        tk.Label(fila, text=f"{nombre} · {detalle}", anchor="w", font=("Helvetica", 12), fg="#333333", bg="#ffffff", wraplength=700, justify="left").pack(side="left", fill="x", expand=True)

    tareas = cargar_tareas(ARCHIVO_TAREAS)
    pendientes_tareas = [t for t in tareas if not t.get("completada", False)]
    pendientes_tareas.sort(key=lambda t: {"Alta": 0, "Media": 1, "Baja": 2}.get(t.get("prioridad", "Media"), 1))
    tk.Label(contenido, text="Tareas pendientes", font=("Helvetica", 18, "bold"), fg="#222222", bg="#f7f7f7").pack(anchor="w", pady=(10, 8))
    if pendientes_tareas:
        for tarea in pendientes_tareas[:5]:
            texto = f"{tarea.get('prioridad', 'Media')} · {tarea.get('nombre', 'Sin nombre')} · {tarea.get('categoria', 'General')}"
            tk.Label(contenido, text=texto, font=("Helvetica", 12), fg="#333333", bg="#ffffff", anchor="w", padx=12, pady=8).pack(fill="x", pady=2)
    else:
        tk.Label(contenido, text="No tienes tareas pendientes creadas.", font=("Helvetica", 12), fg="#555555", bg="#ffffff", padx=12, pady=10).pack(fill="x")

    tk.Label(contenido, text="Cómo registrar lo que haces", font=("Helvetica", 18, "bold"), fg="#222222", bg="#f7f7f7").pack(anchor="w", pady=(20, 8))
    tk.Label(contenido, text="Ve a Planificación → 'Registrar qué has hecho' y apunta la actividad, módulo, horas y horario. Así el planificador podrá comparar lo previsto con lo realizado.", font=("Helvetica", 12), fg="#555555", bg="#f7f7f7", wraplength=850, justify="left").pack(anchor="w")

def crear_calendario_meses(contenedor, planificacion):
    marco = tk.Frame(contenedor, bg="#f7f7f7")
    marco.pack(fill="x", pady=(20, 0))
    tk.Label(marco, text="Calendario hasta el objetivo", font=("Helvetica", 20, "bold"), fg="#222222", bg="#f7f7f7").pack(anchor="w", pady=(0, 15))
    objetivo = obtener_fecha_objetivo(planificacion)
    hoy = date.today()
    fecha_mes = date(hoy.year, hoy.month, 1)
    ultimo = date(objetivo.year, objetivo.month, 1)
    meses = []
    while fecha_mes <= ultimo:
        meses.append(fecha_mes)
        fecha_mes = date(fecha_mes.year + (1 if fecha_mes.month == 12 else 0), 1 if fecha_mes.month == 12 else fecha_mes.month + 1, 1)
    tarjetas = tk.Frame(marco, bg="#f7f7f7")
    tarjetas.pack(fill="x")
    for c in range(2):
        tarjetas.columnconfigure(c, weight=1)
    for indice, mes in enumerate(meses):
        tarjeta = tk.Frame(tarjetas, bg="#ffffff", relief="solid", borderwidth=1, padx=15, pady=15)
        tarjeta.grid(row=indice // 2, column=indice % 2, padx=5, pady=5, sticky="nsew")
        estado = "Mes actual" if (mes.year, mes.month) == (hoy.year, hoy.month) else ("Mes del objetivo" if (mes.year, mes.month) == (objetivo.year, objetivo.month) else "Planificación")
        tk.Label(tarjeta, text=f"{MESES[mes.month - 1]} {mes.year}", font=("Helvetica", 15, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w")
        tk.Label(tarjeta, text=estado, font=("Helvetica", 11), fg="#555555", bg="#ffffff").pack(anchor="w", pady=(5, 0))


def guardar_progreso_modulo(planificacion, clave, campo, entrada):
    try:
        valor = int(entrada.get())
        if valor < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Dato incorrecto", "Introduce un número entero válido.")
        return
    planificacion.setdefault("progreso_tema", {}).setdefault(clave, {})[campo] = valor
    guardar_planificacion_datos(planificacion)
    messagebox.showinfo("Guardado", "Progreso del temario guardado.")


def mostrar_temario(contenido):
    limpiar_contenido(contenido)
    planificacion = preparar_planificacion(cargar_planificacion())
    crear_titulo(contenido, "Temario", "Máster, inglés y bonus: contenido pendiente y progreso registrado")
    tk.Label(contenido, text=(f"Máster: {obtener_progreso_academico(planificacion):.0f}% · Inglés: {obtener_progreso_ingles(planificacion):.0f}% "
                              f"({planificacion.get('clases_ingles_completadas', 30)}/102 clases)"),
             font=("Helvetica", 14, "bold"), fg="#222222", bg="#f7f7f7").pack(anchor="w", pady=(0, 12))
    tk.Label(contenido, text="En cada módulo puedes indicar cuántas clases, tareas y evaluaciones llevas hechas. La aplicación conserva esos datos en planificacion.json.",
             font=("Helvetica", 12), fg="#555555", bg="#f7f7f7", wraplength=850, justify="left").pack(anchor="w", pady=(0, 15))

    for bloque, modulos in TEMARIO.items():
        encabezado = tk.Frame(contenido, bg="#e8e8e8", padx=12, pady=10)
        encabezado.pack(fill="x", pady=(12, 5))
        tk.Label(encabezado, text=bloque, font=("Helvetica", 16, "bold"), fg="#000000", bg="#e8e8e8").pack(anchor="w")
        for nombre, datos in modulos.items():
            clave = f"{bloque}|{nombre}"
            guardado = planificacion.get("progreso_tema", {}).get(clave, {})
            fila = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=10, pady=8)
            fila.pack(fill="x", pady=3)
            resumen = (f"{nombre}  ·  {datos.get('temas', 0)} temas  ·  {datos.get('clases', 0)} clases  ·  "
                       f"{datos.get('tareas', 0)} tareas  ·  {datos.get('evaluaciones', 0)} evaluaciones")
            tk.Label(fila, text=resumen, font=("Helvetica", 11, "bold"), fg="#222222", bg="#ffffff", anchor="w").grid(row=0, column=0, columnspan=6, sticky="w")
            if datos.get("estado"):
                tk.Label(fila, text=datos["estado"], font=("Helvetica", 10), fg="#555555", bg="#ffffff").grid(row=1, column=0, columnspan=6, sticky="w", pady=(3, 5))
            entradas = {}
            for col, (campo, etiqueta, maximo) in enumerate([
                ("clases", "Clases hechas", datos.get("clases", 0)),
                ("tareas", "Tareas hechas", datos.get("tareas", 0)),
                ("evaluaciones", "Evaluaciones hechas", datos.get("evaluaciones", 0)),
            ]):
                tk.Label(fila, text=etiqueta, font=("Helvetica", 9), fg="#555555", bg="#ffffff").grid(row=2, column=col * 2, sticky="w", pady=(4, 0))
                e = tk.Entry(fila, width=7, fg="#000000", bg="#ffffff")
                e.insert(0, str(guardado.get(campo, 0)))
                e.grid(row=3, column=col * 2, sticky="w", padx=(0, 8))
                entradas[campo] = e
            tk.Button(fila, text="Guardar", fg="#000000", bg="#eeeeee", activeforeground="#000000",
                      command=lambda k=clave, es=entradas: guardar_progreso_modulo_dict(planificacion, k, es)).grid(row=3, column=6, padx=8, sticky="e")
            fila.columnconfigure(6, weight=1)


def guardar_progreso_modulo_dict(planificacion, clave, entradas):
    datos = {}
    for campo, entrada in entradas.items():
        try:
            valor = int(entrada.get())
            if valor < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Dato incorrecto", "El progreso debe ser un número entero no negativo.")
            return
        datos[campo] = valor
    planificacion.setdefault("progreso_tema", {})[clave] = datos
    guardar_planificacion_datos(planificacion)
    messagebox.showinfo("Guardado", "Progreso del módulo guardado.")


def mostrar_planificacion(contenido):
    planificacion = preparar_planificacion(cargar_planificacion())
    generar_tareas_automaticas(planificacion)
    limpiar_contenido(contenido)
    crear_titulo(contenido, "Planificación", "Organiza tus semanas hasta el 31 de marzo de 2027")
    objetivo = obtener_fecha_objetivo(planificacion)
    semanas = calcular_semanas_restantes(objetivo)
    horas_semana = obtener_horas_registradas_semana(planificacion, obtener_semana_actual()[0])
    objetivo_semana = float(planificacion.get("horas_semanales_objetivo", 33.0))
    necesarias = calcular_horas_necesarias(planificacion, objetivo)

    panel = tk.Frame(contenido, bg="#f7f7f7")
    panel.pack(fill="x")
    for c in range(2):
        panel.columnconfigure(c, weight=1)
    tarjeta = tk.Frame(panel, bg="#ffffff", relief="solid", borderwidth=1, padx=20, pady=15)
    tarjeta.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    tk.Label(tarjeta, text="Fecha objetivo", fg="#555555", bg="#ffffff").pack(anchor="w")
    tk.Label(tarjeta, text=objetivo.strftime("%d/%m/%Y"), font=("Helvetica", 20, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w", pady=(5, 0))
    tarjeta2 = tk.Frame(panel, bg="#ffffff", relief="solid", borderwidth=1, padx=20, pady=15)
    tarjeta2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    tk.Label(tarjeta2, text="Objetivo semanal", fg="#555555", bg="#ffffff").pack(anchor="w")
    entrada_obj = tk.Entry(tarjeta2, width=10, fg="#000000", bg="#ffffff")
    entrada_obj.insert(0, str(planificacion.get("horas_semanales_objetivo", 33.0)))
    entrada_obj.pack(side="left", pady=(5, 0))
    tk.Button(tarjeta2, text="Guardar", fg="#000000", bg="#eeeeee", activeforeground="#000000",
              command=lambda: cambiar_objetivo_semanal(planificacion, entrada_obj)).pack(side="left", padx=10, pady=(5, 0))

    ritmo = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=20, pady=15)
    ritmo.pack(fill="x", pady=12)
    tk.Label(ritmo, text="Ritmo y situación", font=("Helvetica", 17, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w")
    texto = (f"Quedan aproximadamente {semanas} semanas.\n"
             f"Máster: {obtener_progreso_academico(planificacion):.0f}% · Inglés: {obtener_progreso_ingles(planificacion):.0f}%\n"
             f"Esta semana: {horas_semana:g} / {objetivo_semana:g} h.\n"
             f"Ritmo calculable necesario: {necesarias:.1f} h/semana cuando se haya indicado una estimación total del máster.")
    tk.Label(ritmo, text=texto, font=("Helvetica", 13), justify="left", fg="#333333", bg="#ffffff").pack(anchor="w", pady=(8, 0))

    disponibilidad = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=15, pady=15)
    disponibilidad.pack(fill="x", pady=(5, 10))
    tk.Label(disponibilidad, text="¿Cuántas horas tienes cada día esta semana?", font=("Helvetica", 17, "bold"), fg="#222222", bg="#ffffff").pack(anchor="w")
    entradas = {}
    fila = tk.Frame(disponibilidad, bg="#ffffff")
    fila.pack(fill="x", pady=10)
    for i, dia in enumerate(DIAS_SEMANA):
        celda = tk.Frame(fila, bg="#ffffff")
        celda.grid(row=0, column=i, padx=3, sticky="nsew")
        fila.columnconfigure(i, weight=1)
        tk.Label(celda, text=dia[:3], fg="#555555", bg="#ffffff").pack()
        e = tk.Entry(celda, width=7, justify="center", fg="#000000", bg="#ffffff")
        e.insert(0, str(planificacion.get("disponibilidad", {}).get(dia, 0)))
        e.pack(pady=3)
        entradas[dia] = e
    tk.Button(disponibilidad, text="Guardar disponibilidad y recalcular", fg="#000000", bg="#eeeeee", activeforeground="#000000",
              command=lambda: guardar_disponibilidad_y_refrescar(contenido, planificacion, entradas)).pack(anchor="w")

    mostrar_plan_diario(contenido, planificacion)

    crear_registro_actividad(contenido, planificacion)

    registro_manual = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=15, pady=15)
    registro_manual.pack(fill="x", pady=(0, 10))
    tk.Label(registro_manual, text="Registro rápido de horas de hoy", font=("Helvetica", 15, "bold"), fg="#222222", bg="#ffffff").pack(side="left")
    entrada_horas = tk.Entry(registro_manual, width=8, fg="#000000", bg="#ffffff")
    entrada_horas.pack(side="left", padx=10)
    tk.Button(registro_manual, text="Registrar", fg="#000000", bg="#eeeeee", activeforeground="#000000",
              command=lambda: registrar_horas_hoy(planificacion, entrada_horas)).pack(side="left")

    mostrar_historial_actividades(contenido, planificacion)
    crear_calendario_meses(contenido, planificacion)


def guardar_disponibilidad_y_refrescar(contenido, planificacion, entradas):
    disponibilidad = {}
    for dia, entrada in entradas.items():
        try:
            valor = float(entrada.get() or 0)
            if valor < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Dato incorrecto", f"Horas no válidas para {dia}.")
            return
        disponibilidad[dia] = valor
    planificacion["disponibilidad"] = disponibilidad
    guardar_planificacion_datos(planificacion)
    mostrar_planificacion(contenido)


def mostrar_progreso(contenido):
    limpiar_contenido(contenido)
    planificacion = preparar_planificacion(cargar_planificacion())
    tareas = cargar_tareas(ARCHIVO_TAREAS)
    completadas = sum(1 for tarea in tareas if tarea.get("completada", False))
    crear_titulo(contenido, "Progreso", "Tu progreso académico y tu tiempo real")
    marco = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=20, pady=20)
    marco.pack(fill="x")
    texto = (f"Máster: {obtener_progreso_academico(planificacion):.0f}%\n\n"
             f"Inglés: {obtener_progreso_ingles(planificacion):.0f}% ({planificacion.get('clases_ingles_completadas', 30)}/102 clases)\n\n"
             f"Tareas de la aplicación: {completadas}/{len(tareas)} completadas\n\n"
             f"Actividades registradas: {len(planificacion.get('actividades_realizadas', []))}")
    tk.Label(marco, text=texto, font=("Helvetica", 16), justify="left", fg="#222222", bg="#ffffff").pack(anchor="w")

    actividades = planificacion.get("actividades_realizadas", [])[-10:]
    if actividades:
        tk.Label(contenido, text="Últimas actividades", font=("Helvetica", 18, "bold"), fg="#222222", bg="#f7f7f7").pack(anchor="w", pady=(20, 10))
        for actividad in reversed(actividades):
            tk.Label(contenido, text=f"{actividad.get('fecha')} · {actividad.get('horas', 0)} h · {actividad.get('actividad')} · {actividad.get('modulo', '')}",
                     font=("Helvetica", 12), fg="#333333", bg="#ffffff", padx=10, pady=8, anchor="w").pack(fill="x", pady=2)


def mostrar_configuracion(contenido):
    limpiar_contenido(contenido)
    planificacion = preparar_planificacion(cargar_planificacion())
    crear_titulo(contenido, "Configuración", "Datos base de tu planificación")
    marco = tk.Frame(contenido, bg="#ffffff", relief="solid", borderwidth=1, padx=20, pady=20)
    marco.pack(fill="x")
    tk.Label(marco, text="Progreso actual del máster (%)", fg="#222222", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
    master = tk.Entry(marco, width=10, fg="#000000", bg="#ffffff")
    master.insert(0, str(planificacion.get("porcentaje_master", 35)))
    master.grid(row=0, column=1, sticky="w", padx=10)
    tk.Label(marco, text="Progreso actual de inglés (%)", fg="#222222", bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
    ingles = tk.Entry(marco, width=10, fg="#000000", bg="#ffffff")
    ingles.insert(0, str(planificacion.get("porcentaje_ingles", 29)))
    ingles.grid(row=1, column=1, sticky="w", padx=10)
    tk.Label(marco, text="Clases de inglés completadas", fg="#222222", bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
    clases = tk.Entry(marco, width=10, fg="#000000", bg="#ffffff")
    clases.insert(0, str(planificacion.get("clases_ingles_completadas", 30)))
    clases.grid(row=2, column=1, sticky="w", padx=10)
    tk.Label(marco, text="Estimación total de horas del máster", fg="#222222", bg="#ffffff").grid(row=3, column=0, sticky="w", pady=5)
    horas = tk.Entry(marco, width=10, fg="#000000", bg="#ffffff")
    horas.insert(0, str(planificacion.get("horas_totales_master", 0)))
    horas.grid(row=3, column=1, sticky="w", padx=10)
    tk.Button(marco, text="Guardar datos", fg="#000000", bg="#eeeeee", activeforeground="#000000",
              command=lambda: guardar_configuracion(planificacion, master, ingles, clases, horas)).grid(row=4, column=1, sticky="w", pady=12)


def guardar_configuracion(planificacion, master, ingles, clases, horas):
    try:
        pm = float(master.get()); pi = float(ingles.get()); ci = int(clases.get()); ht = float(horas.get())
        if not (0 <= pm <= 100 and 0 <= pi <= 100 and ci >= 0 and ht >= 0):
            raise ValueError
    except ValueError:
        messagebox.showerror("Dato incorrecto", "Revisa los valores introducidos.")
        return
    planificacion["porcentaje_master"] = pm
    planificacion["porcentaje_ingles"] = pi
    planificacion["clases_ingles_completadas"] = ci
    planificacion["horas_totales_master"] = ht
    guardar_planificacion_datos(planificacion)
    messagebox.showinfo("Guardado", "Datos actualizados.")


def crear_contenedor_scroll(ventana):
    """Crea una zona de contenido con scroll vertical y horizontal."""
    marco_externo = tk.Frame(ventana, bg="#f7f7f7")
    marco_externo.pack(side="right", fill="both", expand=True)

    canvas = tk.Canvas(marco_externo, bg="#f7f7f7", highlightthickness=0)
    scrollbar_y = tk.Scrollbar(marco_externo, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(marco_externo, orient="horizontal", command=canvas.xview)
    contenido = tk.Frame(canvas, bg="#f7f7f7", padx=40, pady=30)

    ventana_canvas = canvas.create_window((0, 0), window=contenido, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    def actualizar_scrollregion(_event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def ajustar_ancho(_event):
        # El contenido ocupa el ancho disponible, pero puede crecer horizontalmente
        # cuando una vista necesita más anchura.
        canvas.itemconfigure(ventana_canvas, width=max(contenido.winfo_reqwidth(), canvas.winfo_width()))
        actualizar_scrollregion()

    contenido.bind("<Configure>", actualizar_scrollregion)
    canvas.bind("<Configure>", ajustar_ancho)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    # Rueda del ratón / trackpad. Tkinter utiliza eventos distintos según macOS,
    # Windows y Linux, así que cubrimos los tres casos.
    def rueda_vertical(event):
        if getattr(event, "num", None) == 4:
            canvas.yview_scroll(-3, "units")
        elif getattr(event, "num", None) == 5:
            canvas.yview_scroll(3, "units")
        else:
            delta = event.delta
            if delta == 0:
                return
            unidades = max(1, abs(int(delta / 120)))
            canvas.yview_scroll(-unidades if delta > 0 else unidades, "units")

    def rueda_horizontal(event):
        delta = event.delta
        if delta == 0:
            return
        unidades = max(1, abs(int(delta / 120)))
        canvas.xview_scroll(-unidades if delta > 0 else unidades, "units")

    canvas.bind_all("<MouseWheel>", rueda_vertical)
    canvas.bind_all("<Shift-MouseWheel>", rueda_horizontal)
    canvas.bind_all("<Button-4>", rueda_vertical)
    canvas.bind_all("<Button-5>", rueda_vertical)

    # El contenido puede recibir foco para que la rueda funcione aunque el cursor
    # esté encima de una etiqueta, entrada o botón.
    canvas.focus_set()

    return contenido


def crear_ventana():
    ventana = tk.Tk()
    ventana.title("Conquer Planner")
    ventana.geometry("1100x750")
    ventana.minsize(900, 600)
    ventana.configure(bg="#f7f7f7")

    menu = tk.Frame(ventana, width=220, bg="#e8e8e8")
    menu.pack(side="left", fill="y")
    menu.pack_propagate(False)

    contenido = crear_contenedor_scroll(ventana)

    tk.Label(menu, text="CONQUER\nPLANNER", font=("Helvetica", 20, "bold"), fg="#222222", bg="#e8e8e8").pack(pady=(40, 35))

    botones = [
        ("Inicio", mostrar_inicio),
        ("Plan de hoy", mostrar_plan_de_hoy),
        ("Tareas", mostrar_tareas_en_interfaz),
        ("Temario", mostrar_temario),
        ("Planificación", mostrar_planificacion),
        ("Progreso", mostrar_progreso),
        ("Configuración", mostrar_configuracion),
    ]
    for texto, funcion in botones:
        tk.Button(menu, text=texto, width=20, fg="#000000", bg="#e8e8e8", activeforeground="#000000", activebackground="#d8d8d8",
                  relief="flat", command=lambda f=funcion: f(contenido)).pack(pady=5)

    mostrar_inicio(contenido)
    ventana.mainloop()


if __name__ == "__main__":
    crear_ventana()

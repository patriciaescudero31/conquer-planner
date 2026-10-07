import json
import math
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
from datetime import date, datetime, timedelta
from calendario import CalendarioAcademico
from tareas import cargar_tareas, guardar_tareas
from utilidades import calcular_horas_hasta_objetivo
from estadisticas import (
    horas_totales,
    horas_por_modulo,
    horas_ultima_semana
)
from planificador import (
    calcular_carga_pendiente,
    generar_planificacion,
    horas_registradas_por_fecha,
)


BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_TAREAS = BASE_DIR / "tareas.json"
ARCHIVO_PLANIFICACION = BASE_DIR / "planificacion.json"
ARCHIVO_TEMARIO = BASE_DIR / "temario.json"

DIAS_SEMANA = [
    "Lunes", "Martes", "Miércoles", "Jueves",
    "Viernes", "Sábado", "Domingo",
]

# ---------------------------------------------------------------------------
# Identidad visual
# ---------------------------------------------------------------------------
BG = "#f8fafc"
CARD = "#ffffff"
SIDEBAR = "#0f172a"
TEXT = "#111827"
MUTED = "#64748b"
BORDER = "#e2e8f0"
ACCENT = "#0d9488"
ACCENT_DARK = "#0f766e"
SUCCESS = "#10b981"
WARNING = "#f59e0b"
DANGER = "#ef4444"
SOFT_TEAL = "#ccfbf1"
SOFT_RED = "#fee2e2"
SOFT_AMBER = "#fef3c7"


# ---------------------------------------------------------------------------
# Catálogo académico. Los datos que cambian viven en planificacion.json.
# ---------------------------------------------------------------------------
CATALOGO = {
    "MÁSTER · PREWORK": {
        "Pseudocódigo": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "Linux y terminal": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "Python": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "GitHub": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "SQL": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "Creación de agentes · apuntes": {"temas": 0, "clases": 0, "tareas": 0, "evaluaciones": 0, "estado": "Completado"},
        "Google Antigravity": {"temas": 1, "clases": 10, "tareas": 0, "evaluaciones": 0, "apuntes": 10, "estado": "Clase semanal fija"},
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
    "INGLÉS": {
        "Unidades 1–9": {"temas": 9, "clases": 30, "tareas": 0, "evaluaciones": 0},
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
    "BONUS · FRONTEND": {
        "React con TypeScript": {"temas": 9, "clases": 16, "tareas": 0, "evaluaciones": 1},
        "Astro": {"temas": 9, "clases": 12, "tareas": 0, "evaluaciones": 1},
        "Angular": {"temas": 8, "clases": 8, "tareas": 0, "evaluaciones": 1},
        "Vue JS": {"temas": 5, "clases": 5, "tareas": 0, "evaluaciones": 0},
    },
    "BONUS · BACKEND": {
        "SQL avanzado": {"temas": 5, "clases": 14, "tareas": 0, "evaluaciones": 1},
        "WordPress": {"temas": 9, "clases": 22, "tareas": 1, "evaluaciones": 1},
        "Streamlit": {"temas": 3, "clases": 6, "tareas": 0, "evaluaciones": 1},
        "Java": {"temas": 5, "clases": 16, "tareas": 0, "evaluaciones": 1},
        "Node.js": {"temas": 6, "clases": 16, "tareas": 0, "evaluaciones": 0},
        "Rust": {"temas": 7, "clases": 14, "tareas": 0, "evaluaciones": 1},
        "Go": {"temas": 7, "clases": 8, "tareas": 0, "evaluaciones": 0},
        "Docker al completo": {"temas": 1, "clases": 20, "tareas": 0, "evaluaciones": 1},
    },
    "BONUS · PRODUCTIVIDAD": {
        "Productividad": {"temas": 1, "clases": 7, "tareas": 0, "evaluaciones": 0},
    },
    "BONUS · IA": {
        "IA para el desarrollo": {"temas": 3, "clases": 4, "tareas": 0, "evaluaciones": 0},
    },
}


def cargar_json(ruta, defecto):
    if not ruta.exists():
        return defecto
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return datos if isinstance(datos, type(defecto)) else defecto
    except (json.JSONDecodeError, OSError):
        return defecto


def guardar_json(ruta, datos):
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        return True
    except OSError:
        return False


def cargar_planificacion():
    datos = cargar_json(ARCHIVO_PLANIFICACION, {})
    disponibilidad = datos.get("disponibilidad")
    if not isinstance(disponibilidad, dict):
        disponibilidad = {}
    datos["disponibilidad"] = {
        dia: _numero_no_negativo(disponibilidad.get(dia), 0.0)
        for dia in DIAS_SEMANA
    }
    datos["horas_estimadas"] = _numero_no_negativo(datos.get("horas_estimadas"), 500.0)
    datos["porcentaje_master"] = min(
        100.0, _numero_no_negativo(datos.get("porcentaje_master"), 36.0)
    )
    datos["horas_semanales_objetivo"] = _numero_no_negativo(
        datos.get("horas_semanales_objetivo"), 35.0
    )
    estimaciones = datos.get("estimaciones")
    if not isinstance(estimaciones, dict):
        estimaciones = {}
    datos["estimaciones"] = {
        tipo: _numero_no_negativo(estimaciones.get(tipo), 1.0) or 1.0
        for tipo in (
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
    }

    try:
        clases_ingles = int(datos.get("clases_ingles_completadas", 41))
    except (TypeError, ValueError, OverflowError):
        clases_ingles = 41
    datos["clases_ingles_completadas"] = max(0, min(102, clases_ingles))

    try:
        datetime.strptime(str(datos.get("fecha_objetivo", "31/03/2027")), "%d/%m/%Y")
    except (TypeError, ValueError):
        datos["fecha_objetivo"] = "31/03/2027"
    horas_realizadas = datos.get("horas_realizadas")
    if not isinstance(horas_realizadas, dict):
        horas_realizadas = {}
    datos["horas_realizadas"] = {
        fecha: _numero_no_negativo(horas, 0.0)
        for fecha, horas in horas_realizadas.items()
    }
    if not isinstance(datos.get("actividades_realizadas"), list):
        datos["actividades_realizadas"] = []
    datos["actividades_realizadas"] = [
        actividad
        for actividad in datos["actividades_realizadas"]
        if isinstance(actividad, dict)
    ]
    if not isinstance(datos.get("progreso_tema"), dict):
        datos["progreso_tema"] = {}
    datos["progreso_tema"] = {
        clave: {
            campo: _entero_no_negativo(valor)
            for campo, valor in progreso.items()
        }
        for clave, progreso in datos["progreso_tema"].items()
        if isinstance(progreso, dict)
    }
    detalle_modulo = datos.get("detalle_modulo")
    if not isinstance(detalle_modulo, dict):
        detalle_modulo = {}
    else:
        detalle_modulo = {
            modulo: detalle
            for modulo, detalle in detalle_modulo.items()
            if isinstance(detalle, dict)
        }
    datos["detalle_modulo"] = detalle_modulo
    detalle_modulo.setdefault("HTML", {"tema_1": 7, "tema_2": 0})
    detalle_modulo.setdefault("Google Antigravity", {"apuntes": 6})
    detalle_modulo["HTML"]["tema_1"] = min(
        7, _entero_no_negativo(detalle_modulo["HTML"].get("tema_1"), 7)
    )
    detalle_modulo["HTML"]["tema_2"] = min(
        6, _entero_no_negativo(detalle_modulo["HTML"].get("tema_2"), 0)
    )
    detalle_modulo["Google Antigravity"]["apuntes"] = min(
        10, _entero_no_negativo(detalle_modulo["Google Antigravity"].get("apuntes"), 6)
    )
    datos["porcentaje_ingles"] = round(datos["clases_ingles_completadas"] / 102 * 100, 1)
    return datos


def aplicar_disponibilidad_semanal(planificacion, disponibilidad, domingo):
    if domingo.weekday() != 6:
        raise ValueError("La disponibilidad solo se actualiza los domingos.")
    if set(disponibilidad) != set(DIAS_SEMANA):
        raise ValueError("Debe indicarse la disponibilidad de todos los días.")
    horas_por_dia = {}
    for dia in DIAS_SEMANA:
        horas = float(disponibilidad[dia])
        if not math.isfinite(horas) or not 0 <= horas <= 24:
            raise ValueError("Las horas diarias deben estar entre 0 y 24.")
        horas_por_dia[dia] = horas
    planificacion["disponibilidad"] = horas_por_dia
    planificacion["horas_semanales_objetivo"] = round(
        sum(horas_por_dia.values()), 1
    )
    planificacion["ultima_revision_disponibilidad"] = domingo.isoformat()


def _numero_no_negativo(valor, defecto):
    try:
        numero = float(valor)
    except (TypeError, ValueError, OverflowError):
        return defecto
    if not math.isfinite(numero) or numero < 0:
        return defecto
    return numero


def _entero_no_negativo(valor, defecto=0):
    try:
        numero = int(valor)
    except (TypeError, ValueError, OverflowError):
        return defecto
    return max(0, numero)


def guardar_planificacion(planificacion):
    planificacion["porcentaje_ingles"] = round(
        max(0, min(102, int(planificacion.get("clases_ingles_completadas", 0)))) / 102 * 100,
        1,
    )
    return guardar_json(ARCHIVO_PLANIFICACION, planificacion)


def cargar_catalogo_local():
    """Devuelve los cambios locales del catálogo guardados en temario.json."""
    datos = cargar_json(ARCHIVO_TEMARIO, {})
    if not isinstance(datos, dict):
        datos = {}
    catalogo = datos.get("catalogo", {})
    if not isinstance(catalogo, dict):
        return {}
    cambios = {}
    for bloque, modulos in catalogo.items():
        if bloque not in CATALOGO or not isinstance(modulos, dict):
            continue
        for nombre, valores in modulos.items():
            if nombre not in CATALOGO[bloque] or not isinstance(valores, dict):
                continue
            normalizados = {}
            for campo in ("clases", "tareas", "evaluaciones"):
                if campo not in valores:
                    continue
                valor = valores[campo]
                if isinstance(valor, bool):
                    continue
                try:
                    entero = int(valor)
                except (TypeError, ValueError, OverflowError):
                    continue
                if entero >= 0 and str(entero) == str(valor).strip():
                    normalizados[campo] = entero
            estado = valores.get("estado")
            if estado in ("Completado", "Pendiente"):
                normalizados["estado"] = estado
            if normalizados:
                cambios.setdefault(bloque, {})[nombre] = normalizados
    return cambios


def aplicar_catalogo_local():
    for bloque, modulos in cargar_catalogo_local().items():
        for nombre, cambios in modulos.items():
            CATALOGO[bloque][nombre].update(cambios)


def guardar_catalogo_local(bloque, nombre, datos_modulo):
    datos = cargar_json(ARCHIVO_TEMARIO, {})
    if not isinstance(datos, dict):
        datos = {}
    catalogo = datos.get("catalogo")
    if not isinstance(catalogo, dict):
        catalogo = {}
    cambios = {
        campo: int(datos_modulo.get(campo, 0) or 0)
        for campo in ("clases", "tareas", "evaluaciones")
    }
    if "estado" in datos_modulo:
        cambios["estado"] = datos_modulo["estado"]
    modulos = catalogo.get(bloque)
    if not isinstance(modulos, dict):
        modulos = {}
        catalogo[bloque] = modulos
    modulos[nombre] = cambios
    datos["catalogo"] = catalogo
    return guardar_json(ARCHIVO_TEMARIO, datos)


def obtener_fecha_objetivo(planificacion):
    try:
        return datetime.strptime(planificacion.get("fecha_objetivo", "31/03/2027"), "%d/%m/%Y").date()
    except (ValueError, TypeError):
        return date(2027, 3, 31)


def progreso_modulo(planificacion, bloque, nombre, datos):
    if bloque == "INGLÉS" and nombre == "Unidades 1–9":
        progreso = planificacion.get("progreso_tema", {}).get(
            f"{bloque}|{nombre}", {}
        )
        hechas = min(
            30,
            _entero_no_negativo(
                progreso.get("clases", planificacion.get("clases_ingles_completadas", 0))
            ),
        )
        return 100.0 if hechas >= 30 else hechas / 30 * 100
    clave = f"{bloque}|{nombre}"
    guardado = planificacion.get("progreso_tema", {}).get(clave, {})
    partes = []
    for campo in ("clases", "tareas", "evaluaciones"):
        total = int(datos.get(campo, 0) or 0)
        if total:
            hechas = max(0, min(total, int(guardado.get(campo, 0) or 0)))
            partes.append((hechas, total))
    if not partes:
        return 100.0 if datos.get("estado") == "Completado" else 0.0
    return sum(hechas for hechas, _ in partes) / sum(total for _, total in partes) * 100


def estado_modulo(planificacion, bloque, nombre, datos):
    progreso = progreso_modulo(planificacion, bloque, nombre, datos)
    if progreso >= 100:
        return "Completado"
    if progreso > 0:
        return "En curso"
    if datos.get("estado"):
        return datos["estado"]
    return "Pendiente"


def pendientes_modulo(planificacion, bloque, nombre, datos):
    if bloque == "INGLÉS" and nombre == "Unidades 1–9":
        hechas = min(
            30,
            _entero_no_negativo(
                planificacion.get("progreso_tema", {})
                .get(f"{bloque}|{nombre}", {})
                .get("clases", planificacion.get("clases_ingles_completadas", 0))
            ),
        )
        return [f"clase {hechas + 1}/30"] if hechas < 30 else []
    if bloque == "MÁSTER · FRONTEND" and nombre == "HTML":
        detalle = planificacion.get("detalle_modulo", {}).get("HTML", {})
        tema1 = int(detalle.get("tema_1", 7) or 0)
        tema2 = int(detalle.get("tema_2", 0) or 0)
        pendientes = []
        if tema1 < 7:
            pendientes.append(f"Tema 1 · clase {tema1 + 1}/7")
        elif tema2 < 6:
            pendientes.append(f"Tema 2 · clase {tema2 + 1}/6")
        else:
            hechas = _entero_no_negativo(
                planificacion.get("progreso_tema", {})
                .get("MÁSTER · FRONTEND|HTML", {})
                .get("clases", 0)
            )
            if hechas < int(datos.get("clases", 0) or 0):
                pendientes.append(f"clase {hechas + 1}/{datos['clases']}")
        guardado = planificacion.get("progreso_tema", {}).get(
            "MÁSTER · FRONTEND|HTML", {}
        )
        for campo, etiqueta in (("tareas", "tarea"), ("evaluaciones", "evaluación")):
            total = int(datos.get(campo, 0) or 0)
            hechas = _entero_no_negativo(guardado.get(campo, 0))
            if hechas < total:
                pendientes.append(f"{etiqueta} {hechas + 1}/{total}")
        return pendientes
    clave = f"{bloque}|{nombre}"
    guardado = planificacion.get("progreso_tema", {}).get(clave, {})
    pendientes = []
    if nombre == "Google Antigravity":
        apuntes = int(planificacion.get("detalle_modulo", {}).get("Google Antigravity", {}).get("apuntes", 6) or 0)
        if apuntes < 10:
            pendientes.append(f"apuntes {apuntes + 1}/10")
    for campo, etiqueta in (("clases", "clase"), ("tareas", "tarea"), ("evaluaciones", "evaluación")):
        total = int(datos.get(campo, 0) or 0)
        hechas = max(0, min(total, int(guardado.get(campo, 0) or 0)))
        if total > hechas:
            pendientes.append(f"{etiqueta} {hechas + 1}/{total}")
    if not pendientes and datos.get("estado") and datos.get("estado") != "Completado":
        pendientes.append(str(datos["estado"]))
    return pendientes


def modulo_pendiente(planificacion, bloque, nombre, datos):
    return bool(pendientes_modulo(planificacion, bloque, nombre, datos))


def obtener_pendientes_por_prioridad(planificacion):
    master, ingles, bonus = [], [], []
    for bloque, modulos in CATALOGO.items():
        for nombre, datos in modulos.items():
            pendientes = pendientes_modulo(planificacion, bloque, nombre, datos)
            if not pendientes:
                continue
            item = {
                "bloque": bloque,
                "nombre": nombre,
                "pendiente": ", ".join(pendientes[:2]),
                "horas": max(1.0, min(4.0, len(pendientes))),
            }
            if bloque.startswith("MÁSTER"):
                master.append(item)
            elif bloque == "INGLÉS":
                ingles.append(item)
            elif bloque.startswith("BONUS"):
                bonus.append(item)
    orden_master = [
        "Google Antigravity", "HTML", "CSS", "JavaScript", "React JS",
        "Diseña con IA", "Django", "Agentes CLI", "Despliegue", "SEO",
        "Preparación de entrevistas", "Metodologías ágiles y Scrum",
        "Soft Skills", "Propuestas laborales", "Proyecto de Fin de Máster",
    ]
    posicion = {nombre: i for i, nombre in enumerate(orden_master)}
    if date.today().weekday() == 2:
        posicion["Google Antigravity"] = -1
    else:
        posicion["Google Antigravity"] = 50
    master.sort(key=lambda x: posicion.get(x["nombre"], 999))
    ingles.sort(key=lambda x: x["nombre"])
    bonus.sort(key=lambda x: x["nombre"])
    return master, ingles, bonus


def frontend_completo(planificacion):
    bloque = CATALOGO["MÁSTER · FRONTEND"]
    return all(progreso_modulo(planificacion, "MÁSTER · FRONTEND", n, d) >= 100 for n, d in bloque.items())


def master_completo(planificacion):
    for bloque, modulos in CATALOGO.items():
        if not bloque.startswith("MÁSTER"):
            continue
        if any(progreso_modulo(planificacion, bloque, n, d) < 100 for n, d in modulos.items()):
            return False
    return True


def bonus_desbloqueados(planificacion, bloque):
    if bloque == "BONUS · FRONTEND":
        return frontend_completo(planificacion)
    return master_completo(planificacion)


def obtener_pendientes_desbloqueados(planificacion):
    master, ingles, bonus = obtener_pendientes_por_prioridad(planificacion)
    bonus = [
        item for item in bonus
        if bonus_desbloqueados(planificacion, item["bloque"])
    ]
    return master, ingles, bonus


def obtener_horas_registradas_dia(planificacion, fecha):
    try:
        return max(0.0, float(planificacion.get("horas_realizadas", {}).get(fecha.isoformat(), 0) or 0))
    except (ValueError, TypeError):
        return 0.0


def obtener_horas_disponibles_semana(planificacion):
    return sum(max(0.0, float(planificacion.get("disponibilidad", {}).get(d, 0) or 0)) for d in DIAS_SEMANA)


def total_clases_ingles(planificacion):
    progreso = planificacion.get("progreso_tema", {})
    total = 0
    for nombre, datos in CATALOGO["INGLÉS"].items():
        clave = f"INGLÉS|{nombre}"
        guardado = progreso.get(clave, {})
        if nombre == "Unidades 1–9" and "clases" not in guardado:
            hechas = min(
                30,
                _entero_no_negativo(planificacion.get("clases_ingles_completadas", 0)),
            )
        else:
            hechas = _entero_no_negativo(guardado.get("clases", 0))
        total += min(int(datos.get("clases", 0) or 0), hechas)
    return min(102, total)


def establecer_clases_ingles(planificacion, clases):
    restantes = max(0, min(102, int(clases)))
    progreso = planificacion.setdefault("progreso_tema", {})
    for nombre, datos in CATALOGO["INGLÉS"].items():
        total = int(datos.get("clases", 0) or 0)
        if not total:
            continue
        clave = f"INGLÉS|{nombre}"
        guardado = progreso.setdefault(clave, {})
        hechas = min(total, restantes)
        guardado["clases"] = hechas
        restantes -= hechas
    planificacion["clases_ingles_completadas"] = max(
        0, min(102, int(clases))
    )


def obtener_capacidad_hasta_objetivo(planificacion):
    fecha_hoy = date.today()
    objetivo = obtener_fecha_objetivo(planificacion)
    if objetivo < fecha_hoy:
        return 0.0
    capacidad = calcular_horas_hasta_objetivo(planificacion, DIAS_SEMANA)
    horas_hoy = horas_registradas_por_fecha(planificacion).get(
        fecha_hoy.isoformat(), 0.0
    )
    return max(0.0, capacidad - horas_hoy)


def obtener_horas_realizadas_totales(planificacion):
    total = 0.0
    for valor in planificacion.get("horas_realizadas", {}).values():
        try:
            total += max(0.0, float(valor))
        except (ValueError, TypeError):
            pass
    return total


def horas_master_restantes(planificacion):
    total = max(0.0, float(planificacion.get("horas_estimadas", 0) or 0))
    porcentaje = max(0.0, min(100.0, float(planificacion.get("porcentaje_master", 0) or 0)))
    return total * (1 - porcentaje / 100)


def dias_restantes(planificacion):
    return max(0, (obtener_fecha_objetivo(planificacion) - date.today()).days)


def limpiar(contenido):
    for widget in contenido.winfo_children():
        widget.destroy()
    canvas = getattr(contenido, "_scroll_canvas", None)
    if canvas is not None:
        canvas.yview_moveto(0)


def titulo(contenido, texto, subtitulo=""):
    ttk.Label(contenido, text=texto, style="Title.TLabel").pack(anchor="w", pady=(0, 3))
    if subtitulo:
        ttk.Label(contenido, text=subtitulo, style="Subtitle.TLabel").pack(anchor="w", pady=(0, 22))


def tarjeta(parent, titulo_texto, valor, detalle="", color=TEXT):
    frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=16)
    frame.pack_propagate(False)
    tk.Label(frame, text=titulo_texto.upper(), font=("Helvetica", 10, "bold"), fg=MUTED, bg=CARD).pack(anchor="w")
    tk.Label(frame, text=valor, font=("Helvetica", 23, "bold"), fg=color, bg=CARD).pack(anchor="w", pady=(7, 2))
    if detalle:
        tk.Label(frame, text=detalle, font=("Helvetica", 10), fg=MUTED, bg=CARD, wraplength=260, justify="left").pack(anchor="w")
    return frame


def boton(parent, texto, comando, principal=False):
    normal = ACCENT if principal else CARD
    hover = ACCENT_DARK if principal else "#f1f5f9"
    widget = tk.Button(
        parent,
        text=texto,
        command=comando,
        font=("Helvetica", 10, "bold"),
        fg="#ffffff" if principal else TEXT,
        bg=normal,
        activeforeground="#ffffff" if principal else TEXT,
        activebackground=hover,
        relief="flat",
        bd=0,
        padx=12,
        pady=8,
        cursor="hand2",
    )
    widget.bind("<Enter>", lambda _event: widget.configure(bg=hover))
    widget.bind("<Leave>", lambda _event: widget.configure(bg=normal))
    return widget


def crear_scroll(parent):
    exterior = tk.Frame(parent, bg=BG)
    canvas = tk.Canvas(exterior, bg=BG, highlightthickness=0)
    barra = ttk.Scrollbar(exterior, orient="vertical", command=canvas.yview)
    contenido = tk.Frame(canvas, bg=BG, padx=34, pady=30)
    ventana = canvas.create_window((0, 0), window=contenido, anchor="nw")
    canvas.configure(yscrollcommand=barra.set)

    def actualizar(_=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def ancho(event):
        canvas.itemconfigure(ventana, width=event.width)

    contenido.bind("<Configure>", actualizar)
    canvas.bind("<Configure>", ancho)
    canvas.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")

    def rueda(event):
        if event.delta:
            pasos = event.delta if sys.platform == "darwin" else event.delta / 120
            if pasos:
                canvas.yview_scroll(-int(pasos), "units")

    canvas.bind_all("<MouseWheel>", rueda)
    if sys.platform.startswith("linux"):
        canvas.bind_all("<Button-4>", lambda _event: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda _event: canvas.yview_scroll(1, "units"))
    contenido._scroll_canvas = canvas
    exterior.pack(fill="both", expand=True)
    return contenido


class ConquerPlanner:
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
        style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Helvetica", 28, "bold"))
        style.configure("Subtitle.TLabel", background=BG, foreground=MUTED, font=("Helvetica", 12))
        style.configure("TEntry", padding=7)
        style.configure(
            "TCombobox",
            padding=7,
            font=("Helvetica", 10),
            fieldbackground=CARD,
            background=CARD,
            foreground=TEXT,
            arrowcolor=ACCENT_DARK,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", CARD), ("disabled", BG)],
            foreground=[("readonly", TEXT), ("disabled", MUTED)],
            selectbackground=[("readonly", CARD)],
            selectforeground=[("readonly", TEXT)],
        )
        style.configure("Horizontal.TProgressbar", troughcolor="#e2e8f0", background=ACCENT, bordercolor="#e2e8f0", lightcolor=ACCENT, darkcolor=ACCENT)

    def _construir_shell(self):
        self.sidebar = tk.Frame(self.ventana, bg=SIDEBAR, width=235)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = tk.Frame(self.sidebar, bg=SIDEBAR)
        logo.pack(fill="x", padx=22, pady=(28, 28))
        tk.Label(logo, text="CONQUER", font=("Helvetica", 18, "bold"), fg="#ffffff", bg=SIDEBAR).pack(anchor="w")
        tk.Label(logo, text="PLANNER", font=("Helvetica", 11, "bold"), fg="#5eead4", bg=SIDEBAR).pack(anchor="w")
        tk.Label(logo, text="Executive Academic Intelligence", font=("Helvetica", 8), fg="#94a3b8", bg=SIDEBAR).pack(anchor="w", pady=(5, 0))

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
        for icono, nombre, funcion in opciones:
            b = tk.Button(self.nav, text=f"  {icono}   {nombre}", command=funcion, anchor="w", font=("Helvetica", 11, "bold"), fg="#cbd5e1", bg=SIDEBAR, activeforeground="#ffffff", activebackground="#1e293b", relief="flat", bd=0, padx=8, pady=10, cursor="hand2")
            b.pack(fill="x", pady=2)

        objetivo = obtener_fecha_objetivo(self.planificacion)
        pie = tk.Frame(self.sidebar, bg="#111c31", padx=15, pady=14)
        pie.pack(side="bottom", fill="x", padx=12, pady=15)
        tk.Label(pie, text="OBJETIVO", font=("Helvetica", 8, "bold"), fg="#94a3b8", bg="#111c31").pack(anchor="w")
        tk.Label(pie, text=objetivo.strftime("%d/%m/%Y"), font=("Helvetica", 13, "bold"), fg="#ffffff", bg="#111c31").pack(anchor="w", pady=(3, 0))
        tk.Label(pie, text=f"{dias_restantes(self.planificacion)} días restantes", font=("Helvetica", 9), fg="#5eead4", bg="#111c31").pack(anchor="w", pady=(2, 0))

        self.main = tk.Frame(self.ventana, bg=BG)
        self.main.pack(side="right", fill="both", expand=True)
        self.contenido = crear_scroll(self.main)
        self.mostrar_inicio()
        self.ventana.after_idle(self._revisar_disponibilidad_dominical)

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
            font=("Helvetica", 17, "bold"),
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
            font=("Helvetica", 10),
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
                font=("Helvetica", 9, "bold"),
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
        tk.Label(diagnostico, text="DIAGNÓSTICO DE VIABILIDAD", font=("Helvetica", 10, "bold"), fg=MUTED, bg=CARD).pack(anchor="w")
        tk.Label(diagnostico, text=("Ritmo viable" if margen >= 20 else "Margen estrecho" if margen >= 0 else "Riesgo de retraso"), font=("Helvetica", 23, "bold"), fg=color, bg=CARD).pack(anchor="w", pady=(5, 2))
        tk.Label(diagnostico, text=f"Máster pendiente estimado: {master_restante:.1f} h · Capacidad restante: {capacidad:.1f} h · Margen: {margen:+.1f} h", font=("Helvetica", 12), fg=TEXT, bg=CARD).pack(anchor="w")
        tk.Label(
            diagnostico,
            text=(
                f"Ritmo mínimo: {ritmo_necesario:.1f} h/semana de máster · "
                f"Disponibilidad configurada: {ritmo_disponible:.1f} h/semana · "
                f"Quedan {semanas} semanas."
            ),
            font=("Helvetica", 10),
            fg=MUTED,
            bg=CARD,
        ).pack(anchor="w", pady=(6, 0))

        tk.Label(self.contenido, text="Siguiente acción", font=("Helvetica", 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(5, 10))
        self._mostrar_recomendacion(self.contenido)

        carga = calcular_carga_pendiente(CATALOGO, self.planificacion)
        tk.Label(
            self.contenido,
            text="Carga académica pendiente",
            font=("Helvetica", 18, "bold"),
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
            font=("Helvetica", 11),
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
        tk.Label(frame, text=nivel, font=("Helvetica", 9, "bold"), fg=ACCENT_DARK, bg=SOFT_TEAL, padx=8, pady=4).pack(anchor="w")
        tk.Label(frame, text=titulo_accion, font=("Helvetica", 17, "bold"), fg=TEXT, bg=CARD).pack(anchor="w", pady=(10, 2))
        tk.Label(frame, text=detalle, font=("Helvetica", 12), fg=MUTED, bg=CARD).pack(anchor="w")

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
        tk.Label(resumen, text=f"{restantes:.1f} h", font=("Helvetica", 32, "bold"), fg=ACCENT, bg=CARD).pack(anchor="w")
        tk.Label(resumen, text=f"de {horas:.1f} h disponibles hoy · {hechas:.1f} h ya registradas", font=("Helvetica", 11), fg=MUTED, bg=CARD).pack(anchor="w")

        tk.Label(
            self.contenido,
            text="Agenda de hoy",
            font=("Helvetica", 18, "bold"),
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
                    color = "#2563eb"
                elif asignacion["categoria"] == "Tarea":
                    color = "#7c3aed"
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
                font=("Helvetica", 11),
                fg=DANGER,
                bg=BG,
                wraplength=850,
                justify="left",
            ).pack(anchor="w", pady=8)
        elif restantes < 1:
            tk.Label(
                self.contenido,
                text="Ya has utilizado las horas disponibles de hoy.",
                font=("Helvetica", 11),
                fg=MUTED,
                bg=BG,
            ).pack(anchor="w", pady=8)
        else:
            tk.Label(
                self.contenido,
                text="No queda trabajo pendiente en el temario desbloqueado. Puedes registrar repaso, tutorías o trabajo del TFM.",
                font=("Helvetica", 11),
                fg=MUTED,
                bg=BG,
                wraplength=850,
                justify="left",
            ).pack(anchor="w", pady=8)

        tk.Label(self.contenido, text="Cómo se prioriza", font=("Helvetica", 17, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(22, 8))
        tk.Label(
            self.contenido,
            text="Las tareas manuales pendientes se programan primero, por prioridad Alta → Media → Baja. Cada una usa la estimación por tarea de Configuración; el tiempo restante se dedica al temario. Se mantienen la sesión semanal de Google Antigravity los miércoles, el inglés cuando cabe y los bonus después del contenido obligatorio.",
            font=("Helvetica", 11),
            fg=MUTED,
            bg=BG,
            wraplength=850,
            justify="left",
        ).pack(anchor="w")

    def _fila_plan(self, parent, numero, categoria, nombre, detalle, horas, color):
        frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=14)
        frame.pack(fill="x", pady=5)
        tk.Label(frame, text=numero, font=("Helvetica", 12, "bold"), fg="#ffffff", bg=color, width=3, pady=4).pack(side="left", padx=(0, 14))
        centro = tk.Frame(frame, bg=CARD)
        centro.pack(side="left", fill="x", expand=True)
        tk.Label(centro, text=categoria.upper(), font=("Helvetica", 9, "bold"), fg=color, bg=CARD).pack(anchor="w")
        tk.Label(centro, text=nombre, font=("Helvetica", 14, "bold"), fg=TEXT, bg=CARD).pack(anchor="w")
        tk.Label(centro, text=detalle, font=("Helvetica", 10), fg=MUTED, bg=CARD).pack(anchor="w")
        tk.Label(frame, text=f"{horas:.1f} h", font=("Helvetica", 16, "bold"), fg=TEXT, bg=CARD).pack(side="right")

    def mostrar_tareas(self):
        limpiar(self.contenido)
        titulo(self.contenido, "Tareas", "Las tareas manuales pendientes aparecen en el plan diario por prioridad; no se generan tareas duplicadas desde el temario.")
        tareas_originales = cargar_tareas(ARCHIVO_TAREAS)
        tareas = self._limpiar_duplicados_tareas(tareas_originales)
        if tareas != tareas_originales and not self._guardar_tareas(tareas):
            return

        form = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=18)
        form.pack(fill="x", pady=(0, 16))
        tk.Label(form, text="Nueva tarea personal", font=("Helvetica", 16, "bold"), fg=TEXT, bg=CARD).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))
        nombre = ttk.Entry(form)
        nombre.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 8))
        nombre.insert(0, "")
        categoria = ttk.Entry(form)
        categoria.grid(row=1, column=2, sticky="ew", padx=8)
        categoria.insert(0, "General")
        prioridad = ttk.Combobox(form, values=("Alta", "Media", "Baja"), state="readonly", width=10)
        prioridad.set("Media")
        prioridad.grid(row=1, column=3, padx=(8, 0))
        tk.Label(form, text="Tarea", font=("Helvetica", 9), fg=MUTED, bg=CARD).grid(row=2, column=0, sticky="w", pady=(4, 0))
        tk.Label(form, text="Categoría", font=("Helvetica", 9), fg=MUTED, bg=CARD).grid(row=2, column=2, sticky="w", padx=8, pady=(4, 0))
        boton(form, "Añadir", lambda: self._crear_tarea(nombre, categoria, prioridad), True).grid(row=1, column=4, padx=(12, 0))
        for c in range(3):
            form.columnconfigure(c, weight=1)

        pendientes = [t for t in tareas if not t.get("completada")]
        completadas = [t for t in tareas if t.get("completada")]
        tk.Label(self.contenido, text=f"Pendientes ({len(pendientes)})", font=("Helvetica", 17, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(4, 8))
        for i, tarea in enumerate(pendientes):
            self._fila_tarea(tarea, tareas.index(tarea))
        if completadas:
            tk.Label(self.contenido, text=f"Completadas ({len(completadas)})", font=("Helvetica", 17, "bold"), fg=MUTED, bg=BG).pack(anchor="w", pady=(22, 8))
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
        tk.Label(centro, text=f"{estado}  {tarea.get('nombre', '')}", font=("Helvetica", 12, "bold"), fg=color, bg=CARD, anchor="w").pack(anchor="w")
        tk.Label(centro, text=f"{tarea.get('categoria', 'General')} · prioridad {tarea.get('prioridad', 'Media')}", font=("Helvetica", 9), fg=MUTED, bg=CARD).pack(anchor="w", pady=(3, 0))
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
        tk.Label(marco, text="Editar tarea", font=("Helvetica", 18, "bold"), fg=TEXT, bg=CARD).pack(anchor="w", pady=(0, 14))
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
        aviso = tk.Frame(self.contenido, bg=SOFT_TEAL, highlightbackground="#99f6e4", highlightthickness=1, padx=18, pady=14)
        aviso.pack(fill="x", pady=(0, 18))
        tk.Label(aviso, text="ESTADO ACTUAL", font=("Helvetica", 9, "bold"), fg=ACCENT_DARK, bg=SOFT_TEAL).pack(anchor="w")
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
            font=("Helvetica", 11, "bold"),
            fg=TEXT,
            bg=SOFT_TEAL,
            wraplength=900,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

        for bloque, modulos in CATALOGO.items():
            cab = tk.Frame(self.contenido, bg=SIDEBAR, padx=15, pady=9)
            cab.pack(fill="x", pady=(12, 5))
            tk.Label(cab, text=bloque, font=("Helvetica", 13, "bold"), fg="#ffffff", bg=SIDEBAR).pack(anchor="w")
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
        tk.Label(top, text=nombre, font=("Helvetica", 12, "bold"), fg=TEXT, bg=CARD).pack(side="left")
        tk.Label(top, text=f"{estado} · {progreso:.0f}%", font=("Helvetica", 9, "bold"), fg=color, bg=CARD).pack(side="right")
        tk.Label(frame, text=f"{datos.get('clases', 0)} clases · {datos.get('tareas', 0)} tareas · {datos.get('evaluaciones', 0)} evaluaciones", font=("Helvetica", 9), fg=MUTED, bg=CARD).pack(anchor="w", pady=(3, 7))
        if nombre == "Google Antigravity":
            apuntes = self.planificacion["detalle_modulo"]["Google Antigravity"]["apuntes"]
            clases = _entero_no_negativo(guardado.get("clases", 0))
            estado_apuntes = "apuntes pendientes" if apuntes < 10 else "apuntes completados"
            tk.Label(
                frame,
                text=f"Clases: {clases}/10 · apuntes: {apuntes}/10 · {estado_apuntes}",
                font=("Helvetica", 9, "bold"),
                fg=WARNING if apuntes < 10 or clases < 10 else SUCCESS,
                bg=CARD,
            ).pack(anchor="w", pady=(0, 7))
        if nombre == "HTML":
            detalle = self.planificacion["detalle_modulo"]["HTML"]
            tk.Label(frame, text=f"Tema 1: {detalle.get('tema_1', 7)}/7 · Tema 2: {detalle.get('tema_2', 0)}/6", font=("Helvetica", 9, "bold"), fg=ACCENT, bg=CARD).pack(anchor="w", pady=(0, 7))
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
            tk.Label(celda, text=etiqueta, font=("Helvetica", 8), fg=MUTED, bg=CARD).pack(anchor="w")
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
                tk.Label(celda, text=etiqueta, font=("Helvetica", 8), fg=MUTED, bg=CARD).pack(anchor="w")
                entrada = ttk.Entry(celda, width=7)
                entrada.insert(0, str(detalle.get(campo, 0)))
                entrada.pack()
                entradas[campo] = entrada
        if nombre == "Google Antigravity":
            detalle = self.planificacion.setdefault("detalle_modulo", {}).setdefault("Google Antigravity", {"apuntes": 6})
            celda = tk.Frame(frame, bg=CARD)
            celda.pack(anchor="w", pady=(8, 0))
            tk.Label(celda, text="Apuntes hechos / 10", font=("Helvetica", 8), fg=MUTED, bg=CARD).pack(anchor="w")
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
                font=("Helvetica", 9),
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
            font=("Helvetica", 17, "bold"),
            fg=TEXT,
            bg=CARD,
        ).pack(anchor="w", pady=(0, 6))
        tk.Label(
            marco,
            text=bloque,
            font=("Helvetica", 10),
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
                font=("Helvetica", 10, "bold"),
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
            font=("Helvetica", 10),
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
        tk.Label(ritmo, text="RITMO NECESARIO", font=("Helvetica", 9, "bold"), fg=MUTED, bg=CARD).pack(anchor="w")
        tk.Label(ritmo, text=f"{necesario:.1f} h/semana de máster", font=("Helvetica", 21, "bold"), fg=TEXT, bg=CARD).pack(anchor="w", pady=(4, 2))
        tk.Label(ritmo, text=f"Disponibilidad semanal configurada: {semanal:.1f} h · {semanas} semanas aproximadas.", font=("Helvetica", 10), fg=MUTED, bg=CARD).pack(anchor="w")

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
            highlightbackground="#fecaca" if fuera_objetivo > 0 else "#99f6e4",
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
            font=("Helvetica", 10, "bold"),
            fg=estado_color,
            bg=estado_plan["bg"],
            wraplength=900,
            justify="left",
        ).pack(anchor="w")

        tk.Label(self.contenido, text="Disponibilidad semanal", font=("Helvetica", 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(5, 8))
        disponibilidad = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=16, pady=16)
        disponibilidad.pack(fill="x")
        entradas = {}
        for dia in DIAS_SEMANA:
            celda = tk.Frame(disponibilidad, bg=CARD)
            celda.pack(side="left", fill="x", expand=True, padx=3)
            tk.Label(celda, text=dia[:3], font=("Helvetica", 9, "bold"), fg=MUTED, bg=CARD).pack()
            entrada = ttk.Entry(celda, width=7, justify="center")
            entrada.insert(0, str(self.planificacion.get("disponibilidad", {}).get(dia, 0)))
            entrada.pack(pady=(5, 0))
            entradas[dia] = entrada
        boton(disponibilidad, "Guardar disponibilidad", lambda: self._guardar_disponibilidad(entradas), True).pack(anchor="e", pady=(12, 0))

        tk.Label(self.contenido, text="Registro de estudio", font=("Helvetica", 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(24, 8))
        self._registro_estudio()

        tk.Label(self.contenido, text="Plan de la semana", font=("Helvetica", 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(24, 8))
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
                font=("Helvetica", 10, "bold"),
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
                tk.Label(fila, text=texto, font=("Helvetica", 10), fg=TEXT, bg=CARD, anchor="w").pack(side="left", fill="x", expand=True)
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
            tk.Label(fila, text=f"{dia[:3]} {fecha.strftime('%d/%m')}", width=12, anchor="w", font=("Helvetica", 10, "bold"), fg=TEXT, bg=CARD).pack(side="left")
            horas_planificadas = sum(item["horas"] for item in asignaciones)
            tk.Label(fila, text=f"{horas_planificadas:.1f}/{horas:.1f} h", width=9, anchor="w", font=("Helvetica", 10, "bold"), fg=ACCENT, bg=CARD).pack(side="left")
            tk.Label(fila, text=texto, anchor="w", font=("Helvetica", 10), fg=MUTED, bg=CARD).pack(side="left", fill="x", expand=True)

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

        tk.Label(self.contenido, text="Hitos actuales", font=("Helvetica", 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(22, 8))
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
            tk.Label(fila, text="●", font=("Helvetica", 12), fg=color, bg=CARD).pack(side="left", padx=(0, 9))
            tk.Label(fila, text=nombre, font=("Helvetica", 11, "bold"), fg=TEXT, bg=CARD, width=22, anchor="w").pack(side="left")
            tk.Label(fila, text=detalle, font=("Helvetica", 10), fg=MUTED, bg=CARD, anchor="w").pack(side="left", fill="x", expand=True)

        objetivo = obtener_fecha_objetivo(self.planificacion)
        capacidad = obtener_capacidad_hasta_objetivo(self.planificacion)
        restante = horas_master_restantes(self.planificacion)
        tk.Label(self.contenido, text="Viabilidad hasta el objetivo", font=("Helvetica", 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(22, 8))
        frame = tk.Frame(self.contenido, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=18)
        frame.pack(fill="x")
        tk.Label(frame, text=f"Te quedan {restante:.1f} h estimadas de máster hasta el {objetivo.strftime('%d/%m/%Y')}. La capacidad disponible configurada es de {capacidad:.1f} h.", font=("Helvetica", 12), fg=TEXT, bg=CARD, wraplength=900, justify="left").pack(anchor="w")

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
            tk.Label(frame, text=etiqueta, font=("Helvetica", 10, "bold"), fg=TEXT, bg=CARD).grid(row=fila, column=0, sticky="w", pady=7)
            entrada = ttk.Entry(frame, width=20)
            entrada.insert(0, valor)
            entrada.grid(row=fila, column=1, sticky="w", padx=18, pady=7)
            campos[clave] = entrada
        boton(frame, "Guardar configuración", lambda: self._guardar_configuracion(campos), True).grid(row=len(definiciones), column=1, sticky="w", pady=(12, 0))

        info = tk.Frame(self.contenido, bg=SOFT_AMBER, highlightbackground="#fde68a", highlightthickness=1, padx=18, pady=15)
        info.pack(fill="x", pady=18)
        tk.Label(info, text="Cómo se genera la planificación", font=("Helvetica", 13, "bold"), fg=TEXT, bg=SOFT_AMBER).pack(anchor="w")
        tk.Label(info, text="• Cada tipo de actividad tiene su estimación editable. Al registrar una sesión, el campo de horas se rellena con la estimación del tipo elegido.\n• Los tiempos reales de las últimas cinco sesiones del mismo módulo y tipo ajustan automáticamente la previsión de las actividades del temario.\n• El plan asigna primero las tareas manuales Alta → Media → Baja y reserva el tiempo disponible restante para el temario hasta la fecha objetivo.\n• El máster ocupa primero el tiempo académico; mientras siga pendiente, se planifica además una actividad diaria de inglés si cabe.\n• Registrar una clase, tarea o evaluación actualiza el progreso correspondiente; una clase de HTML también avanza su siguiente lección y un registro de TFM actualiza su tarea.\n• Antigravity se planifica los miércoles con la disponibilidad restante. Los bonus se planifican después del contenido obligatorio.\n• El porcentaje global del máster es una estimación manual; se recalcula el tiempo pendiente al cambiarlo.", font=("Helvetica", 10), fg=TEXT, bg=SOFT_AMBER, justify="left").pack(anchor="w", pady=(7, 0))

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

        tk.Label(self.contenido, text="Horas por módulo", font=("Helvetica", 18, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(25, 10))

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
            tk.Label(fila, text=nombre, font=("Helvetica", 11, "bold"), bg=CARD, fg=TEXT).pack(side="left")
            tk.Label(fila, text=f"{horas:.1f} h", font=("Helvetica", 11), bg=CARD, fg=ACCENT).pack(side="right")
    def ejecutar(self):
        self.ventana.mainloop()


def crear_ventana():
    ConquerPlanner().ejecutar()


if __name__ == "__main__":
    crear_ventana()

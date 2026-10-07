import json
import math
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path

from copias_seguridad import (
    ErrorCopiaSeguridad,
    crear_copia_antes_de_guardar,
)
from planificador import (
    calcular_carga_pendiente,
    generar_planificacion,
    horas_registradas_por_fecha,
)
from utilidades import calcular_horas_hasta_objetivo

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_TAREAS = BASE_DIR / "tareas.json"
ARCHIVO_PLANIFICACION = BASE_DIR / "planificacion.json"
ARCHIVO_TEMARIO = BASE_DIR / "temario.json"

DIAS_SEMANA = [
    "Lunes", "Martes", "Miércoles", "Jueves",
    "Viernes", "Sábado", "Domingo",
]

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
CATALOGO_INICIAL = deepcopy(CATALOGO)


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
        crear_copia_antes_de_guardar(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        return True
    except (OSError, ErrorCopiaSeguridad) as error:
        print(f"Error al guardar «{ruta.name}»: {error}")
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
    for bloque, modulos in CATALOGO_INICIAL.items():
        for nombre, datos in modulos.items():
            CATALOGO[bloque][nombre].clear()
            CATALOGO[bloque][nombre].update(deepcopy(datos))
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

__all__ = [
    "BASE_DIR",
    "ARCHIVO_TAREAS",
    "ARCHIVO_PLANIFICACION",
    "ARCHIVO_TEMARIO",
    "DIAS_SEMANA",
    "CATALOGO",
    "CATALOGO_INICIAL",
    "cargar_json",
    "guardar_json",
    "cargar_planificacion",
    "aplicar_disponibilidad_semanal",
    "guardar_planificacion",
    "cargar_catalogo_local",
    "aplicar_catalogo_local",
    "guardar_catalogo_local",
    "obtener_fecha_objetivo",
    "progreso_modulo",
    "estado_modulo",
    "pendientes_modulo",
    "modulo_pendiente",
    "obtener_pendientes_por_prioridad",
    "frontend_completo",
    "master_completo",
    "bonus_desbloqueados",
    "obtener_pendientes_desbloqueados",
    "obtener_horas_registradas_dia",
    "obtener_horas_disponibles_semana",
    "total_clases_ingles",
    "establecer_clases_ingles",
    "obtener_capacidad_hasta_objetivo",
    "obtener_horas_realizadas_totales",
    "horas_master_restantes",
    "dias_restantes"
] + ["_numero_no_negativo", "_entero_no_negativo"]

from datetime import date, datetime, timedelta
import math
from statistics import median


DIAS_SEMANA = (
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
)


def _entero(valor):
    try:
        return max(0, int(valor or 0))
    except (TypeError, ValueError, OverflowError):
        return 0


def _progreso_modulo(planificacion, bloque, nombre):
    progreso = planificacion.get("progreso_tema", {}).get(
        f"{bloque}|{nombre}", {}
    )
    return progreso if isinstance(progreso, dict) else {}


def _horas_estimadas(
    planificacion,
    tipo,
    modulo=None,
    bloque=None,
    defecto=None,
):
    tipo_sesion = {
        "clase": "clase",
        "apuntes": "apuntes",
        "tarea": "tarea",
        "evaluacion": "evaluación",
        "clase_apuntes": "clase + apuntes",
        "tfm": "tfm",
    }[tipo]
    sesiones = planificacion.get("actividades_realizadas", [])
    if not isinstance(sesiones, list):
        sesiones = []
    especificas = []
    globales = []
    for sesion in sesiones:
        if not isinstance(sesion, dict):
            continue
        if str(sesion.get("tipo", "")).strip().casefold() != tipo_sesion:
            continue
        try:
            horas = float(sesion.get("horas", 0) or 0)
        except (TypeError, ValueError, OverflowError):
            continue
        if not math.isfinite(horas) or horas <= 0:
            continue
        globales.append(horas)
        if (
            modulo
            and sesion.get("modulo") == modulo
            and (not bloque or sesion.get("bloque") == bloque)
        ):
            especificas.append(horas)
    muestras = especificas if modulo else globales
    if muestras:
        return float(median(muestras[-5:]))

    estimaciones = planificacion.get("estimaciones", {})
    if not isinstance(estimaciones, dict):
        estimaciones = {}
    if defecto is not None:
        return defecto
    try:
        horas = float(estimaciones.get(tipo, 1.0))
    except (TypeError, ValueError, OverflowError):
        return 1.0
    return horas if math.isfinite(horas) and horas > 0 else 1.0


def _trabajo_modulo(planificacion, bloque, nombre, datos):
    progreso = _progreso_modulo(planificacion, bloque, nombre)
    acciones = []

    if nombre == "Google Antigravity":
        clases = min(10, _entero(progreso.get("clases")))
        apuntes = min(
            10,
            _entero(
                planificacion.get("detalle_modulo", {})
                .get("Google Antigravity", {})
                .get("apuntes", 6)
            ),
        )
        for numero in range(max(clases, apuntes) + 1, 11):
            partes = []
            if clases < numero:
                partes.append(f"clase {numero}/10")
            if apuntes < numero:
                partes.append(f"apuntes {numero}/10")
            acciones.append(
                (
                    " + ".join(partes),
                    _horas_estimadas(
                        planificacion,
                        "clase_apuntes",
                        nombre,
                        bloque,
                        max(
                            _horas_estimadas(
                                planificacion, "clase", nombre, bloque
                            ),
                            _horas_estimadas(
                                planificacion,
                                "apuntes",
                                nombre,
                                bloque,
                            ),
                        ),
                    ),
                )
            )
        return acciones

    total_clases = _entero(datos.get("clases"))
    if bloque == "INGLÉS" and nombre == "Unidades 1–9":
        clases_hechas = min(
            30,
            _entero(planificacion.get("clases_ingles_completadas", 0)),
        )
    else:
        clases_hechas = min(total_clases, _entero(progreso.get("clases")))

    clases_html_detalladas = 0
    if bloque == "MÁSTER · FRONTEND" and nombre == "HTML":
        detalle = planificacion.get("detalle_modulo", {}).get("HTML", {})
        tema_1 = min(7, _entero(detalle.get("tema_1", 7)))
        tema_2 = min(6, _entero(detalle.get("tema_2", 0)))
        for tema, hechas, total in (
            (1, tema_1, 7),
            (2, tema_2, 6),
        ):
            for numero in range(hechas + 1, total + 1):
                if clases_html_detalladas >= total_clases - clases_hechas:
                    break
                acciones.append(
                    (
                        f"Tema {tema} · clase {numero}/{total}",
                        _horas_estimadas(
                            planificacion, "clase", nombre, bloque
                        ),
                    )
                )
                clases_html_detalladas += 1

    for numero in range(
        clases_hechas + clases_html_detalladas + 1,
        total_clases + 1,
    ):
        acciones.append(
            (
                f"clase {numero}/{total_clases}",
                _horas_estimadas(
                    planificacion, "clase", nombre, bloque
                ),
            )
        )

    for campo, etiqueta, tipo_estimacion in (
        (
            "tareas",
            "tarea",
            "tfm" if nombre == "Proyecto de Fin de Máster" else "tarea",
        ),
        ("evaluaciones", "evaluación", "evaluacion"),
    ):
        total = _entero(datos.get(campo))
        hechas = min(total, _entero(progreso.get(campo)))
        for numero in range(hechas + 1, total + 1):
            acciones.append(
                (
                    f"{etiqueta} {numero}/{total}",
                    _horas_estimadas(
                        planificacion, tipo_estimacion, nombre, bloque
                    ),
                )
            )
    return acciones


def _cola_trabajo(catalogo, planificacion, incluir_bonuses_futuros=False):
    cola = []
    frontal = all(
        not _trabajo_modulo(planificacion, "MÁSTER · FRONTEND", nombre, datos)
        for nombre, datos in catalogo.get("MÁSTER · FRONTEND", {}).items()
    )
    master = all(
        not _trabajo_modulo(planificacion, bloque, nombre, datos)
        for bloque, modulos in catalogo.items()
        if bloque.startswith("MÁSTER")
        for nombre, datos in modulos.items()
    )

    for bloque, modulos in catalogo.items():
        if bloque.startswith("BONUS"):
            desbloqueado = master or (
                bloque == "BONUS · FRONTEND" and frontal
            )
            if not desbloqueado and not incluir_bonuses_futuros:
                continue
        categoria = (
            "Máster"
            if bloque.startswith("MÁSTER")
            else "Inglés"
            if bloque == "INGLÉS"
            else "Bonus"
        )
        for nombre, datos in modulos.items():
            for accion, horas in _trabajo_modulo(
                planificacion, bloque, nombre, datos
            ):
                cola.append(
                    {
                        "categoria": categoria,
                        "bloque": bloque,
                        "modulo": nombre,
                        "detalle": accion,
                        "horas": horas,
                    }
                )
    return cola


def _cola_tareas(tareas, planificacion):
    prioridades = {"Alta": 0, "Media": 1, "Baja": 2}
    pendientes = []
    for posicion, tarea in enumerate(tareas or []):
        if not isinstance(tarea, dict) or tarea.get("completada"):
            continue
        nombre = str(tarea.get("nombre", "")).strip()
        if not nombre:
            continue
        prioridad = tarea.get("prioridad", "Media")
        if prioridad not in prioridades:
            prioridad = "Media"
        categoria = str(tarea.get("categoria", "General")).strip() or "General"
        horas = estimar_horas_tarea(tarea, planificacion)
        pendientes.append(
            (
                prioridades[prioridad],
                posicion,
                {
                    "categoria": "Tarea",
                    "bloque": "Tareas personales",
                    "modulo": nombre,
                    "detalle": f"Prioridad {prioridad} · {categoria}",
                    "horas": horas,
                },
            )
        )
    pendientes.sort(key=lambda item: (item[0], item[1]))
    return [trabajo for _, _, trabajo in pendientes]


def estimar_horas_tarea(tarea, planificacion):
    try:
        horas = float(str(tarea.get("horas", "")).replace(",", "."))
    except (TypeError, ValueError, OverflowError):
        horas = 0.0
    if not math.isfinite(horas) or horas <= 0:
        horas = _horas_estimadas(planificacion, "tarea")
    return horas


def horas_registradas_por_fecha(planificacion):
    resultado = {}
    for fecha, horas in planificacion.get("horas_realizadas", {}).items():
        try:
            valor = max(0.0, float(horas or 0))
        except (TypeError, ValueError, OverflowError):
            continue
        resultado[fecha] = valor
    for actividad in planificacion.get("actividades_realizadas", []):
        try:
            fecha = date.fromisoformat(actividad.get("fecha", "")).isoformat()
            horas = max(0.0, float(actividad.get("horas", 0) or 0))
        except (AttributeError, TypeError, ValueError, OverflowError):
            continue
        resultado[fecha] = max(resultado.get(fecha, 0.0), horas)
    return resultado


def generar_planificacion(catalogo, planificacion, fecha_inicio=None, tareas=None):
    """Reparte trabajo pendiente en los huecos disponibles hasta el objetivo."""
    inicio = fecha_inicio or date.today()
    try:
        objetivo = datetime.strptime(
            planificacion.get("fecha_objetivo", "31/03/2027"),
            "%d/%m/%Y",
        ).date()
    except (TypeError, ValueError):
        objetivo = date(2027, 3, 31)
    if objetivo < inicio:
        return {}

    disponibilidad = planificacion.get("disponibilidad", {})
    registradas = horas_registradas_por_fecha(planificacion)
    cola = _cola_trabajo(catalogo, planificacion, incluir_bonuses_futuros=True)
    cola_tareas = _cola_tareas(tareas, planificacion)
    calendario = {}
    fecha = inicio

    while fecha <= objetivo and (cola or cola_tareas):
        clave_fecha = fecha.isoformat()
        dia = DIAS_SEMANA[fecha.weekday()]
        try:
            capacidad = max(0.0, float(disponibilidad.get(dia, 0) or 0))
        except (TypeError, ValueError, OverflowError):
            capacidad = 0.0
        capacidad = max(0.0, capacidad - registradas.get(clave_fecha, 0.0))
        asignaciones = []

        def asignar(categoria, limite, permitir_antigravity=False, trabajos=None):
            nonlocal capacidad
            cola_asignacion = cola if trabajos is None else trabajos
            asignadas = 0.0
            while capacidad > 0 and asignadas < limite:
                presupuesto = min(capacidad, limite - asignadas)
                siguiente = next(
                    (
                        posicion
                        for posicion, trabajo in enumerate(cola_asignacion)
                        if (
                            trabajo["categoria"] == categoria
                            and (
                                permitir_antigravity
                                or trabajo["modulo"] != "Google Antigravity"
                            )
                            and trabajo["horas"] <= presupuesto
                        )
                    ),
                    None,
                )
                if siguiente is None:
                    break
                trabajo = cola_asignacion.pop(siguiente)
                asignaciones.append(trabajo.copy())
                capacidad -= trabajo["horas"]
                asignadas += trabajo["horas"]
            return asignadas

        asignar("Tarea", capacidad, trabajos=cola_tareas)

        if dia == "Miércoles" and capacidad > 0:
            antigravity = next(
                (
                    posicion
                    for posicion, trabajo in enumerate(cola)
                    if (
                        trabajo["modulo"] == "Google Antigravity"
                        and trabajo["horas"] <= capacidad
                    )
                ),
                None,
            )
            if antigravity is not None:
                trabajo = cola.pop(antigravity)
                asignaciones.append(trabajo.copy())
                capacidad -= trabajo["horas"]

        master_pendiente = any(item["categoria"] == "Máster" for item in cola)
        ingles_pendiente = any(item["categoria"] == "Inglés" for item in cola)
        reserva_ingles = 0.0
        if master_pendiente and ingles_pendiente:
            reserva_ingles = next(
                (
                    item["horas"]
                    for item in cola
                    if item["categoria"] == "Inglés"
                    and item["horas"] <= capacidad
                ),
                0.0,
            )

        asignar("Máster", max(0.0, capacidad - reserva_ingles))
        if reserva_ingles:
            asignar("Inglés", reserva_ingles)
        asignar("Máster", capacidad)
        if not any(item["categoria"] == "Máster" for item in cola):
            asignar("Inglés", capacidad)
        if not any(
            item["categoria"] in ("Máster", "Inglés") for item in cola
        ):
            asignar("Bonus", capacidad)

        if asignaciones:
            agrupadas = []
            for asignacion in asignaciones:
                if (
                    agrupadas
                    and agrupadas[-1]["categoria"] == asignacion["categoria"]
                    and agrupadas[-1]["modulo"] == asignacion["modulo"]
                ):
                    agrupadas[-1]["horas"] += asignacion["horas"]
                    agrupadas[-1]["detalles"].append(asignacion["detalle"])
                else:
                    agrupadas.append(
                        {
                            "categoria": asignacion["categoria"],
                            "bloque": asignacion["bloque"],
                            "modulo": asignacion["modulo"],
                            "horas": asignacion["horas"],
                            "detalles": [asignacion["detalle"]],
                        }
                    )
            calendario[clave_fecha] = agrupadas
        if not cola and not cola_tareas:
            break
        fecha += timedelta(days=1)

    return calendario


def calcular_carga_pendiente(
    catalogo,
    planificacion,
    incluir_bonuses_futuros=False,
):
    cola = _cola_trabajo(
        catalogo,
        planificacion,
        incluir_bonuses_futuros=incluir_bonuses_futuros,
    )
    por_categoria = {}
    for trabajo in cola:
        categoria = trabajo["categoria"]
        por_categoria[categoria] = por_categoria.get(categoria, 0.0) + trabajo["horas"]
    return por_categoria

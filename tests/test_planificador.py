from datetime import date

from planificador import (
    _trabajo_modulo,
    calcular_carga_pendiente,
    generar_planificacion,
)


CATALOGO_PRUEBA = {
    "MÁSTER · PREWORK": {
        "Google Antigravity": {"clases": 10},
    },
    "MÁSTER · FRONTEND": {
        "HTML": {"clases": 2, "tareas": 1, "evaluaciones": 0},
    },
    "INGLÉS": {
        "Unidad 10": {"clases": 2, "tareas": 0, "evaluaciones": 0},
    },
    "BONUS · FRONTEND": {
        "Astro": {"clases": 1, "tareas": 0, "evaluaciones": 0},
    },
}


def _planificacion():
    return {
        "fecha_objetivo": "08/10/2026",
        "disponibilidad": {
            "Lunes": 0,
            "Martes": 0,
            "Miércoles": 3,
            "Jueves": 5,
            "Viernes": 0,
            "Sábado": 0,
            "Domingo": 0,
        },
        "horas_realizadas": {},
        "actividades_realizadas": [],
        "progreso_tema": {
            "MÁSTER · PREWORK|Google Antigravity": {"clases": 6},
            "MÁSTER · FRONTEND|HTML": {"clases": 1},
            "INGLÉS|Unidad 10": {"clases": 1},
        },
        "detalle_modulo": {"Google Antigravity": {"apuntes": 6}},
    }


def test_plan_diario_reserva_una_hora_de_antigravity_el_miercoles():
    calendario = generar_planificacion(
        CATALOGO_PRUEBA,
        _planificacion(),
        date(2026, 10, 7),
    )

    miercoles = calendario["2026-10-07"]
    antigravity = next(
        asignacion
        for asignacion in miercoles
        if asignacion["modulo"] == "Google Antigravity"
    )
    assert antigravity["horas"] == 1
    assert antigravity["detalles"] == ["clase 7/10 + apuntes 7/10"]
    assert sum(asignacion["horas"] for asignacion in miercoles) == 3


def test_planificador_prioriza_master_antes_de_ingles_y_bonus():
    calendario = generar_planificacion(
        CATALOGO_PRUEBA,
        _planificacion(),
        date(2026, 10, 8),
    )

    jueves = calendario["2026-10-08"]
    assert [asignacion["modulo"] for asignacion in jueves] == ["HTML", "Unidad 10"]
    assert sum(item["horas"] for item in jueves) == 3
    assert all(asignacion["categoria"] != "Bonus" for asignacion in jueves)


def test_planificador_usa_estimaciones_y_descuenta_horas_registradas():
    planificacion = _planificacion()
    planificacion["fecha_objetivo"] = "07/10/2026"
    planificacion["estimaciones"] = {"clase": 2, "apuntes": 1, "tarea": 1, "evaluacion": 1}
    planificacion["horas_realizadas"] = {"2026-10-07": 1}

    calendario = generar_planificacion(
        CATALOGO_PRUEBA,
        planificacion,
        date(2026, 10, 7),
    )

    assert calendario["2026-10-07"] == [
        {
            "categoria": "Máster",
            "bloque": "MÁSTER · PREWORK",
            "modulo": "Google Antigravity",
            "horas": 2,
            "detalles": ["clase 7/10 + apuntes 7/10"],
        }
    ]


def test_carga_pendiente_no_cuenta_bonus_bloqueados():
    carga = calcular_carga_pendiente(CATALOGO_PRUEBA, _planificacion())

    assert "Bonus" not in carga
    assert carga["Máster"] == 6
    assert carga["Inglés"] == 1


def test_planificador_no_asigna_mas_horas_que_la_disponibilidad():
    planificacion = _planificacion()
    planificacion["fecha_objetivo"] = "07/10/2026"
    planificacion["disponibilidad"]["Miércoles"] = 1

    calendario = generar_planificacion(
        CATALOGO_PRUEBA,
        planificacion,
        date(2026, 10, 7),
    )

    assert sum(item["horas"] for item in calendario["2026-10-07"]) == 1


def test_bonus_se_programa_despues_de_completar_master_e_ingles():
    planificacion = _planificacion()
    planificacion["fecha_objetivo"] = "07/10/2026"
    planificacion["progreso_tema"].update(
        {
            "MÁSTER · PREWORK|Google Antigravity": {"clases": 10},
            "MÁSTER · FRONTEND|HTML": {"clases": 2, "tareas": 1},
            "INGLÉS|Unidad 10": {"clases": 2},
        }
    )
    planificacion["detalle_modulo"]["Google Antigravity"]["apuntes"] = 10

    calendario = generar_planificacion(
        CATALOGO_PRUEBA,
        planificacion,
        date(2026, 10, 7),
    )

    categorias = [
        item["categoria"]
        for item in calendario["2026-10-07"]
    ]
    assert categorias == ["Bonus"]


def test_estimaciones_distintas_cambian_la_duracion_del_plan():
    planificacion = _planificacion()
    planificacion["fecha_objetivo"] = "08/10/2026"
    planificacion["progreso_tema"]["MÁSTER · FRONTEND|HTML"]["tareas"] = 1
    planificacion["estimaciones"] = {
        "clase": 2,
        "apuntes": 1,
        "tarea": 1,
        "evaluacion": 1,
    }

    calendario = generar_planificacion(
        CATALOGO_PRUEBA,
        planificacion,
        date(2026, 10, 8),
    )

    html = next(
        item
        for item in calendario["2026-10-08"]
        if item["modulo"] == "HTML"
    )
    assert html["horas"] == 2


def test_plan_html_muestra_el_tema_y_la_leccion_reales():
    catalogo = {
        "MÁSTER · FRONTEND": {
            "HTML": {"clases": 27, "tareas": 2, "evaluaciones": 3},
        },
    }
    planificacion = {
        "progreso_tema": {
            "MÁSTER · FRONTEND|HTML": {
                "clases": 8,
                "tareas": 0,
                "evaluaciones": 0,
            },
        },
        "detalle_modulo": {
            "HTML": {"tema_1": 7, "tema_2": 0},
        },
    }

    acciones = _trabajo_modulo(
        planificacion,
        "MÁSTER · FRONTEND",
        "HTML",
        catalogo["MÁSTER · FRONTEND"]["HTML"],
    )

    assert acciones[0][0] == "Tema 2 · clase 1/6"
    assert len(acciones) == (27 - 8) + 2 + 3


def test_tiempos_reales_recalculan_estimacion_del_modulo():
    planificacion = _planificacion()
    planificacion["fecha_objetivo"] = "08/10/2026"
    planificacion["actividades_realizadas"] = [
        {
            "tipo": "Clase",
            "bloque": "MÁSTER · FRONTEND",
            "modulo": "HTML",
            "horas": 2,
        },
        {
            "tipo": "Clase",
            "bloque": "MÁSTER · FRONTEND",
            "modulo": "HTML",
            "horas": 3,
        },
    ]

    calendario = generar_planificacion(
        CATALOGO_PRUEBA,
        planificacion,
        date(2026, 10, 8),
    )

    html = next(
        item
        for item in calendario["2026-10-08"]
        if item["modulo"] == "HTML"
    )
    assert html["horas"] == 3.5


def test_planifica_tareas_manuales_por_prioridad_y_omite_completadas():
    planificacion = {
        "fecha_objetivo": "08/10/2026",
        "disponibilidad": {"Jueves": 3},
        "estimaciones": {"tarea": 1},
    }
    tareas = [
        {"nombre": "Tarea baja", "prioridad": "Baja", "categoria": "Casa"},
        {"nombre": "Tarea alta", "prioridad": "Alta", "categoria": "Estudio"},
        {
            "nombre": "Ya terminada",
            "prioridad": "Alta",
            "completada": True,
        },
        {"nombre": "Tarea media", "prioridad": "Media", "categoria": "Trabajo"},
    ]

    calendario = generar_planificacion(
        {},
        planificacion,
        date(2026, 10, 8),
        tareas,
    )

    asignaciones = calendario["2026-10-08"]
    assert [item["modulo"] for item in asignaciones] == [
        "Tarea alta",
        "Tarea media",
        "Tarea baja",
    ]
    assert [item["categoria"] for item in asignaciones] == ["Tarea"] * 3
    assert [item["detalles"] for item in asignaciones] == [
        ["Prioridad Alta · Estudio"],
        ["Prioridad Media · Trabajo"],
        ["Prioridad Baja · Casa"],
    ]


def test_tareas_ocupan_primero_el_dia_y_el_tiempo_restante_se_asigna_al_temario():
    catalogo = {
        "MÁSTER · FRONTEND": {
            "HTML": {"clases": 1, "tareas": 0, "evaluaciones": 0},
        },
    }
    planificacion = {
        "fecha_objetivo": "08/10/2026",
        "disponibilidad": {"Jueves": 2},
        "estimaciones": {"tarea": 1, "clase": 1},
        "progreso_tema": {},
    }

    calendario = generar_planificacion(
        catalogo,
        planificacion,
        date(2026, 10, 8),
        [{"nombre": "Entregar formulario", "prioridad": "Alta"}],
    )

    assert [item["modulo"] for item in calendario["2026-10-08"]] == [
        "Entregar formulario",
        "HTML",
    ]
    assert sum(item["horas"] for item in calendario["2026-10-08"]) == 2

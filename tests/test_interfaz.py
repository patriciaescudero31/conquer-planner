import json
import tkinter as tk
from datetime import date, timedelta

import interfaz
from estadisticas import horas_ultima_semana
from planificador import _trabajo_modulo
import pytest


def _progreso_completo(bloques):
    planificacion = {
        "clases_ingles_completadas": 41,
        "progreso_tema": {},
        "detalle_modulo": {
            "HTML": {"tema_1": 7, "tema_2": 6},
            "Google Antigravity": {"apuntes": 10},
        },
    }
    for bloque, modulos in bloques.items():
        for nombre, datos in modulos.items():
            progreso = {
                campo: datos.get(campo, 0)
                for campo in ("clases", "tareas", "evaluaciones")
                if datos.get(campo, 0)
            }
            if progreso:
                planificacion["progreso_tema"][f"{bloque}|{nombre}"] = progreso
    return planificacion


def test_bonus_frontend_se_desbloquea_al_completar_frontend():
    planificacion = _progreso_completo(
        {"MÁSTER · FRONTEND": interfaz.CATALOGO["MÁSTER · FRONTEND"]}
    )

    _, _, bonus = interfaz.obtener_pendientes_desbloqueados(planificacion)

    assert bonus
    assert {item["bloque"] for item in bonus} == {"BONUS · FRONTEND"}


def test_resto_de_bonus_se_desbloquea_al_completar_master():
    bloques_master = {
        bloque: modulos
        for bloque, modulos in interfaz.CATALOGO.items()
        if bloque.startswith("MÁSTER")
    }
    planificacion = _progreso_completo(bloques_master)

    assert interfaz.master_completo(planificacion)
    _, _, bonus = interfaz.obtener_pendientes_desbloqueados(planificacion)

    assert {item["bloque"] for item in bonus} == {
        bloque for bloque in interfaz.CATALOGO if bloque.startswith("BONUS")
    }


def test_cargar_planificacion_repara_campos_invalidos(tmp_path, monkeypatch):
    archivo = tmp_path / "planificacion.json"
    archivo.write_text(
        json.dumps(
            {
                "disponibilidad": {"Lunes": 3, "Martes": "inválido", "Miércoles": -2},
                "horas_estimadas": float("inf"),
                "porcentaje_master": 150,
                "clases_ingles_completadas": 200,
                "horas_realizadas": [],
                "actividades_realizadas": [None, {"actividad": "estudio"}],
                "progreso_tema": {"HTML": None},
                "detalle_modulo": {"HTML": None},
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(interfaz, "ARCHIVO_PLANIFICACION", archivo)

    planificacion = interfaz.cargar_planificacion()

    assert planificacion["disponibilidad"]["Lunes"] == 3
    assert planificacion["disponibilidad"]["Martes"] == 0
    assert planificacion["disponibilidad"]["Miércoles"] == 0
    assert planificacion["disponibilidad"]["Domingo"] == 0
    assert planificacion["horas_estimadas"] == 500
    assert planificacion["porcentaje_master"] == 100
    assert planificacion["clases_ingles_completadas"] == 102
    assert planificacion["horas_realizadas"] == {}
    assert planificacion["actividades_realizadas"] == [{"actividad": "estudio"}]
    assert planificacion["progreso_tema"] == {}
    assert planificacion["detalle_modulo"]["HTML"] == {"tema_1": 7, "tema_2": 0}
    assert set(planificacion["estimaciones"]) == {
        "clase",
        "apuntes",
        "clase_apuntes",
        "tarea",
        "evaluacion",
        "tutoria",
        "clase_directo",
        "practica",
        "tfm",
    }


def test_horas_ultima_semana_usa_ventana_de_siete_dias():
    hoy = date.today()
    actividades = [
        {"fecha": hoy.isoformat(), "horas": 2},
        {"fecha": (hoy - timedelta(days=6)).isoformat(), "horas": 1.5},
        {"fecha": (hoy - timedelta(days=7)).isoformat(), "horas": 10},
        {"fecha": (hoy + timedelta(days=1)).isoformat(), "horas": 20},
        {"fecha": hoy.isoformat(), "horas": "inválido"},
    ]

    assert horas_ultima_semana(actividades) == 3.5


def test_establecer_clases_ingles_distribuye_progreso_por_unidad():
    planificacion = {"progreso_tema": {}}

    interfaz.establecer_clases_ingles(planificacion, 41)

    progreso = planificacion["progreso_tema"]
    assert progreso["INGLÉS|Unidades 1–9"]["clases"] == 30
    assert progreso["INGLÉS|Unidad 10"]["clases"] == 4
    assert progreso["INGLÉS|Unidad 11"]["clases"] == 3
    assert progreso["INGLÉS|Unidad 12"]["clases"] == 4
    assert interfaz.total_clases_ingles(planificacion) == 41


def test_contenedor_principal_se_muestra_en_la_ventana():
    try:
        ventana = tk.Tk()
    except tk.TclError as error:
        pytest.skip(f"Tk no está disponible: {error}")

    try:
        ventana.geometry("800x600")
        contenido = interfaz.crear_scroll(ventana)
        interfaz.titulo(contenido, "Pantalla visible")
        ventana.update()

        exterior = contenido.master.master
        assert exterior.winfo_manager() == "pack"
        assert exterior.winfo_width() > 1
        assert exterior.winfo_height() > 1
        assert contenido.winfo_children()[0].winfo_viewable()
    finally:
        ventana.destroy()


def test_registro_de_clase_html_avanza_y_revertir_sesion_restablece_tema():
    app = interfaz.ConquerPlanner.__new__(interfaz.ConquerPlanner)
    app.planificacion = {
        "progreso_tema": {
            "MÁSTER · FRONTEND|HTML": {"clases": 8},
        },
        "detalle_modulo": {
            "HTML": {"tema_1": 7, "tema_2": 0},
        },
    }
    sesion = {
        "bloque": "MÁSTER · FRONTEND",
        "modulo": "HTML",
        "tipo": "Clase",
    }

    sesion["progreso_aplicado"] = app._aplicar_progreso_sesion(sesion)

    assert app.planificacion["progreso_tema"][
        "MÁSTER · FRONTEND|HTML"
    ]["clases"] == 9
    assert app.planificacion["detalle_modulo"]["HTML"]["tema_2"] == 1
    assert _trabajo_modulo(
        app.planificacion,
        "MÁSTER · FRONTEND",
        "HTML",
        interfaz.CATALOGO["MÁSTER · FRONTEND"]["HTML"],
    )[0][0] == "Tema 2 · clase 2/6"

    app._revertir_progreso_sesion(sesion)

    assert app.planificacion["progreso_tema"][
        "MÁSTER · FRONTEND|HTML"
    ]["clases"] == 8
    assert app.planificacion["detalle_modulo"]["HTML"]["tema_2"] == 0


def test_registro_tfm_avanza_la_tarea_del_proyecto():
    app = interfaz.ConquerPlanner.__new__(interfaz.ConquerPlanner)
    app.planificacion = {"progreso_tema": {}, "detalle_modulo": {}}

    cambios = app._aplicar_progreso_sesion(
        {
            "bloque": "MÁSTER · DESARROLLO PROFESIONAL",
            "modulo": "Proyecto de Fin de Máster",
            "tipo": "TFM",
        }
    )

    assert cambios["antes"] == {"tareas": 0}
    assert app.planificacion["progreso_tema"][
        "MÁSTER · DESARROLLO PROFESIONAL|Proyecto de Fin de Máster"
    ]["tareas"] == 1


def test_estimacion_de_tfm_usa_el_valor_configurado():
    planificacion = {
        "estimaciones": {"tfm": 4.5},
        "actividades_realizadas": [],
        "progreso_tema": {},
    }
    catalogo = {
        "MÁSTER · DESARROLLO PROFESIONAL": {
            "Proyecto de Fin de Máster": {
                "clases": 0,
                "tareas": 1,
                "evaluaciones": 0,
            },
        },
    }

    trabajos = _trabajo_modulo(
        planificacion,
        "MÁSTER · DESARROLLO PROFESIONAL",
        "Proyecto de Fin de Máster",
        catalogo["MÁSTER · DESARROLLO PROFESIONAL"][
            "Proyecto de Fin de Máster"
        ],
    )

    assert trabajos == [("tarea 1/1", 4.5)]

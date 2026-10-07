import json
import tkinter as tk
from copy import deepcopy
from datetime import date, timedelta

import interfaz
from calendario import CalendarioAcademico
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


def test_catalogo_local_permite_definir_totales_y_estado_del_prework(
    tmp_path,
    monkeypatch,
):
    archivo = tmp_path / "temario.json"
    archivo.write_text(
        json.dumps({"hitos": ["mantener"]}),
        encoding="utf-8",
    )
    monkeypatch.setattr(interfaz, "ARCHIVO_TEMARIO", archivo)

    assert interfaz.guardar_catalogo_local(
        "MÁSTER · PREWORK",
        "Pseudocódigo",
        {
            "clases": 12,
            "tareas": 2,
            "evaluaciones": 1,
            "estado": "Pendiente",
        },
    )

    contenido = json.loads(archivo.read_text(encoding="utf-8"))
    assert contenido["hitos"] == ["mantener"]
    assert interfaz.cargar_catalogo_local() == {
        "MÁSTER · PREWORK": {
            "Pseudocódigo": {
                "clases": 12,
                "tareas": 2,
                "evaluaciones": 1,
                "estado": "Pendiente",
            }
        }
    }


def test_catalogo_local_ignora_totales_invalidos(tmp_path, monkeypatch):
    archivo = tmp_path / "temario.json"
    archivo.write_text(
        json.dumps(
            {
                "catalogo": {
                    "MÁSTER · PREWORK": {
                        "Pseudocódigo": {
                            "clases": -1,
                            "tareas": "no es un número",
                            "evaluaciones": 2,
                            "estado": "desconocido",
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(interfaz, "ARCHIVO_TEMARIO", archivo)

    assert interfaz.cargar_catalogo_local() == {
        "MÁSTER · PREWORK": {
            "Pseudocódigo": {"evaluaciones": 2}
        }
    }


def test_aplicar_catalogo_local_actualiza_totales_y_estado(
    tmp_path,
    monkeypatch,
):
    archivo = tmp_path / "temario.json"
    archivo.write_text(
        json.dumps(
            {
                "catalogo": {
                    "MÁSTER · PREWORK": {
                        "Pseudocódigo": {
                            "clases": 8,
                            "tareas": 1,
                            "evaluaciones": 0,
                            "estado": "Pendiente",
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(interfaz, "ARCHIVO_TEMARIO", archivo)
    monkeypatch.setattr(interfaz, "CATALOGO", deepcopy(interfaz.CATALOGO))

    interfaz.aplicar_catalogo_local()

    datos = interfaz.CATALOGO["MÁSTER · PREWORK"]["Pseudocódigo"]
    assert datos["clases"] == 8
    assert datos["tareas"] == 1
    assert interfaz.progreso_modulo(
        {"progreso_tema": {}},
        "MÁSTER · PREWORK",
        "Pseudocódigo",
        datos,
    ) == 0
    assert len(
        _trabajo_modulo(
            {},
            "MÁSTER · PREWORK",
            "Pseudocódigo",
            datos,
        )
    ) == 9


def test_seccion_sin_actividades_puede_marcarse_completada():
    datos = {
        "clases": 0,
        "tareas": 0,
        "evaluaciones": 0,
        "estado": "Completado",
    }

    assert interfaz.progreso_modulo(
        {"progreso_tema": {}},
        "MÁSTER · PREWORK",
        "Pseudocódigo",
        datos,
    ) == 100
    assert interfaz.estado_modulo(
        {"progreso_tema": {}},
        "MÁSTER · PREWORK",
        "Pseudocódigo",
        datos,
    ) == "Completado"


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


def test_estilo_visual_aplica_tipografia_y_botones_legibles():
    try:
        ventana = tk.Tk()
    except tk.TclError as error:
        pytest.skip(f"Tk no está disponible: {error}")

    try:
        app = interfaz.ConquerPlanner.__new__(interfaz.ConquerPlanner)
        app.ventana = ventana
        app._configurar_estilos()
        estilo = interfaz.ttk.Style(ventana)
        fuente_titulo = estilo.lookup("Title.TLabel", "font")

        assert interfaz.FONT_FAMILY in fuente_titulo
        assert estilo.lookup("Treeview", "background") == interfaz.CARD

        boton_principal = interfaz.boton(
            ventana,
            "Guardar",
            lambda: None,
            principal=True,
        )
        boton_secundario = interfaz.boton(
            ventana,
            "Cancelar",
            lambda: None,
        )
        assert boton_principal.cget("bg") == interfaz.ACCENT
        assert boton_principal.cget("activebackground") == interfaz.ACCENT_DARK
        assert boton_secundario.cget("bg") == interfaz.CARD
        assert int(boton_secundario.cget("highlightthickness")) == 1
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


def test_disponibilidad_dominical_actualiza_todos_los_dias():
    planificacion = {}
    domingo = date(2026, 10, 11)
    disponibilidad = {
        "Lunes": 5,
        "Martes": 4,
        "Miércoles": 3,
        "Jueves": 2,
        "Viernes": 1,
        "Sábado": 0,
        "Domingo": 0,
    }

    interfaz.aplicar_disponibilidad_semanal(
        planificacion,
        disponibilidad,
        domingo,
    )

    assert planificacion["disponibilidad"] == disponibilidad
    assert planificacion["horas_semanales_objetivo"] == 15
    assert planificacion["ultima_revision_disponibilidad"] == "2026-10-11"


def test_disponibilidad_dominical_rechaza_datos_invalidos_sin_cambiar_plan():
    planificacion = {"disponibilidad": {"Lunes": 2}}
    original = {"disponibilidad": {"Lunes": 2}}
    disponibilidad = {dia: 1 for dia in interfaz.DIAS_SEMANA}
    disponibilidad["Sábado"] = 25

    with pytest.raises(ValueError):
        interfaz.aplicar_disponibilidad_semanal(
            planificacion,
            disponibilidad,
            date(2026, 10, 11),
        )

    assert planificacion == original


def test_calendario_muestra_agenda_completa_hasta_fecha_objetivo():
    try:
        ventana = tk.Tk()
    except tk.TclError as error:
        pytest.skip(f"Tk no está disponible: {error}")
    fecha = date.today().replace(day=1)
    fecha_planificada = date(
        fecha.year + (fecha.month == 12),
        fecha.month % 12 + 1,
        5,
    )
    objetivo = date(
        fecha_planificada.year,
        fecha_planificada.month,
        20,
    )
    plan = {
        fecha_planificada.isoformat(): [
            {
                "categoria": "Máster",
                "modulo": "HTML",
                "horas": 1.5,
                "detalles": ["Tema 2 · clase 1/6"],
            },
        ],
    }

    try:
        calendario = CalendarioAcademico(
            ventana,
            plan=plan,
            fecha_objetivo=objetivo,
        )
        ventana.update()

        filas = calendario.agenda_tabla.get_children()
        assert len(filas) == 1
        assert calendario.agenda_tabla.item(filas[0], "values") == (
            fecha_planificada.strftime("%a %d/%m"),
            "Máster",
            "HTML",
            "Tema 2 · clase 1/6",
            "1.5 h",
        )
        assert calendario.agenda_tabla.winfo_viewable()
    finally:
        ventana.destroy()

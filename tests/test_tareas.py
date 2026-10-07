import json
from datetime import datetime
from unittest.mock import patch

from tareas import cargar_tareas, guardar_tareas
from utilidades import validar_fecha, calcular_horas_hasta_objetivo


def test_cargar_tareas_con_formato_antiguo(tmp_path):
    archivo = tmp_path / "tareas.json"

    datos = [
        "Estudiar Python",
        {
            "nombre": "Hacer ejercicios",
            "fecha_limite": "10/10/2026",
            "prioridad": "Alta",
            "categoria": "Python",
            "completada": False,
        },
    ]

    archivo.write_text(
        json.dumps(datos),
        encoding="utf-8",
    )

    tareas = cargar_tareas(archivo)

    assert len(tareas) == 2
    assert tareas[0]["nombre"] == "Estudiar Python"
    assert tareas[0]["prioridad"] == "Media"
    assert tareas[0]["categoria"] == "General"
    assert tareas[0]["completada"] is False

    assert tareas[1]["nombre"] == "Hacer ejercicios"
    assert tareas[1]["prioridad"] == "Alta"
    assert tareas[1]["categoria"] == "Python"


def test_cargar_tareas_corrige_datos_invalidos(tmp_path):
    archivo = tmp_path / "tareas.json"

    datos = [
        {
            "nombre": "Tarea válida",
            "prioridad": "Urgente",
            "categoria": "",
            "completada": "sí",
        },
        {
            "nombre": "",
            "prioridad": "Alta",
        },
        {
            "nombre": "Fecha incorrecta",
            "fecha_limite": "31/02/2026",
        },
        123,
        "",
    ]

    archivo.write_text(
        json.dumps(datos),
        encoding="utf-8",
    )

    tareas = cargar_tareas(archivo)

    assert len(tareas) == 2
    assert tareas[0]["nombre"] == "Tarea válida"
    assert tareas[0]["prioridad"] == "Media"
    assert tareas[0]["categoria"] == "General"
    assert tareas[0]["completada"] is True
    assert tareas[1]["fecha_limite"] == ""


def test_cargar_tareas_con_json_no_lista(tmp_path):
    archivo = tmp_path / "tareas.json"

    archivo.write_text(
        json.dumps({"tarea": "Estudiar"}),
        encoding="utf-8",
    )

    tareas = cargar_tareas(archivo)

    assert tareas == []

def test_cargar_tareas_si_el_archivo_no_existe(tmp_path):
    archivo = tmp_path / "tareas.json"

    tareas = cargar_tareas(archivo)

    assert tareas == []

def test_guardar_tareas_y_volver_a_cargarlas(tmp_path):
    archivo = tmp_path / "tareas.json"

    tareas_originales = [
        {
            "nombre": "Estudiar Python",
            "fecha_limite": "10/10/2026",
            "prioridad": "Alta",
            "categoria": "Python",
            "completada": False,
        }
    ]

    assert guardar_tareas(tareas_originales, archivo) is True

    tareas_cargadas = cargar_tareas(archivo)

    assert tareas_cargadas == tareas_originales

def test_guardar_tareas_muestra_error_si_no_puede_guardar(
    tmp_path,
    capsys,
):
    archivo = tmp_path / "tareas.json"

    archivo.mkdir()

    tareas = [
        {
            "nombre": "Estudiar Python",
            "fecha_limite": "",
            "prioridad": "Media",
            "categoria": "Python",
            "completada": False,
        }
    ]

    assert guardar_tareas(tareas, archivo) is False

    salida = capsys.readouterr().out

    assert "no se han podido guardar" in salida

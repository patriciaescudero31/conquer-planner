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
        123,
    ]

    archivo.write_text(
        json.dumps(datos),
        encoding="utf-8",
    )

    tareas = cargar_tareas(archivo)

    assert len(tareas) == 1
    assert tareas[0]["nombre"] == "Tarea válida"
    assert tareas[0]["prioridad"] == "Media"
    assert tareas[0]["categoria"] == "General"
    assert tareas[0]["completada"] is True


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

    guardar_tareas(tareas_originales, archivo)

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

    guardar_tareas(tareas, archivo)

    salida = capsys.readouterr().out

    assert "no se han podido guardar" in salida

def test_validar_fecha():
    assert validar_fecha("") is True
    assert validar_fecha("25/12/2026") is True
    assert validar_fecha("31/02/2026") is False
    assert validar_fecha("2026-12-25") is False
    assert validar_fecha("hola") is False

def test_calcular_horas_hasta_objetivo():
    planificacion = {
        "fecha_objetivo": "04/10/2026",
        "disponibilidad": {
            "Lunes": 2.0,
            "Martes": 2.0,
            "Miércoles": 2.0,
            "Jueves": 2.0,
            "Viernes": 2.0,
            "Sábado": 4.0,
            "Domingo": 4.0,
        },
    }

    fecha_simulada = datetime(2026, 10, 1)

    with patch("utilidades.datetime") as datetime_mock:
        datetime_mock.now.return_value = fecha_simulada
        datetime_mock.strptime.side_effect = datetime.strptime

        horas = calcular_horas_hasta_objetivo(
            planificacion,
            [
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes",
                "Sábado",
                "Domingo",
            ],
        )

    assert horas == 12.0

def test_calcular_horas_hasta_objetivo_si_ya_paso():
    planificacion = {
        "fecha_objetivo": "30/09/2026",
        "disponibilidad": {
            "Lunes": 2.0,
            "Martes": 2.0,
            "Miércoles": 2.0,
            "Jueves": 2.0,
            "Viernes": 2.0,
            "Sábado": 4.0,
            "Domingo": 4.0,
        },
    }

    fecha_simulada = datetime(2026, 10, 1)

    with patch("utilidades.datetime") as datetime_mock:
        datetime_mock.now.return_value = fecha_simulada
        datetime_mock.strptime.side_effect = datetime.strptime

        horas = calcular_horas_hasta_objetivo(
            planificacion,
            [
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes",
                "Sábado",
                "Domingo",
            ],
        )

    assert horas == 0.0
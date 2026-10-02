import json

from tareas import cargar_tareas


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
    assert tareas[0]["completada"] is False

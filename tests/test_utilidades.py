from datetime import datetime
from unittest.mock import patch

from conquer_planner.core.utilidades import (
    calcular_horas_hasta_objetivo,
    validar_fecha,
)

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

    with patch("conquer_planner.core.utilidades.datetime") as datetime_mock:
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

    with patch("conquer_planner.core.utilidades.datetime") as datetime_mock:
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
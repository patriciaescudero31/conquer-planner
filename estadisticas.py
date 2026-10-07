from collections import defaultdict
from datetime import date, timedelta
import math


def _horas(actividad):
    try:
        horas = float(actividad.get("horas", 0) or 0)
    except (TypeError, ValueError, OverflowError):
        return 0.0
    return horas if math.isfinite(horas) and horas > 0 else 0.0


def horas_totales(actividades):
    return round(
        sum(_horas(actividad) for actividad in actividades),
        2,
    )


def horas_por_modulo(actividades):
    resultado = defaultdict(float)

    for actividad in actividades:
        modulo = (
            actividad.get(
                "modulo",
                ""
            )
            or "Sin módulo"
        )

        resultado[modulo] += _horas(actividad)

    return dict(resultado)


def horas_ultima_semana(actividades):
    inicio = date.today() - timedelta(days=6)
    hoy = date.today()
    total = 0.0

    for actividad in actividades:
        try:
            fecha = date.fromisoformat(actividad.get("fecha", ""))
        except (TypeError, ValueError):
            continue
        if inicio <= fecha <= hoy:
            total += _horas(actividad)

    return round(total, 2)
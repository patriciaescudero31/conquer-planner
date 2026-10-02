from datetime import datetime, timedelta


def validar_fecha(fecha):
    if not fecha:
        return True

    try:
        datetime.strptime(
            fecha,
            "%d/%m/%Y",
        )
        return True

    except ValueError:
        return False


def calcular_horas_hasta_objetivo(
    planificacion,
    dias_semana,
):
    fecha_hoy = datetime.now().date()

    fecha_objetivo = datetime.strptime(
        planificacion["fecha_objetivo"],
        "%d/%m/%Y",
    ).date()

    if fecha_objetivo < fecha_hoy:
        return 0.0

    horas_totales = 0.0
    fecha_actual = fecha_hoy

    while fecha_actual <= fecha_objetivo:
        dia_semana = dias_semana[
            fecha_actual.weekday()
        ]

        horas_totales += planificacion[
            "disponibilidad"
        ][dia_semana]

        fecha_actual += timedelta(days=1)

    return horas_totales

from datetime import datetime
from pathlib import Path
import json
import math
import sys

from copias_seguridad import (
    ErrorCopiaSeguridad,
    crear_copia_antes_de_guardar,
)
from tareas import (
    añadir_tarea,
    cargar_tareas,
    completar_tarea,
    eliminar_tarea,
    guardar_tareas,
    mostrar_progreso,
    mostrar_tareas,
)
from utilidades import (
    calcular_horas_hasta_objetivo,
    validar_fecha,
)


BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_TAREAS = BASE_DIR / "tareas.json"
ARCHIVO_PLANIFICACION = BASE_DIR / "planificacion.json"

PRIORIDADES = {
    "1": "Alta",
    "2": "Media",
    "3": "Baja",
}

DIAS_SEMANA = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
]


def mostrar_cabecera():
    print("===================================")
    print("       CONQUER PLANNER")
    print("===================================")
    print()
    print("Mi planificador académico")
    print()


def mostrar_objetivo(planificacion):
    print()
    print("OBJETIVO")
    print("-----------------------------------")
    print(
        f"Fecha objetivo: "
        f"{planificacion['fecha_objetivo']}"
    )

    if "horas_estimadas" in planificacion:
        print(
            f"Horas estimadas: "
            f"{planificacion['horas_estimadas']:g} h"
        )

    print()


def mostrar_menu():
    print()
    print("-----------------------------------")
    print("MENÚ PRINCIPAL")
    print("-----------------------------------")
    print("1. Ver objetivo")
    print("2. Añadir tarea")
    print("3. Ver tareas")
    print("4. Completar tarea")
    print("5. Eliminar tarea")
    print("6. Ver progreso")
    print("7. Configurar planificación")
    print("8. Ver disponibilidad")
    print("9. Ver horas hasta el objetivo")
    print("10. Salir")
    print()


def crear_planificacion_por_defecto():
    return {
        "fecha_objetivo": "31/03/2027",
        "horas_estimadas": 100.0,
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


def cargar_planificacion():
    if not ARCHIVO_PLANIFICACION.exists():
        planificacion = crear_planificacion_por_defecto()
        guardar_planificacion(planificacion)
        return planificacion

    try:
        with open(
            ARCHIVO_PLANIFICACION,
            "r",
            encoding="utf-8",
        ) as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, dict):
            raise ValueError

        defecto = crear_planificacion_por_defecto()
        fecha = datos.get("fecha_objetivo")
        if not isinstance(fecha, str) or not fecha or not validar_fecha(fecha):
            datos["fecha_objetivo"] = defecto["fecha_objetivo"]
        try:
            horas_estimadas = float(datos.get("horas_estimadas", defecto["horas_estimadas"]))
            if not math.isfinite(horas_estimadas) or horas_estimadas < 0:
                raise ValueError
        except (TypeError, ValueError, OverflowError):
            horas_estimadas = defecto["horas_estimadas"]
        datos["horas_estimadas"] = horas_estimadas

        disponibilidad = datos.get("disponibilidad")
        if not isinstance(disponibilidad, dict):
            disponibilidad = {}
        datos["disponibilidad"] = {}
        for dia, horas_defecto in defecto["disponibilidad"].items():
            try:
                horas = float(disponibilidad.get(dia, horas_defecto))
                if not math.isfinite(horas) or horas < 0:
                    raise ValueError
            except (TypeError, ValueError, OverflowError):
                horas = horas_defecto
            datos["disponibilidad"][dia] = horas
        return datos

    except (json.JSONDecodeError, OSError, ValueError):
        print()
        print(
            "Aviso: no se ha podido cargar "
            "la planificación."
        )
        print()

        planificacion = crear_planificacion_por_defecto()
        guardar_planificacion(planificacion)
        return planificacion


def guardar_planificacion(planificacion):
    try:
        crear_copia_antes_de_guardar(ARCHIVO_PLANIFICACION)
        with open(
            ARCHIVO_PLANIFICACION,
            "w",
            encoding="utf-8",
        ) as archivo:
            json.dump(
                planificacion,
                archivo,
                ensure_ascii=False,
                indent=4,
            )

    except (OSError, ErrorCopiaSeguridad) as error:
        print()
        print(
            "Error: no se ha podido guardar "
            f"la planificación. {error}"
        )
        print()


def configurar_planificacion(planificacion):
    print()
    print("CONFIGURAR PLANIFICACIÓN")
    print("-----------------------------------")

    fecha = input(
        "Fecha objetivo (DD/MM/AAAA): "
    ).strip()

    if not fecha or not validar_fecha(fecha):
        print()
        print(
            "Fecha no válida. Usa DD/MM/AAAA."
        )
        return

    try:
        horas = float(
            input(
                "Horas estimadas necesarias: "
            ).strip()
        )
    except ValueError:
        print()
        print("Introduce un número válido.")
        return

    if not math.isfinite(horas) or horas < 0:
        print()
        print("Las horas no pueden ser negativas.")
        return

    print()
    print("Disponibilidad semanal:")
    print()

    disponibilidad = {}
    for dia in DIAS_SEMANA:
        try:
            horas_dia = float(
                input(
                    f"Horas disponibles el {dia}: "
                ).strip()
            )
        except ValueError:
            print()
            print("Introduce un número válido.")
            return

        if not math.isfinite(horas_dia) or horas_dia < 0:
            print()
            print("Las horas no pueden ser negativas.")
            return

        disponibilidad[dia] = horas_dia

    planificacion["fecha_objetivo"] = fecha
    planificacion["horas_estimadas"] = horas
    planificacion["disponibilidad"] = disponibilidad
    guardar_planificacion(planificacion)

    print()
    print("✓ Planificación actualizada correctamente.")
    print()


def mostrar_disponibilidad(planificacion):
    print()
    print("DISPONIBILIDAD SEMANAL")
    print("-----------------------------------")

    total = 0.0

    for dia in DIAS_SEMANA:
        horas = planificacion["disponibilidad"][dia]
        total += horas
        print(f"{dia}: {horas:g} h")

    print()
    print(f"Total disponible semanal: {total:g} h")
    print()


def mostrar_horas_hasta_objetivo(planificacion):
    print()
    print("HORAS HASTA EL OBJETIVO")
    print("-----------------------------------")

    horas_disponibles = calcular_horas_hasta_objetivo(
        planificacion,
        DIAS_SEMANA,
    )

    print(
        f"Horas disponibles hasta el objetivo: "
        f"{horas_disponibles:g} h"
    )

    if "horas_estimadas" not in planificacion:
        print()
        print(
            "Todavía no has configurado las "
            "horas estimadas necesarias."
        )
        print(
            "Puedes hacerlo desde la opción 7."
        )
        print()
        return

    horas_estimadas = planificacion["horas_estimadas"]

    print(
        f"Horas estimadas necesarias: "
        f"{horas_estimadas:g} h"
    )

    if horas_estimadas <= 0:
        print()
        print(
            "No se puede calcular la cobertura "
            "porque las horas estimadas deben ser "
            "mayores que 0."
        )
        print()
        return

    cobertura = (
        horas_disponibles / horas_estimadas
    ) * 100

    diferencia = horas_disponibles - horas_estimadas

    fecha_hoy = datetime.now().date()

    fecha_objetivo = datetime.strptime(
        planificacion["fecha_objetivo"],
        "%d/%m/%Y",
    ).date()

    dias_restantes = (
        fecha_objetivo - fecha_hoy
    ).days

    if dias_restantes < 0:
        dias_restantes = 0

    semanas_restantes = dias_restantes / 7

    print(
        f"Cobertura disponible: "
        f"{cobertura:.1f}%"
    )

    if diferencia >= 0:
        print(
            f"Margen disponible: "
            f"{diferencia:g} h"
        )
    else:
        print(
            f"Faltan: "
            f"{abs(diferencia):g} h"
        )

    if semanas_restantes > 0:
        horas_semanales_necesarias = (
            horas_estimadas
            / semanas_restantes
        )

        disponibilidad_semanal = sum(
            planificacion["disponibilidad"][dia]
            for dia in DIAS_SEMANA
        )

        print(
            f"Media necesaria por semana: "
            f"{horas_semanales_necesarias:.1f} h"
        )

        print(
            f"Disponibilidad semanal configurada: "
            f"{disponibilidad_semanal:g} h"
        )

    print()


def main():
    mostrar_cabecera()

    tareas = cargar_tareas(ARCHIVO_TAREAS)
    planificacion = cargar_planificacion()

    while True:
        mostrar_menu()

        opcion = input(
            "Selecciona una opción: "
        ).strip()

        if opcion == "1":
            mostrar_objetivo(planificacion)

        elif opcion == "2":
            añadir_tarea(
                tareas,
                PRIORIDADES,
                validar_fecha,
                lambda datos: guardar_tareas(
                    datos,
                    ARCHIVO_TAREAS,
                ),
            )

        elif opcion == "3":
            mostrar_tareas(tareas)

        elif opcion == "4":
            completar_tarea(
                tareas,
                lambda datos: guardar_tareas(
                    datos,
                    ARCHIVO_TAREAS,
                ),
            )

        elif opcion == "5":
            eliminar_tarea(
                tareas,
                lambda datos: guardar_tareas(
                    datos,
                    ARCHIVO_TAREAS,
                ),
            )

        elif opcion == "6":
            mostrar_progreso(tareas)

        elif opcion == "7":
            configurar_planificacion(planificacion)

        elif opcion == "8":
            mostrar_disponibilidad(planificacion)

        elif opcion == "9":
            mostrar_horas_hasta_objetivo(planificacion)

        elif opcion == "10":
            print()
            print("¡Hasta luego!")
            break

        else:
            print()
            print(
                "Opción no válida. "
                "Selecciona una opción del menú."
            )
            print()


if __name__ == "__main__":
    if "--cli" in sys.argv[1:]:
        main()
    else:
        from interfaz import crear_ventana

        crear_ventana()
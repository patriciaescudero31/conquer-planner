import json
from datetime import datetime, timedelta
from pathlib import Path


ARCHIVO_TAREAS = Path("tareas.json")
ARCHIVO_PLANIFICACION = Path("planificacion.json")

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
    print("Terminar el máster")
    print(f"Fecha objetivo: {planificacion['fecha_objetivo']}")
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


def cargar_tareas():
    if not ARCHIVO_TAREAS.exists():
        return []

    try:
        with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

    except (json.JSONDecodeError, OSError):
        print()
        print("Aviso: no se han podido cargar las tareas.")
        return []

    tareas = []

    for tarea in datos:
        if isinstance(tarea, str):
            tareas.append({
                "nombre": tarea,
                "fecha_limite": "",
                "prioridad": "Media",
                "categoria": "General",
                "completada": False,
            })

        elif isinstance(tarea, dict):
            tareas.append({
                "nombre": str(tarea.get("nombre", "")).strip(),
                "fecha_limite": str(
                    tarea.get("fecha_limite", "")
                ).strip(),
                "prioridad": tarea.get("prioridad", "Media"),
                "categoria": str(
                    tarea.get("categoria", "General")
                ).strip(),
                "completada": bool(
                    tarea.get("completada", False)
                ),
            })

    return tareas


def guardar_tareas(tareas):
    try:
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as archivo:
            json.dump(
                tareas,
                archivo,
                ensure_ascii=False,
                indent=4,
            )

    except OSError:
        print()
        print("Error: no se han podido guardar las tareas.")
        print()


def crear_planificacion_por_defecto():
    return {
        "fecha_objetivo": "31/03/2027",
        "disponibilidad": {
            "Lunes": 0.0,
            "Martes": 0.0,
            "Miércoles": 0.0,
            "Jueves": 0.0,
            "Viernes": 0.0,
            "Sábado": 0.0,
            "Domingo": 0.0,
        },
    }


def cargar_planificacion():
    if not ARCHIVO_PLANIFICACION.exists():
        return crear_planificacion_por_defecto()

    try:
        with open(
            ARCHIVO_PLANIFICACION,
            "r",
            encoding="utf-8",
        ) as archivo:
            datos = json.load(archivo)

    except (json.JSONDecodeError, OSError):
        print()
        print("Aviso: no se ha podido cargar la planificación.")
        print()
        return crear_planificacion_por_defecto()

    planificacion = crear_planificacion_por_defecto()

    if isinstance(datos, dict):
        fecha_objetivo = datos.get(
            "fecha_objetivo",
            "31/03/2027",
        )

        if validar_fecha(fecha_objetivo):
            planificacion["fecha_objetivo"] = fecha_objetivo

        disponibilidad = datos.get(
            "disponibilidad",
            {},
        )

        if isinstance(disponibilidad, dict):
            for dia in DIAS_SEMANA:
                valor = disponibilidad.get(dia, 0.0)

                try:
                    valor = float(valor)

                    if valor >= 0:
                        planificacion["disponibilidad"][dia] = valor

                except (TypeError, ValueError):
                    pass

    return planificacion


def guardar_planificacion(planificacion):
    try:
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

    except OSError:
        print()
        print("Error: no se ha podido guardar la planificación.")
        print()


def validar_fecha(fecha):
    if not fecha:
        return True

    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True

    except ValueError:
        return False


def pedir_numero_tarea(tareas, mensaje):
    if not tareas:
        print()
        print("No hay tareas disponibles.")
        print()
        return None

    try:
        numero = int(input(mensaje).strip())

    except ValueError:
        print()
        print("Introduce un número válido.")
        print()
        return None

    if numero < 1 or numero > len(tareas):
        print()
        print("Ese número de tarea no existe.")
        print()
        return None

    return numero - 1


def pedir_prioridad():
    print()
    print("Prioridad:")
    print("1. Alta")
    print("2. Media")
    print("3. Baja")

    opcion = input("Selecciona prioridad: ").strip()

    return PRIORIDADES.get(opcion, "Media")


def añadir_tarea(tareas):
    print()
    print("AÑADIR TAREA")
    print("-----------------------------------")

    nombre = input("Nombre de la tarea: ").strip()

    if not nombre:
        print()
        print("La tarea no puede estar vacía.")
        return

    fecha = input(
        "Fecha límite (DD/MM/AAAA, Enter para dejar vacía): "
    ).strip()

    if not validar_fecha(fecha):
        print()
        print("Fecha no válida. Usa DD/MM/AAAA.")
        return

    categoria = input(
        "Categoría (ej. TFM, asignatura, lectura): "
    ).strip()

    if not categoria:
        categoria = "General"

    prioridad = pedir_prioridad()

    tarea = {
        "nombre": nombre,
        "fecha_limite": fecha,
        "prioridad": prioridad,
        "categoria": categoria,
        "completada": False,
    }

    tareas.append(tarea)
    guardar_tareas(tareas)

    print()
    print("✓ Tarea añadida correctamente.")
    print()


def mostrar_tareas(tareas):
    print()
    print("MIS TAREAS")
    print("-----------------------------------")

    if not tareas:
        print("Todavía no hay tareas.")
        return

    for numero, tarea in enumerate(tareas, start=1):
        estado = "✓" if tarea["completada"] else " "
        fecha = tarea["fecha_limite"] or "Sin fecha"

        print(f"{numero}. [{estado}] {tarea['nombre']}")
        print(f"   Fecha: {fecha}")
        print(f"   Prioridad: {tarea['prioridad']}")
        print(f"   Categoría: {tarea['categoria']}")
        print()


def completar_tarea(tareas):
    print()
    print("COMPLETAR TAREA")
    print("-----------------------------------")

    indice = pedir_numero_tarea(
        tareas,
        "Número de tarea completada: ",
    )

    if indice is None:
        return

    if tareas[indice]["completada"]:
        print()
        print("Esta tarea ya estaba completada.")
        return

    tareas[indice]["completada"] = True
    guardar_tareas(tareas)

    print()
    print(f"✓ Completada: {tareas[indice]['nombre']}")
    print()


def eliminar_tarea(tareas):
    print()
    print("ELIMINAR TAREA")
    print("-----------------------------------")

    indice = pedir_numero_tarea(
        tareas,
        "Número de tarea a eliminar: ",
    )

    if indice is None:
        return

    tarea = tareas[indice]

    confirmacion = input(
        f'¿Eliminar "{tarea["nombre"]}"? (s/n): '
    ).strip().lower()

    if confirmacion != "s":
        print()
        print("Eliminación cancelada.")
        return

    tareas.pop(indice)
    guardar_tareas(tareas)

    print()
    print("✓ Tarea eliminada.")
    print()


def mostrar_progreso(tareas):
    print()
    print("PROGRESO")
    print("-----------------------------------")

    if not tareas:
        print("Todavía no hay tareas.")
        return

    total = len(tareas)

    completadas = sum(
        tarea["completada"]
        for tarea in tareas
    )

    pendientes = total - completadas
    porcentaje = (completadas / total) * 100

    print(f"Total de tareas: {total}")
    print(f"Completadas: {completadas}")
    print(f"Pendientes: {pendientes}")
    print(f"Progreso: {porcentaje:.0f}%")
    print()

    print("Por categoría:")

    categorias = {}

    for tarea in tareas:
        categoria = tarea["categoria"]

        if categoria not in categorias:
            categorias[categoria] = {
                "total": 0,
                "completadas": 0,
            }

        categorias[categoria]["total"] += 1

        if tarea["completada"]:
            categorias[categoria]["completadas"] += 1

    for categoria, datos in categorias.items():
        total_categoria = datos["total"]
        completadas_categoria = datos["completadas"]

        porcentaje_categoria = (
            completadas_categoria / total_categoria
        ) * 100

        print(
            f"- {categoria}: "
            f"{completadas_categoria}/"
            f"{total_categoria} "
            f"({porcentaje_categoria:.0f}%)"
        )

    print()


def configurar_planificacion(planificacion):
    print()
    print("CONFIGURAR PLANIFICACIÓN")
    print("-----------------------------------")

    print(
        "Aquí indicaremos cuánto tiempo real "
        "tienes disponible cada día."
    )
    print()

    fecha_actual = planificacion["fecha_objetivo"]

    nueva_fecha = input(
        f"Fecha objetivo (actual: {fecha_actual}): "
    ).strip()

    if nueva_fecha:
        if not validar_fecha(nueva_fecha):
            print()
            print("Fecha no válida. Usa DD/MM/AAAA.")
            return

        planificacion["fecha_objetivo"] = nueva_fecha

    print()
    print(
        "Ahora introduce las horas que "
        "puedes dedicar al estudio cada día."
    )
    print(
        "Puedes usar decimales. "
        "Ejemplo: 1.5 = 1 hora y 30 minutos."
    )
    print()

    for dia in DIAS_SEMANA:
        actual = planificacion["disponibilidad"][dia]

        while True:
            respuesta = input(
                f"{dia} (actual: {actual} h): "
            ).strip()

            if not respuesta:
                break

            try:
                horas = float(respuesta)

                if horas < 0:
                    raise ValueError

                planificacion["disponibilidad"][dia] = horas
                break

            except ValueError:
                print(
                    "Introduce un número mayor o igual que 0."
                )

    guardar_planificacion(planificacion)

    print()
    print("✓ Planificación guardada correctamente.")
    print()


def mostrar_disponibilidad(planificacion):
    print()
    print("MI DISPONIBILIDAD")
    print("-----------------------------------")

    print(
        f"Fecha objetivo: "
        f"{planificacion['fecha_objetivo']}"
    )
    print()

    total = 0.0

    for dia in DIAS_SEMANA:
        horas = planificacion["disponibilidad"][dia]
        total += horas

        print(f"{dia}: {horas:g} h")

    print()
    print(f"Total disponible semanal: {total:g} h")
    print()

def calcular_horas_hasta_objetivo(planificacion):
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
        dia_semana = DIAS_SEMANA[
            fecha_actual.weekday()
        ]

        horas_totales += planificacion[
            "disponibilidad"
        ][dia_semana]

        fecha_actual += timedelta(days=1)

    return horas_totales


def mostrar_horas_hasta_objetivo(planificacion):
    print()
    print("HORAS DISPONIBLES HASTA EL OBJETIVO")
    print("-----------------------------------")

    horas = calcular_horas_hasta_objetivo(planificacion)

    print(
        f"Fecha objetivo: "
        f"{planificacion['fecha_objetivo']}"
    )

    print(f"Horas disponibles: {horas:g} h")
    print()


def main():
    mostrar_cabecera()

    tareas = cargar_tareas()
    planificacion = cargar_planificacion()

    while True:
        mostrar_menu()

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            mostrar_objetivo(planificacion)

        elif opcion == "2":
            añadir_tarea(tareas)

        elif opcion == "3":
            mostrar_tareas(tareas)

        elif opcion == "4":
            completar_tarea(tareas)

        elif opcion == "5":
            eliminar_tarea(tareas)

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
            print("Opción no válida.")
            print()


if __name__ == "__main__":
    main()
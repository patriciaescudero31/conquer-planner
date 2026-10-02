import json


def cargar_tareas(archivo_tareas):
    if not archivo_tareas.exists():
        return []

    try:
        with open(
            archivo_tareas,
            "r",
            encoding="utf-8",
        ) as archivo:
            datos = json.load(archivo)

        if isinstance(datos, list):
            return datos

        return []

    except (json.JSONDecodeError, OSError):
        print()
        print(
            "Aviso: no se han podido cargar "
            "las tareas."
        )
        print()
        return []


def guardar_tareas(tareas, archivo_tareas):
    try:
        with open(
            archivo_tareas,
            "w",
            encoding="utf-8",
        ) as archivo:
            json.dump(
                tareas,
                archivo,
                ensure_ascii=False,
                indent=4,
            )

    except OSError:
        print()
        print(
            "Error: no se han podido guardar "
            "las tareas."
        )
        print()


def pedir_numero_tarea(tareas, mensaje):
    if not tareas:
        print()
        print("No hay tareas.")
        print()
        return None

    try:
        numero = int(
            input(mensaje).strip()
        )

    except ValueError:
        print()
        print("Introduce un número válido.")
        print()
        return None

    if numero < 1 or numero > len(tareas):
        print()
        print(
            "Ese número de tarea no existe."
        )
        print()
        return None

    return numero - 1


def pedir_prioridad(prioridades):
    print()
    print("1. Alta")
    print("2. Media")
    print("3. Baja")

    opcion = input(
        "Selecciona prioridad: "
    ).strip()

    return prioridades.get(
        opcion,
        "Media",
    )


def añadir_tarea(
    tareas,
    prioridades,
    validar_fecha,
    guardar,
):
    print()
    print("AÑADIR TAREA")
    print("-----------------------------------")

    nombre = input(
        "Nombre de la tarea: "
    ).strip()

    if not nombre:
        print()
        print(
            "La tarea no puede estar vacía."
        )
        return

    fecha = input(
        "Fecha límite "
        "(DD/MM/AAAA, Enter para dejar vacía): "
    ).strip()

    if not validar_fecha(fecha):
        print()
        print(
            "Fecha no válida. Usa DD/MM/AAAA."
        )
        return

    categoria = input(
        "Categoría "
        "(ej. TFM, asignatura, lectura): "
    ).strip()

    if not categoria:
        categoria = "General"

    prioridad = pedir_prioridad(
        prioridades
    )

    tarea = {
        "nombre": nombre,
        "fecha_limite": fecha,
        "categoria": categoria,
        "prioridad": prioridad,
        "completada": False,
    }

    tareas.append(tarea)
    guardar(tareas)

    print()
    print("✓ Tarea añadida correctamente.")
    print()


def mostrar_tareas(tareas):
    print()
    print("TAREAS")
    print("-----------------------------------")

    if not tareas:
        print("Todavía no hay tareas.")
        return

    for numero, tarea in enumerate(
        tareas,
        start=1,
    ):
        estado = (
            "✓"
            if tarea["completada"]
            else " "
        )

        fecha = (
            tarea["fecha_limite"]
            or "Sin fecha"
        )

        print(
            f"{numero}. [{estado}] "
            f"{tarea['nombre']}"
        )
        print(f"   Fecha: {fecha}")
        print(
            f"   Prioridad: "
            f"{tarea['prioridad']}"
        )
        print(
            f"   Categoría: "
            f"{tarea['categoria']}"
        )
        print()


def completar_tarea(tareas, guardar):
    indice = pedir_numero_tarea(
        tareas,
        "Número de tarea a completar: ",
    )

    if indice is None:
        return

    if tareas[indice]["completada"]:
        print()
        print(
            "Esta tarea ya estaba completada."
        )
        return

    tareas[indice]["completada"] = True
    guardar(tareas)

    print()
    print(
        f"✓ Completada: "
        f"{tareas[indice]['nombre']}"
    )
    print()


def eliminar_tarea(tareas, guardar):
    indice = pedir_numero_tarea(
        tareas,
        "Número de tarea a eliminar: ",
    )

    if indice is None:
        return

    tarea = tareas[indice]

    confirmacion = input(
        f'¿Eliminar "{tarea["nombre"]}"? '
        "(s/n): "
    ).strip().lower()

    if confirmacion != "s":
        print()
        print("Operación cancelada.")
        print()
        return

    tareas.pop(indice)
    guardar(tareas)

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

    porcentaje = (
        completadas / total
    ) * 100

    print(f"Total de tareas: {total}")
    print(
        f"Completadas: {completadas}"
    )
    print(f"Pendientes: {pendientes}")
    print(
        f"Progreso: {porcentaje:.0f}%"
    )
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
            categorias[categoria][
                "completadas"
            ] += 1

    for categoria, datos in (
        categorias.items()
    ):
        total_categoria = datos["total"]

        completadas_categoria = (
            datos["completadas"]
        )

        porcentaje_categoria = (
            completadas_categoria
            / total_categoria
        ) * 100

        print(
            f"- {categoria}: "
            f"{completadas_categoria}/"
            f"{total_categoria} "
            f"({porcentaje_categoria:.0f}%)"
        )

    print()

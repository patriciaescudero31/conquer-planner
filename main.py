import json
from datetime import datetime
from pathlib import Path


ARCHIVO_TAREAS = Path("tareas.json")


def mostrar_cabecera():
    print("===================================")
    print("       CONQUER PLANNER")
    print("===================================")
    print()
    print("Mi planificador académico")
    print()


def mostrar_objetivo():
    print()
    print("OBJETIVO")
    print("-----------------------------------")
    print("Terminar el máster")
    print("Fecha objetivo: 31/03/2027")
    print()


def mostrar_menu():
    print()
    print("-----------------------------------")
    print("MENÚ PRINCIPAL")
    print("-----------------------------------")
    print("1. Ver objetivo")
    print("2. Añadir tarea")
    print("3. Ver tareas")
    print("4. Salir")
    print()


def cargar_tareas():
    if not ARCHIVO_TAREAS.exists():
        return []

    try:
        with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as archivo:
            tareas = json.load(archivo)
    except (json.JSONDecodeError, OSError):
        print()
        print("Aviso: no se han podido cargar las tareas.")
        print("Se empezará con una lista vacía.")
        print()
        return []

    tareas_convertidas = []

    for tarea in tareas:
        if isinstance(tarea, str):
            tareas_convertidas.append({
                "nombre": tarea,
                "fecha_limite": ""
            })

        elif isinstance(tarea, dict):
            tareas_convertidas.append({
                "nombre": tarea.get("nombre", "").strip(),
                "fecha_limite": tarea.get("fecha_limite", "").strip()
            })

    return tareas_convertidas


def guardar_tareas(tareas):
    try:
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as archivo:
            json.dump(tareas, archivo, ensure_ascii=False, indent=4)
    except OSError:
        print()
        print("Error: no se han podido guardar las tareas.")
        print()


def validar_fecha(fecha):
    if fecha == "":
        return True

    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def añadir_tarea(tareas):
    print()
    print("AÑADIR TAREA")
    print("-----------------------------------")

    nombre = input("Nombre de la tarea: ").strip()

    if nombre == "":
        print()
        print("La tarea no puede estar vacía.")
        print()
        return

    fecha_limite = input(
        "Fecha límite (DD/MM/AAAA, Enter para dejar vacía): "
    ).strip()

    if not validar_fecha(fecha_limite):
        print()
        print("Fecha no válida.")
        print("Utiliza el formato DD/MM/AAAA.")
        print()
        return

    tarea = {
        "nombre": nombre,
        "fecha_limite": fecha_limite
    }

    tareas.append(tarea)
    guardar_tareas(tareas)

    print()
    print("Tarea añadida correctamente.")
    print()


def mostrar_tareas(tareas):
    print()
    print("MIS TAREAS")
    print("-----------------------------------")

    if not tareas:
        print("Todavía no hay tareas guardadas.")
        print()
        return

    for numero, tarea in enumerate(tareas, start=1):
        nombre = tarea.get("nombre", "Sin nombre")
        fecha = tarea.get("fecha_limite", "")

        print(f"{numero}. {nombre}")

        if fecha:
            print(f"   Fecha límite: {fecha}")
        else:
            print("   Fecha límite: Sin fecha")

    print()


def main():
    mostrar_cabecera()

    tareas = cargar_tareas()

    while True:
        mostrar_menu()

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            mostrar_objetivo()

        elif opcion == "2":
            añadir_tarea(tareas)

        elif opcion == "3":
            mostrar_tareas(tareas)

        elif opcion == "4":
            print()
            print("¡Hasta luego!")
            break

        else:
            print()
            print("Opción no válida. Elige un número del 1 al 4.")
            print()


if __name__ == "__main__":
    main()
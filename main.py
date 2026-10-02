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
    print("4. Completar tarea")
    print("5. Eliminar tarea")
    print("6. Salir")
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
        print("Se empezará con una lista vacía.")
        print()
        return []

    tareas = []

    for tarea in datos:
        # Compatibilidad con las tareas antiguas que eran solo texto
        if isinstance(tarea, str):
            tareas.append({
                "nombre": tarea,
                "fecha_limite": "",
                "completada": False
            })

        elif isinstance(tarea, dict):
            tareas.append({
                "nombre": str(tarea.get("nombre", "")).strip(),
                "fecha_limite": str(tarea.get("fecha_limite", "")).strip(),
                "completada": bool(tarea.get("completada", False))
            })

    return tareas


def guardar_tareas(tareas):
    try:
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as archivo:
            json.dump(
                tareas,
                archivo,
                ensure_ascii=False,
                indent=4
            )
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


def añadir_tarea(tareas):
    print()
    print("AÑADIR TAREA")
    print("-----------------------------------")

    nombre = input("Nombre de la tarea: ").strip()

    if not nombre:
        print()
        print("La tarea no puede estar vacía.")
        print()
        return

    fecha = input(
        "Fecha límite (DD/MM/AAAA, Enter para dejar vacía): "
    ).strip()

    if not validar_fecha(fecha):
        print()
        print("Fecha no válida. Usa DD/MM/AAAA.")
        print()
        return

    tarea = {
        "nombre": nombre,
        "fecha_limite": fecha,
        "completada": False
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
        print()
        return

    for numero, tarea in enumerate(tareas, start=1):
        estado = "✓" if tarea["completada"] else " "
        nombre = tarea["nombre"]
        fecha = tarea["fecha_limite"] or "Sin fecha"

        print(f"{numero}. [{estado}] {nombre}")
        print(f"   Fecha límite: {fecha}")

    print()


def completar_tarea(tareas):
    print()
    print("COMPLETAR TAREA")
    print("-----------------------------------")

    indice = pedir_numero_tarea(
        tareas,
        "Número de tarea completada: "
    )

    if indice is None:
        return

    tarea = tareas[indice]

    if tarea["completada"]:
        print()
        print("Esta tarea ya estaba completada.")
        print()
        return

    tarea["completada"] = True
    guardar_tareas(tareas)

    print()
    print(f"✓ Tarea completada: {tarea['nombre']}")
    print()


def eliminar_tarea(tareas):
    print()
    print("ELIMINAR TAREA")
    print("-----------------------------------")

    indice = pedir_numero_tarea(
        tareas,
        "Número de tarea a eliminar: "
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
        print()
        return

    tareas.pop(indice)
    guardar_tareas(tareas)

    print()
    print("✓ Tarea eliminada.")
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
            completar_tarea(tareas)

        elif opcion == "5":
            eliminar_tarea(tareas)

        elif opcion == "6":
            print()
            print("¡Hasta luego!")
            break

        else:
            print()
            print("Opción no válida.")
            print()


if __name__ == "__main__":
    main()
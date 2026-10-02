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


def añadir_tarea(tareas):
    print()
    print("AÑADIR TAREA")
    print("-----------------------------------")

    nombre = input("Nombre de la tarea: ").strip()

    if nombre == "":
        print()
        print("La tarea no puede estar vacía.")
        return

    tareas.append(nombre)

    print()
    print("Tarea añadida correctamente.")
    print()


def mostrar_tareas(tareas):
    print()
    print("MIS TAREAS")
    print("-----------------------------------")

    if not tareas:
        print("Todavía no hay tareas guardadas.")
    else:
        for numero, tarea in enumerate(tareas, start=1):
            print(f"{numero}. {tarea}")

    print()


def main():
    mostrar_cabecera()

    tareas = []

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

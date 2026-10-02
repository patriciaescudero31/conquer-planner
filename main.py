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


def main():
    mostrar_cabecera()

    while True:
        mostrar_menu()

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mostrar_objetivo()

        elif opcion == "2":
            print()
            print("Añadir tarea")
            print("Esta función la construiremos en el siguiente paso.")
            print()

        elif opcion == "3":
            print()
            print("Mis tareas")
            print("Todavía no hay tareas guardadas.")
            print()

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

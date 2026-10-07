import sys

from conquer_planner.cli import *


if __name__ == "__main__":
    if "--cli" in sys.argv[1:]:
        main()
    else:
        from conquer_planner.ui.app import crear_ventana

        crear_ventana()

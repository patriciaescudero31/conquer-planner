from unittest.mock import patch

import main


def test_configuracion_rechaza_fecha_objetivo_vacia_sin_modificar_datos(capsys):
    planificacion = main.crear_planificacion_por_defecto()
    original = {
        clave: valor.copy() if isinstance(valor, dict) else valor
        for clave, valor in planificacion.items()
    }

    with patch("builtins.input", return_value=""):
        main.configurar_planificacion(planificacion)

    assert planificacion == original
    assert "Fecha no válida" in capsys.readouterr().out


def test_configuracion_invalida_no_guarda_cambios_parciales(capsys):
    planificacion = main.crear_planificacion_por_defecto()
    original = {
        clave: valor.copy() if isinstance(valor, dict) else valor
        for clave, valor in planificacion.items()
    }
    respuestas = iter(("01/04/2027", "200", "3", "incorrecto"))

    with patch("builtins.input", side_effect=lambda _prompt: next(respuestas)):
        main.configurar_planificacion(planificacion)

    assert planificacion == original
    assert "Introduce un número válido" in capsys.readouterr().out

import json

import copias_seguridad


def _configurar_archivos(tmp_path, monkeypatch):
    datos = tmp_path / "datos"
    datos.mkdir()
    archivos = {
        "planificacion.json": datos / "planificacion.json",
        "tareas.json": datos / "tareas.json",
        "temario.json": datos / "temario.json",
    }
    monkeypatch.setattr(copias_seguridad, "ARCHIVOS_DATOS", archivos)
    monkeypatch.setattr(
        copias_seguridad,
        "DIRECTORIO_COPIAS",
        tmp_path / "copias",
    )
    return archivos


def test_crea_copia_de_los_datos_existentes_antes_de_guardar(
    tmp_path,
    monkeypatch,
):
    archivos = _configurar_archivos(tmp_path, monkeypatch)
    archivos["planificacion.json"].write_text(
        json.dumps({"progreso": 10}),
        encoding="utf-8",
    )
    archivos["temario.json"].write_text(
        json.dumps({"catalogo": {}}),
        encoding="utf-8",
    )

    copia = copias_seguridad.crear_copia_antes_de_guardar(
        archivos["planificacion.json"]
    )

    assert copia is not None
    assert json.loads(
        (copia / "planificacion.json").read_text(encoding="utf-8")
    ) == {"progreso": 10}
    assert not (copia / "tareas.json").exists()
    manifiesto = json.loads(
        (copia / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifiesto["archivos"] == [
        "planificacion.json",
        "temario.json",
    ]


def test_restaurar_copia_recupera_datos_y_guarda_estado_actual(
    tmp_path,
    monkeypatch,
):
    archivos = _configurar_archivos(tmp_path, monkeypatch)
    archivos["planificacion.json"].write_text(
        json.dumps({"progreso": 10}),
        encoding="utf-8",
    )
    archivos["tareas.json"].write_text(
        json.dumps([{"nombre": "anterior"}]),
        encoding="utf-8",
    )
    copia = copias_seguridad.crear_copia_seguridad()
    archivos["planificacion.json"].write_text(
        json.dumps({"progreso": 90}),
        encoding="utf-8",
    )
    archivos["tareas.json"].unlink()

    copias_seguridad.restaurar_copia(copia.name)

    assert json.loads(
        archivos["planificacion.json"].read_text(encoding="utf-8")
    ) == {"progreso": 10}
    assert json.loads(
        archivos["tareas.json"].read_text(encoding="utf-8")
    ) == [{"nombre": "anterior"}]
    assert len(copias_seguridad.listar_copias()) == 2
    copia_estado_actual = copias_seguridad.listar_copias()[0]["ruta"]
    assert json.loads(
        (copia_estado_actual / "planificacion.json").read_text(
            encoding="utf-8"
        )
    ) == {"progreso": 90}
    assert not (copia_estado_actual / "tareas.json").exists()


def test_limita_el_numero_de_copias_conservadas(tmp_path, monkeypatch):
    archivos = _configurar_archivos(tmp_path, monkeypatch)
    archivos["planificacion.json"].write_text(
        json.dumps({"progreso": 0}),
        encoding="utf-8",
    )

    for progreso in range(4):
        archivos["planificacion.json"].write_text(
            json.dumps({"progreso": progreso}),
            encoding="utf-8",
        )
        copias_seguridad.crear_copia_seguridad(max_copias=2)

    copias = copias_seguridad.listar_copias()
    assert len(copias) == 2
    assert json.loads(
        (copias[-1]["ruta"] / "planificacion.json").read_text(
            encoding="utf-8"
        )
    ) == {"progreso": 2}

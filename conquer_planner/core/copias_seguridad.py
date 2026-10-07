import json
import os
from datetime import datetime
from pathlib import Path
import shutil
import tempfile


BASE_DIR = Path(__file__).resolve().parents[2]
ARCHIVOS_DATOS = {
    "planificacion.json": BASE_DIR / "planificacion.json",
    "tareas.json": BASE_DIR / "tareas.json",
    "temario.json": BASE_DIR / "temario.json",
}
DIRECTORIO_COPIAS = BASE_DIR / ".copias_seguridad"
MAX_COPIAS = 30


class ErrorCopiaSeguridad(Exception):
    pass


def crear_copia_seguridad(directorio=None, max_copias=MAX_COPIAS):
    """Guarda una instantánea íntegra de los datos locales existentes."""
    destino = Path(directorio) if directorio else DIRECTORIO_COPIAS
    archivos_existentes = {
        nombre: ruta
        for nombre, ruta in ARCHIVOS_DATOS.items()
        if ruta.is_file()
    }
    if not archivos_existentes:
        return None

    temporal = None
    try:
        destino.mkdir(parents=True, exist_ok=True)
        temporal = Path(
            tempfile.mkdtemp(prefix=".copia-temporal-", dir=str(destino))
        )
        fecha = datetime.now().astimezone().isoformat(timespec="seconds")
        for nombre, ruta in archivos_existentes.items():
            shutil.copy2(ruta, temporal / nombre)
        (temporal / "manifest.json").write_text(
            json.dumps(
                {
                    "fecha": fecha,
                    "archivos": sorted(archivos_existentes),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        marca = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        copia = destino / f"copia-{marca}"
        os.replace(temporal, copia)
        temporal = None
        _limitar_copias(destino, max_copias)
        return copia
    except OSError as error:
        raise ErrorCopiaSeguridad(
            f"No se pudo crear la copia en «{destino}»: {error}"
        ) from error
    finally:
        if temporal is not None:
            shutil.rmtree(temporal, ignore_errors=True)


def crear_copia_antes_de_guardar(archivo):
    """Crea una copia antes de modificar uno de los archivos personales."""
    ruta = Path(archivo).resolve()
    if ruta not in {dato.resolve() for dato in ARCHIVOS_DATOS.values()}:
        return None
    return crear_copia_seguridad()


def listar_copias(directorio=None):
    destino = Path(directorio) if directorio else DIRECTORIO_COPIAS
    if not destino.is_dir():
        return []
    copias = []
    for ruta in destino.iterdir():
        if not ruta.is_dir() or not ruta.name.startswith("copia-"):
            continue
        try:
            manifiesto = json.loads(
                (ruta / "manifest.json").read_text(encoding="utf-8")
            )
            archivos = manifiesto.get("archivos")
            if (
                not isinstance(archivos, list)
                or not archivos
                or any(
                    nombre not in ARCHIVOS_DATOS
                    or not (ruta / nombre).is_file()
                    for nombre in archivos
                )
            ):
                continue
            copias.append(
                {
                    "id": ruta.name,
                    "fecha": str(manifiesto.get("fecha", ruta.name)),
                    "ruta": ruta,
                }
            )
        except (OSError, json.JSONDecodeError, AttributeError):
            continue
    return sorted(copias, key=lambda copia: copia["id"], reverse=True)


def restaurar_copia(identificador, directorio=None):
    destino = Path(directorio) if directorio else DIRECTORIO_COPIAS
    if (
        not isinstance(identificador, str)
        or Path(identificador).name != identificador
        or not identificador.startswith("copia-")
    ):
        raise ErrorCopiaSeguridad("La copia seleccionada no es válida.")
    copia = destino / identificador
    candidatas = {item["id"]: item["ruta"] for item in listar_copias(destino)}
    if identificador not in candidatas or candidatas[identificador] != copia:
        raise ErrorCopiaSeguridad("La copia seleccionada no existe o está dañada.")

    manifiesto = json.loads(
        (copia / "manifest.json").read_text(encoding="utf-8")
    )
    archivos = manifiesto["archivos"]
    datos_temporales = {}
    try:
        for nombre in archivos:
            with open(copia / nombre, "r", encoding="utf-8") as archivo:
                valor = json.load(archivo)
            tipo_esperado = list if nombre == "tareas.json" else dict
            if not isinstance(valor, tipo_esperado):
                raise ErrorCopiaSeguridad(
                    f"El archivo «{nombre}» de la copia tiene un formato inválido."
                )
            datos_temporales[nombre] = valor
    except (OSError, json.JSONDecodeError) as error:
        raise ErrorCopiaSeguridad(
            f"No se pudo leer la copia seleccionada: {error}"
        ) from error

    crear_copia_seguridad(destino)
    temporales = []
    try:
        for nombre, valor in datos_temporales.items():
            ruta = ARCHIVOS_DATOS[nombre]
            ruta.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporal = tempfile.mkstemp(
                prefix=f".{nombre}-",
                dir=str(ruta.parent),
            )
            temporales.append((Path(temporal), ruta))
            with os.fdopen(descriptor, "w", encoding="utf-8") as archivo:
                json.dump(valor, archivo, ensure_ascii=False, indent=4)
        for temporal, ruta in temporales:
            os.replace(temporal, ruta)
        for nombre, ruta in ARCHIVOS_DATOS.items():
            if nombre not in datos_temporales and ruta.exists():
                ruta.unlink()
    except OSError as error:
        raise ErrorCopiaSeguridad(
            f"No se pudo completar la restauración: {error}"
        ) from error
    finally:
        for temporal, _ in temporales:
            if temporal.exists():
                temporal.unlink()


def _limitar_copias(directorio, max_copias):
    copias = listar_copias(directorio)
    for antigua in copias[max(0, max_copias):]:
        shutil.rmtree(antigua["ruta"])

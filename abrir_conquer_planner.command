#!/bin/sh

set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON="$PROJECT_DIR/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
    printf '%s\n' "No encuentro .venv/bin/python en:"
    printf '%s\n' "$PROJECT_DIR"
    printf '%s\n' "Consulta README.md para configurar el entorno del proyecto."
    exit 1
fi

cd "$PROJECT_DIR"
exec "$PYTHON" "$PROJECT_DIR/main.py"

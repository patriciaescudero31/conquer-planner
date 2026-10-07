# Conquer Planner

**Planificador académico inteligente local** para organizar máster, inglés, disponibilidad y progreso hasta una fecha objetivo.

## Qué hace ahora

- **Plan de hoy automático** con tareas manuales ordenadas por prioridad antes del temario.
- Sesión semanal de **Google Antigravity los miércoles** cuando queda disponibilidad tras las tareas.
- Seguimiento y edición del progreso por módulo.
- Edición de las clases, tareas y evaluaciones totales de cada sección del temario; el prework vacío se puede marcar como completado o configurar con sus cantidades reales.
- Seguimiento de HTML, inglés y resto del catálogo.
- Agenda diaria y semanal generada desde el temario, el progreso, la disponibilidad y la fecha objetivo.
- Calendario mensual con planificación prevista y sesiones reales.
- Registro de clases, apuntes, tareas, evaluaciones, tutorías, directos y práctica.
- Estimación independiente de clases, apuntes, sesiones combinadas, tareas, evaluaciones, tutorías, clases en directo, práctica y TFM.
- Las sesiones pueden actualizar el progreso académico y recalculan la planificación.
- Estimaciones editables por clase, apuntes, tarea y evaluación.
- Las últimas cinco sesiones reales por módulo y tipo ajustan las estimaciones automáticamente.
- Cálculo automático de capacidad hasta el objetivo, horas pendientes y ritmo semanal.
- Cálculo de horas de máster restantes y margen.
- Gestión manual de tareas: las pendientes se integran en la agenda diaria por prioridad Alta → Media → Baja, usando la estimación por tarea configurada.
- Configuración editable sin abrir VS Code.
- Interfaz visual de fondo claro con navegación oscura y acentos turquesa.

## Qué ofrece cada sección

- **Inicio:** viabilidad hacia la fecha objetivo, ritmo semanal, carga pendiente y siguiente acción recomendada.
- **Plan de hoy:** agenda de tareas pendientes por prioridad, seguida del temario que cabe en las horas disponibles.
- **Tareas:** creación y seguimiento de tareas personales; al completar o cambiar prioridad, la planificación se actualiza sin duplicar actividades del temario.
- **Temario:** totales y progreso editables por módulo; los cambios se guardan localmente y se reflejan en Plan de hoy, Planificación y Calendario.
- **Planificación:** disponibilidad por día, registro y corrección de sesiones, estimaciones, proyección semanal y carga que podría quedar fuera del objetivo.
- **Planificación semanal:** cada domingo, al abrir la aplicación, puedes revisar las horas disponibles de cada día para la semana siguiente; al guardar se recalcula el calendario.
- **Progreso:** porcentajes globales, hitos actuales y capacidad frente a horas de máster pendientes.
- **Calendario:** plan previsto hasta la fecha objetivo en una agenda desplazable, además de sesiones reales seleccionables por día y mes.
- **Estadísticas:** horas registradas, actividad reciente y distribución del esfuerzo por módulo.
- **Configuración:** fecha objetivo, horas/progreso globales, inglés y estimaciones específicas por tipo de actividad.

Flujo recomendado: revisa **Plan de hoy**, estudia, registra el tiempo y el tipo de actividad en **Planificación** y deja que el progreso guardado recalcule la siguiente agenda. También puedes corregir el avance manualmente desde **Temario**.

## Requisitos

- Python 3
- Tkinter (incluido normalmente en Python de escritorio; en macOS debe estar disponible en la instalación de Python).
- Entorno virtual recomendado.

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecutar la aplicación

```bash
python main.py
```

También puedes abrir directamente la interfaz con `python interfaz.py`. Para
usar la versión de terminal, ejecuta `python main.py --cli`.

En macOS, activa el entorno virtual antes de iniciar:

```bash
source .venv/bin/activate
python main.py
```

Si el entorno virtual ya está creado, también puedes iniciar directamente con:

```bash
.venv/bin/python main.py
```

### Abrir desde el Escritorio en macOS

El acceso **Conquer Planner.command** del Escritorio abre automáticamente
Terminal y desde allí inicia la interfaz gráfica, sin que tengas que abrir
VS Code. Utiliza `.venv/bin/python` junto a la carpeta del proyecto. Mantén el
proyecto y su entorno `.venv` en su ubicación actual para que el acceso siga
funcionando.

La revisión de disponibilidad aparece los domingos a las 09:00 mientras la app
está abierta, o al iniciar la app ese mismo domingo.

## Ejecutar tests

```bash
python -m pytest -q
```

## Datos personales

`planificacion.json`, `tareas.json`, `temario.json` y las guías locales están excluidos de Git. El código de la aplicación sí se versiona.

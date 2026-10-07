import tkinter as tk
from tkinter import messagebox, ttk

from interfaz_componentes import *
from interfaz_datos import *
from interfaz_datos import _entero_no_negativo, _numero_no_negativo
from interfaz_inicio import InicioMixin
from interfaz_otros import OtrasVistasMixin
from interfaz_planificacion import PlanificacionMixin
from interfaz_shell import ShellMixin
from interfaz_tareas import TareasMixin
from interfaz_temario import TemarioMixin
from calendario import CalendarioAcademico
from copias_seguridad import ErrorCopiaSeguridad, listar_copias, restaurar_copia
from estadisticas import horas_por_modulo, horas_totales, horas_ultima_semana
from planificador import (
    calcular_carga_pendiente,
    generar_planificacion,
    horas_registradas_por_fecha,
)
from tareas import cargar_tareas, guardar_tareas
from utilidades import calcular_horas_hasta_objetivo


class ConquerPlanner(
    ShellMixin,
    InicioMixin,
    TareasMixin,
    TemarioMixin,
    PlanificacionMixin,
    OtrasVistasMixin,
):
    pass


def crear_ventana():
    ConquerPlanner().ejecutar()


if __name__ == "__main__":
    crear_ventana()

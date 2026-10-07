import tkinter as tk


class Pomodoro:
    def __init__(self, master=None):
        self.ventana = tk.Toplevel(master)
        self.ventana.title("Pomodoro")
        self.ventana.resizable(False, False)
        self.segundos_iniciales = 25 * 60
        self.segundos = self.segundos_iniciales
        self.corriendo = False
        self.after_id = None

        self.label = tk.Label(
            self.ventana,
            text="25:00",
            font=("Helvetica", 40, "bold"),
        )
        self.label.pack(padx=30, pady=(30, 18))

        controles = tk.Frame(self.ventana)
        controles.pack(pady=(0, 24))
        self.boton_inicio = tk.Button(
            controles,
            text="Iniciar",
            command=self.iniciar_pausar,
        )
        self.boton_inicio.pack(side="left", padx=5)
        tk.Button(
            controles,
            text="Reiniciar",
            command=self.reiniciar,
        ).pack(side="left", padx=5)
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)

    def iniciar_pausar(self):
        if self.corriendo:
            self.corriendo = False
            if self.after_id is not None:
                self.ventana.after_cancel(self.after_id)
                self.after_id = None
            self.boton_inicio.config(text="Continuar")
            return

        if self.segundos == 0:
            self.reiniciar()
        self.corriendo = True
        self.boton_inicio.config(text="Pausar")
        self.after_id = self.ventana.after(1000, self.contar)

    def contar(self):
        self.after_id = None
        if not self.corriendo:
            return

        self.segundos -= 1
        minutos, segundos = divmod(self.segundos, 60)
        self.label.config(text=f"{minutos:02}:{segundos:02}")
        if self.segundos == 0:
            self.corriendo = False
            self.label.config(text="¡Tiempo!")
            self.boton_inicio.config(text="Iniciar")
            return

        self.after_id = self.ventana.after(1000, self.contar)

    def reiniciar(self):
        if self.after_id is not None:
            self.ventana.after_cancel(self.after_id)
            self.after_id = None
        self.corriendo = False
        self.segundos = self.segundos_iniciales
        self.label.config(text="25:00")
        self.boton_inicio.config(text="Iniciar")

    def cerrar(self):
        if self.after_id is not None:
            self.ventana.after_cancel(self.after_id)
        self.ventana.destroy()

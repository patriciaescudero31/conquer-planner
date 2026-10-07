import sys
import tkinter as tk
from tkinter import ttk

BG = "#f3f6f6"
CARD = "#ffffff"
SIDEBAR = "#11191d"
TEXT = "#182126"
MUTED = "#68777d"
BORDER = "#e1e8e9"
ACCENT = "#087b7b"
ACCENT_DARK = "#066565"
SUCCESS = "#087b7b"
WARNING = "#8c713e"
DANGER = "#b94c4c"
SOFT_TEAL = "#e2f5f4"
SOFT_RED = "#f8e8e8"
SOFT_AMBER = "#edf1ef"
FONT_FAMILY = "Avenir Next"

def limpiar(contenido):
    for widget in contenido.winfo_children():
        widget.destroy()
    canvas = getattr(contenido, "_scroll_canvas", None)
    if canvas is not None:
        canvas.yview_moveto(0)


def titulo(contenido, texto, subtitulo=""):
    ttk.Label(contenido, text=texto, style="Title.TLabel").pack(anchor="w", pady=(0, 3))
    if subtitulo:
        ttk.Label(contenido, text=subtitulo, style="Subtitle.TLabel").pack(anchor="w", pady=(0, 22))


def tarjeta(parent, titulo_texto, valor, detalle="", color=TEXT):
    frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=16)
    frame.pack_propagate(False)
    tk.Label(frame, text=titulo_texto.upper(), font=(FONT_FAMILY, 10, "bold"), fg=MUTED, bg=CARD).pack(anchor="w")
    tk.Label(frame, text=valor, font=(FONT_FAMILY, 23, "bold"), fg=color, bg=CARD).pack(anchor="w", pady=(7, 2))
    if detalle:
        tk.Label(frame, text=detalle, font=(FONT_FAMILY, 10), fg=MUTED, bg=CARD, wraplength=260, justify="left").pack(anchor="w")
    return frame


def boton(parent, texto, comando, principal=False):
    normal = ACCENT if principal else CARD
    hover = ACCENT_DARK if principal else "#e8f4f4"
    widget = tk.Button(
        parent,
        text=texto,
        command=comando,
        font=(FONT_FAMILY, 10, "bold"),
        fg=CARD if principal else TEXT,
        bg=normal,
        activeforeground=CARD if principal else TEXT,
        activebackground=hover,
        relief="flat",
        bd=0,
        highlightthickness=1 if not principal else 0,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        padx=12,
        pady=8,
        cursor="hand2",
    )
    widget.bind("<Enter>", lambda _event: widget.configure(bg=hover))
    widget.bind("<Leave>", lambda _event: widget.configure(bg=normal))
    return widget


def crear_scroll(parent):
    exterior = tk.Frame(parent, bg=BG)
    canvas = tk.Canvas(exterior, bg=BG, highlightthickness=0)
    barra = ttk.Scrollbar(exterior, orient="vertical", command=canvas.yview)
    contenido = tk.Frame(canvas, bg=BG, padx=34, pady=30)
    ventana = canvas.create_window((0, 0), window=contenido, anchor="nw")
    canvas.configure(yscrollcommand=barra.set)

    def actualizar(_=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def ancho(event):
        canvas.itemconfigure(ventana, width=event.width)

    contenido.bind("<Configure>", actualizar)
    canvas.bind("<Configure>", ancho)
    canvas.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")

    def rueda(event):
        if event.delta:
            pasos = event.delta if sys.platform == "darwin" else event.delta / 120
            if pasos:
                canvas.yview_scroll(-int(pasos), "units")

    canvas.bind_all("<MouseWheel>", rueda)
    if sys.platform.startswith("linux"):
        canvas.bind_all("<Button-4>", lambda _event: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda _event: canvas.yview_scroll(1, "units"))
    contenido._scroll_canvas = canvas
    exterior.pack(fill="both", expand=True)
    return contenido

__all__ = [
    "BG", "CARD", "SIDEBAR", "TEXT", "MUTED", "BORDER",
    "ACCENT", "ACCENT_DARK", "SUCCESS", "WARNING", "DANGER",
    "SOFT_TEAL", "SOFT_RED", "SOFT_AMBER", "FONT_FAMILY",
    "limpiar", "titulo", "tarjeta", "boton", "crear_scroll",
]

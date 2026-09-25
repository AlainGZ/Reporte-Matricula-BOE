"""Tema visual de la interfaz: paleta institucional y estilos ttk centralizados.

AVISO — colores sin confirmar contra el manual de marca oficial:
No fue posible acceder al manual de identidad visual impreso de UNIMINUTO
desde este entorno (el PDF institucional bloqueó la descarga automática).
Los valores de abajo se tomaron de la extracción pública de brandfetch.com
sobre uniminuto.edu (dorado + neutros) como punto de partida razonable, NO
como copia verificada del manual de marca. Si tienes el kit de marca oficial
(PDF de identidad visual o el archivo de colores del área de comunicaciones),
reemplaza estos valores por los reales — es el único cambio que se necesita
aquí, todo el resto de la interfaz ya está armado para tomarlos de este
archivo.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk

# --- Paleta institucional (pendiente de confirmación oficial, ver aviso arriba) ---
COLOR_ORO = "#FFD300"          # Color principal de marca.
COLOR_ORO_OSCURO = "#C9A400"   # Variante oscura, para hover.
COLOR_AZUL_NOCHE = "#1B2A4A"   # Color secundario: cabecera y texto de énfasis.
COLOR_GRIS_CLARO = "#F4F4F4"   # Fondo neutro de paneles secundarios.
COLOR_GRIS_TEXTO = "#4A4A4A"   # Texto de cuerpo.
COLOR_BLANCO = "#FFFFFF"
COLOR_ERROR = "#C0392B"
COLOR_EXITO = "#2E7D32"

FUENTE_TITULO = ("Segoe UI", 16, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 10, "bold")
FUENTE_MENSAJE = ("Segoe UI", 11)
FUENTE_PASO = ("Segoe UI", 10, "bold")


def aplicar_tema(raiz: tk.Tk) -> None:
    """Configura los estilos ttk usados por toda la ventana. Se llama una sola
    vez, al construir la ventana principal."""
    estilo = ttk.Style(raiz)
    try:
        # "clam" es el único tema base incluido en Tk que permite recolorear
        # fondos y bordes de botones/progressbar de forma consistente en
        # Windows; el tema por defecto ("vista"/"xpnative") ignora esos colores.
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    raiz.configure(background=COLOR_BLANCO)

    estilo.configure("Cabecera.TFrame", background=COLOR_AZUL_NOCHE)
    estilo.configure(
        "LogoCabecera.TLabel",
        background=COLOR_AZUL_NOCHE,
    )
    estilo.configure(
        "TituloCabecera.TLabel",
        background=COLOR_AZUL_NOCHE,
        foreground=COLOR_BLANCO,
        font=FUENTE_TITULO,
    )
    estilo.configure(
        "SubtituloCabecera.TLabel",
        background=COLOR_AZUL_NOCHE,
        foreground=COLOR_ORO,
        font=FUENTE_SUBTITULO,
    )
    estilo.configure(
        "PasoCabecera.TLabel",
        background=COLOR_AZUL_NOCHE,
        foreground=COLOR_BLANCO,
        font=FUENTE_PASO,
    )

    estilo.configure("Central.TFrame", background=COLOR_BLANCO)
    estilo.configure(
        "Mensaje.TLabel",
        background=COLOR_BLANCO,
        foreground=COLOR_GRIS_TEXTO,
        font=FUENTE_MENSAJE,
    )
    estilo.configure(
        "MensajeError.TLabel",
        background=COLOR_BLANCO,
        foreground=COLOR_ERROR,
        font=FUENTE_MENSAJE,
    )
    estilo.configure(
        "MensajeExito.TLabel",
        background=COLOR_BLANCO,
        foreground=COLOR_EXITO,
        font=FUENTE_MENSAJE,
    )

    estilo.configure(
        "Principal.TButton",
        font=FUENTE_BOTON,
        foreground=COLOR_AZUL_NOCHE,
        background=COLOR_ORO,
        padding=(20, 10),
        borderwidth=0,
        focusthickness=0,
    )
    estilo.map(
        "Principal.TButton",
        background=[("active", COLOR_ORO_OSCURO), ("disabled", COLOR_GRIS_CLARO)],
        foreground=[("disabled", COLOR_GRIS_TEXTO)],
    )

    estilo.configure(
        "Secundario.TButton",
        font=FUENTE_BOTON,
        foreground=COLOR_AZUL_NOCHE,
        background=COLOR_GRIS_CLARO,
        padding=(20, 10),
        borderwidth=0,
        focusthickness=0,
    )
    estilo.map("Secundario.TButton", background=[("active", "#E0E0E0")])

    estilo.configure("Pie.TFrame", background=COLOR_GRIS_CLARO)

    estilo.configure(
        "Institucional.Horizontal.TProgressbar",
        troughcolor=COLOR_GRIS_CLARO,
        background=COLOR_ORO,
        bordercolor=COLOR_GRIS_CLARO,
        lightcolor=COLOR_ORO,
        darkcolor=COLOR_ORO_OSCURO,
        thickness=10,
    )

"""Ventana principal de la aplicación de escritorio.

Conduce el mismo orquestador que usa la consola, pero traduce cada
`ResultadoEtapa` a una pantalla gráfica: barra de progreso, mensajes, y —cuando
una etapa pide revisión— una vista previa editable con una pestaña por hoja del
Excel intermedio. El usuario corrige lo que necesite y, al aprobar, sus cambios
se guardan de vuelta al archivo antes de continuar.

No contiene lógica de negocio: solo presenta y recoge decisiones. Toda la lógica
vive en `dominio/` y la coordinación en `nucleo/`.
"""

from __future__ import annotations
from datetime import date
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import pandas as pd

from ..nucleo.etapa import Contexto
from ..nucleo.orquestador import Orquestador
from ..nucleo.resultado import ResultadoEtapa, TipoResultado
from ..nucleo import excel_io
from ..etapas.etapa1_matricula_base import EtapaMatriculaBase
from . import tema
from .tabla_editable import TablaEditable

#: Ruta del logo institucional. Es opcional: si el archivo no existe, la
#: cabecera simplemente se muestra sin logo. Coloca aquí el PNG oficial
#: (fondo transparente, alto recomendado ~120px) para que aparezca.
RUTA_LOGO = Path(__file__).resolve().parents[3] / "assets" / "logo_uniminuto.png"


def _cargar_logo() -> tk.PhotoImage | None:
    """Carga el logo institucional si está disponible, reducido a un alto
    razonable para la cabecera. Nunca lanza: si falta el archivo o Tk no
    puede leerlo, la interfaz sigue funcionando sin logo."""
    if not RUTA_LOGO.exists():
        return None
    try:
        imagen = tk.PhotoImage(file=str(RUTA_LOGO))
    except tk.TclError:
        return None
    alto_objetivo = 56
    if imagen.height() > alto_objetivo:
        factor = max(1, imagen.height() // alto_objetivo)
        imagen = imagen.subsample(factor, factor)
    return imagen


class VentanaPrincipal(tk.Tk):
    """Aplicación de escritorio para el reporte de matrícula."""

    def __init__(self, carpeta_datos: Path, fecha_reporte: str | None = None) -> None:
        super().__init__()
        tema.aplicar_tema(self)

        self.title("Reporte de Matrícula Financiera — UNIMINUTO")
        self.geometry("1040x620")
        self.minsize(860, 520)

        self._logo_imagen = _cargar_logo()
        if self._logo_imagen is not None:
            self.iconphoto(True, self._logo_imagen)

        self._carpeta_datos = carpeta_datos
        self._fecha_reporte = fecha_reporte
        self._orquestador: Orquestador | None = None
        self._tablas_visibles: dict[str, TablaEditable] = {}
        self._archivo_en_revision: Path | None = None
        self._proceso_iniciado: bool = False
        self._ultimo_resultado: ResultadoEtapa | None = None

        self._construir_cabecera()
        self._construir_area_central()
        self._construir_pie()
        self._preparar_proceso()

    # ---------- Construcción de la interfaz ----------

    def _construir_cabecera(self) -> None:
        cabecera = ttk.Frame(self, style="Cabecera.TFrame", padding=(24, 18))
        cabecera.pack(fill="x")

        fila_superior = ttk.Frame(cabecera, style="Cabecera.TFrame")
        fila_superior.pack(fill="x")

        if self._logo_imagen is not None:
            ttk.Label(fila_superior, image=self._logo_imagen, style="LogoCabecera.TLabel").pack(
                side="left", padx=(0, 16)
            )

        textos = ttk.Frame(fila_superior, style="Cabecera.TFrame")
        textos.pack(side="left", fill="x", expand=True)
        ttk.Label(
            textos, text="Reporte de Matrícula Financiera", style="TituloCabecera.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            textos, text="Coordinación Financiera — UNIMINUTO", style="SubtituloCabecera.TLabel"
        ).pack(anchor="w")

        self._etiqueta_paso = ttk.Label(cabecera, text="", style="PasoCabecera.TLabel")
        self._etiqueta_paso.pack(anchor="w", pady=(14, 0))

        self._barra = ttk.Progressbar(
            cabecera, mode="determinate", style="Institucional.Horizontal.TProgressbar"
        )
        self._barra.pack(fill="x", pady=(8, 0))

    def _construir_area_central(self) -> None:
        self._centro = ttk.Frame(self, style="Central.TFrame", padding=(24, 20))
        self._centro.pack(fill="both", expand=True)

        self._mensaje = ttk.Label(
            self._centro, text="", style="Mensaje.TLabel", wraplength=980, justify="left"
        )
        self._mensaje.pack(anchor="w", pady=(0, 8))

        # Contenedor donde se montan las pestañas de vista previa, si alguna
        # etapa futura vuelve a pedir revisión antes de continuar.
        self._contenedor_preview = ttk.Frame(self._centro, style="Central.TFrame")
        self._contenedor_preview.pack(fill="both", expand=True)

    def _construir_pie(self) -> None:
        pie = ttk.Frame(self, style="Pie.TFrame", padding=(24, 18))
        pie.pack(fill="x")

        self._boton_secundario = ttk.Button(
            pie, text="Cancelar", style="Secundario.TButton", command=self._cancelar
        )
        self._boton_secundario.pack(side="left")

        self._boton_principal = ttk.Button(
            pie, text="Seleccionar archivo", style="Principal.TButton", command=self._accion_principal
        )
        self._boton_principal.pack(side="right")

    # ---------- Preparación del proceso ----------

    def _preparar_proceso(self) -> None:
        contexto = self._construir_contexto()
        etapas = [
            EtapaMatriculaBase(),
            # Próximas etapas (rectoría, recibos, fortalecimiento) se agregan aquí.
        ]
        self._orquestador = Orquestador(etapas, contexto)
        self._proceso_iniciado = False
        self._actualizar_progreso()
        self._mensaje.config(
            text=(
                "Presiona \"Seleccionar archivo\" y elige el Excel de matrícula "
                "descargado, esté donde esté guardado en tu computador."
            )
        )
        self._boton_principal.config(text="Seleccionar archivo")

    def _construir_contexto(self) -> Contexto:
        fecha = self._fecha_reporte or date.today().strftime("%d.%m.%Y")
        contexto = Contexto(
            carpeta_entrada=self._carpeta_datos / "entrada",
            carpeta_salida=self._carpeta_datos / "salida",
            carpeta_historico=self._carpeta_datos / "historico",
            carpeta_temporal=self._carpeta_datos / "temporal",
            fecha_reporte=fecha,
        )
        for carpeta in (contexto.carpeta_entrada, contexto.carpeta_salida,
                        contexto.carpeta_historico, contexto.carpeta_temporal):
            carpeta.mkdir(parents=True, exist_ok=True)
        return contexto

    # ---------- Flujo por pasos ----------

    def _accion_principal(self) -> None:
        """El botón principal cambia de significado según el estado:
        Seleccionar archivo / Aprobar y continuar / Ya lo tengo / Cerrar."""
        if self._orquestador is None or self._orquestador.terminado:
            self.destroy()
            return

        if not self._proceso_iniciado:
            self._seleccionar_archivo_y_comenzar()
            return

        # Si hay una revisión pendiente, guardar las ediciones antes de continuar.
        if self._archivo_en_revision is not None:
            self._guardar_ediciones_revision()
            self._archivo_en_revision = None
            self._limpiar_preview()
            self._orquestador.confirmar_y_continuar()

        self._ejecutar_siguiente()

    def _seleccionar_archivo_y_comenzar(self) -> None:
        """Abre el cuadro de búsqueda del explorador de archivos, y con el
        archivo elegido arranca el proceso de inmediato, sin importar en qué
        carpeta esté guardado."""
        ruta = filedialog.askopenfilename(
            parent=self,
            title="Selecciona el archivo de matrícula financiera",
            filetypes=[("Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return  # El usuario canceló el diálogo; se queda en la pantalla inicial.

        assert self._orquestador is not None
        self._orquestador.contexto.archivo_seleccionado = Path(ruta)
        self._proceso_iniciado = True
        self._mensaje.config(text=f"Archivo seleccionado:\n{ruta}\n\nProcesando...")
        self._boton_principal.config(state="disabled")
        self.update_idletasks()
        self._boton_principal.config(state="normal")
        self._ejecutar_siguiente()

    def _ejecutar_siguiente(self) -> None:
        if self._orquestador is None:
            return
        if self._orquestador.terminado:
            self._finalizar()
            return

        self._actualizar_progreso()
        resultado = self._orquestador.avanzar()
        self._procesar_resultado(resultado)

    def _procesar_resultado(self, resultado: ResultadoEtapa) -> None:
        self._mensaje.config(text=resultado.mensaje, style="Mensaje.TLabel")
        self._ultimo_resultado = resultado

        if resultado.tipo is TipoResultado.ERROR:
            self._mensaje.config(style="MensajeError.TLabel")
            messagebox.showerror("Error en el proceso", f"{resultado.mensaje}\n\n{resultado.detalle_error}")
            self._boton_principal.config(text="Cerrar")
            return

        if resultado.tipo is TipoResultado.CONTINUAR:
            self._ejecutar_siguiente()
            return

        if resultado.tipo is TipoResultado.REVISION_USUARIO:
            self._mostrar_revision(resultado)
            return

        if resultado.tipo is TipoResultado.ESPERAR_ARCHIVO:
            self._mostrar_espera(resultado)
            return

    def _mostrar_revision(self, resultado: ResultadoEtapa) -> None:
        self._archivo_en_revision = resultado.archivo_generado
        self._montar_preview(resultado.archivo_generado)
        self._boton_principal.config(text="Aprobar y continuar")

    def _mostrar_espera(self, resultado: ResultadoEtapa) -> None:
        requerido = resultado.archivo_requerido
        detalle = f"{resultado.mensaje}\n\nArchivo a proporcionar: {requerido.nombre_sugerido}\n{requerido.instrucciones}"
        self._mensaje.config(text=detalle)
        self._boton_principal.config(text="Ya lo tengo, continuar")

    # ---------- Vista previa editable ----------

    def _montar_preview(self, ruta_excel: Path) -> None:
        self._limpiar_preview()

        cuaderno = ttk.Notebook(self._contenedor_preview)
        cuaderno.pack(fill="both", expand=True)

        hojas = excel_io.leer_hojas(ruta_excel)  # {hoja: df}
        for nombre_hoja, df in hojas.items():
            marco = ttk.Frame(cuaderno)
            tabla = TablaEditable(marco, df)
            tabla.pack(fill="both", expand=True)
            if tabla.filas_ocultas() > 0:
                ttk.Label(
                    marco,
                    text=(
                        f"Mostrando las primeras {len(df) - tabla.filas_ocultas()} filas "
                        f"de {len(df)}. Las ediciones sobre filas visibles se guardan."
                    ),
                    foreground="#8a6d00",
                ).pack(anchor="w", pady=(4, 0))
            cuaderno.add(marco, text=nombre_hoja)
            self._tablas_visibles[nombre_hoja] = tabla

    def _guardar_ediciones_revision(self) -> None:
        if self._archivo_en_revision is None or not self._tablas_visibles:
            return
        hojas = {nombre: tabla.dataframe for nombre, tabla in self._tablas_visibles.items()}
        excel_io.guardar_hojas(hojas, self._archivo_en_revision)

    def _limpiar_preview(self) -> None:
        for hijo in self._contenedor_preview.winfo_children():
            hijo.destroy()
        self._tablas_visibles.clear()

    # ---------- Auxiliares ----------

    def _actualizar_progreso(self) -> None:
        if self._orquestador is None:
            return
        actual, total = self._orquestador.progreso
        self._etiqueta_paso.config(text=f"Paso {actual} de {total}")
        self._barra.config(maximum=total, value=actual - 1)

    def _finalizar(self) -> None:
        contexto = self._orquestador.contexto if self._orquestador else None
        salida = contexto.carpeta_salida if contexto else ""
        self._limpiar_preview()

        detalle = self._ultimo_resultado.mensaje if self._ultimo_resultado else ""
        self._mensaje.config(
            text=f"{detalle}\n\nArchivo exportado en:\n{salida}",
            style="MensajeExito.TLabel",
        )
        self._etiqueta_paso.config(text="Completado")
        self._barra.config(value=self._barra["maximum"])
        self._boton_principal.config(text="Cerrar")
        self._boton_secundario.config(state="disabled")

    def _cancelar(self) -> None:
        if messagebox.askyesno("Cancelar", "¿Seguro que quieres cancelar el proceso?"):
            self.destroy()


def iniciar_aplicacion(carpeta_datos: Path, fecha_reporte: str | None = None) -> None:
    app = VentanaPrincipal(carpeta_datos, fecha_reporte)
    app.mainloop()

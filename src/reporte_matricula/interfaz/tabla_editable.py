"""Tabla editable para vista previa de DataFrames.

Basada en ttk.Treeview (incluido en Python, sin dependencias externas). Muestra
un DataFrame en una rejilla con scroll y permite editar una celda con doble
clic: aparece un campo de texto sobre la celda y, al confirmar con Enter, el
valor se guarda de vuelta en el DataFrame. Pensada para que el usuario corrija
datos puntuales antes de aprobar una etapa.

Para archivos grandes se muestran solo las primeras filas (configurable), porque
Treeview no está pensado para decenas de miles de filas fluidas; el propósito de
la vista previa es revisar y corregir, no navegar toda la data.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk

import pandas as pd


class TablaEditable(ttk.Frame):
    """Rejilla con scroll que refleja y edita un DataFrame in situ."""

    def __init__(self, maestro: tk.Misc, df: pd.DataFrame, max_filas: int = 500) -> None:
        super().__init__(maestro)
        self._df = df
        self._max_filas = max_filas
        self._editor: tk.Entry | None = None
        self._columnas = [str(c) for c in df.columns]

        self._construir_tabla()
        self._poblar()

    @property
    def dataframe(self) -> pd.DataFrame:
        """El DataFrame con las ediciones aplicadas."""
        return self._df

    def filas_ocultas(self) -> int:
        """Cuántas filas no se muestran por el límite de vista previa."""
        return max(0, len(self._df) - self._max_filas)

    def _construir_tabla(self) -> None:
        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True)

        self._tree = ttk.Treeview(
            contenedor, columns=self._columnas, show="headings", selectmode="browse"
        )
        for columna in self._columnas:
            self._tree.heading(columna, text=columna)
            self._tree.column(columna, width=120, anchor="w", stretch=False)

        scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=self._tree.yview)
        scroll_x = ttk.Scrollbar(contenedor, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self._tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)

        self._tree.bind("<Double-1>", self._al_doble_clic)

    def _poblar(self) -> None:
        filas_a_mostrar = min(len(self._df), self._max_filas)
        for indice in range(filas_a_mostrar):
            valores = [self._formatear(self._df.iat[indice, col]) for col in range(len(self._columnas))]
            # El iid del Treeview es el índice posicional de la fila, como texto.
            self._tree.insert("", "end", iid=str(indice), values=valores)

    @staticmethod
    def _formatear(valor: object) -> str:
        if pd.isna(valor):
            return ""
        return str(valor)

    def _al_doble_clic(self, evento: tk.Event) -> None:
        if self._tree.identify_region(evento.x, evento.y) != "cell":
            return
        fila_iid = self._tree.identify_row(evento.y)
        columna_id = self._tree.identify_column(evento.x)
        if not fila_iid or not columna_id:
            return
        self._abrir_editor(fila_iid, columna_id)

    def _abrir_editor(self, fila_iid: str, columna_id: str) -> None:
        self._cerrar_editor()

        indice_columna = int(columna_id.replace("#", "")) - 1
        caja = self._tree.bbox(fila_iid, columna_id)
        if not caja:
            return
        x, y, ancho, alto = caja
        valor_actual = self._tree.set(fila_iid, self._columnas[indice_columna])

        editor = tk.Entry(self._tree)
        editor.place(x=x, y=y, width=ancho, height=alto)
        editor.insert(0, valor_actual)
        editor.focus_set()
        editor.select_range(0, "end")

        editor.bind("<Return>", lambda e: self._guardar_editor(fila_iid, indice_columna))
        editor.bind("<Escape>", lambda e: self._cerrar_editor())
        editor.bind("<FocusOut>", lambda e: self._guardar_editor(fila_iid, indice_columna))
        self._editor = editor

    def _guardar_editor(self, fila_iid: str, indice_columna: int) -> None:
        if self._editor is None:
            return
        nuevo_valor = self._editor.get()
        columna = self._columnas[indice_columna]

        self._tree.set(fila_iid, columna, nuevo_valor)
        indice_fila = int(fila_iid)
        self._df.iat[indice_fila, indice_columna] = self._convertir_al_tipo(columna, nuevo_valor)

        self._cerrar_editor()

    def _convertir_al_tipo(self, columna: str, valor: str) -> object:
        """Intenta conservar el tipo numérico de la columna; si no, deja texto."""
        if valor == "":
            return None
        if pd.api.types.is_numeric_dtype(self._df[columna].dtype):
            try:
                numero = float(valor)
                return int(numero) if numero.is_integer() else numero
            except ValueError:
                return valor
        return valor

    def _cerrar_editor(self) -> None:
        if self._editor is not None:
            self._editor.destroy()
            self._editor = None

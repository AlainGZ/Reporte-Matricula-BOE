"""Lectura y escritura de archivos Excel, centralizada.

Aísla la dependencia de pandas/openpyxl para que las etapas no repitan la lógica
de guardado y para poder cambiar el motor en un solo lugar si hiciera falta.
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd


def guardar_hojas(hojas: dict[str, pd.DataFrame], ruta_salida: Path) -> Path:
    """Guarda un diccionario {nombre_hoja: DataFrame} como un Excel de varias
    hojas. Las hojas se ordenan por nombre para una salida estable."""
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(ruta_salida, engine="openpyxl") as writer:
        for nombre, df in sorted(hojas.items()):
            # Excel limita los nombres de hoja a 31 caracteres.
            df.to_excel(writer, sheet_name=nombre[:31], index=False)
    return ruta_salida


def leer_hojas(ruta: Path) -> dict[str, pd.DataFrame]:
    """Lee todas las hojas de un Excel como {nombre_hoja: DataFrame}."""
    return pd.read_excel(ruta, sheet_name=None)


def leer_hoja(ruta: Path, hoja="0", fila_encabezado: int = 0) -> pd.DataFrame:
    """Lee una hoja concreta. `fila_encabezado` es 0-indexada."""
    return pd.read_excel(ruta, sheet_name=hoja, header=fila_encabezado)


def contar_filas(hojas: dict[str, pd.DataFrame]) -> int:
    return sum(len(df) for df in hojas.values())

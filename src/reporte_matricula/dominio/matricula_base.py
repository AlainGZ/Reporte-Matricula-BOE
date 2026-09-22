"""Transformaciones de la matrícula base — el reemplazo de la macro VBA.

Cada función es pura: recibe un DataFrame y devuelve uno nuevo, sin efectos
secundarios ni acceso a disco. Esto las hace fáciles de probar de forma aislada
y de recombinar. La lectura y el guardado viven en la etapa que las orquesta.

El orden de ejecución de `procesar_matricula_base` replica exactamente la
subrutina `MetodoAbrirLibro` del VBA original, más la deduplicación por llave
de 4 campos que el proceso manual hace después de la macro.
"""

from __future__ import annotations
import pandas as pd

from . import columnas as C


def cargar_hoja_detalle(ruta, hoja: str = C.HOJA_FUENTE_DETALLE) -> pd.DataFrame:
    """Lee la hoja de detalle. Los encabezados están en la fila 2 (header=1) y la
    columna A no tiene encabezado (columna vacía del proceso manual): pandas la
    lee como 'Unnamed: 0' y aquí se descarta."""
    df = pd.read_excel(ruta, sheet_name=hoja, header=1)
    return df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]


def preprocesamiento_manual(df: pd.DataFrame) -> pd.DataFrame:
    """Paso 0 (manual, previo a la macro): borra CCP Propio y Desc_convenios si
    existen; pone Valor Convenio en 0."""
    df = df.copy()
    for columna in (C.COL_CCP_PROPIO, C.COL_DESC_CONVENIOS):
        if columna in df.columns:
            df = df.drop(columns=[columna])
    if C.COL_VALOR_CONVENIO in df.columns:
        df[C.COL_VALOR_CONVENIO] = 0
    return df


def limpiar_y_normalizar(df: pd.DataFrame) -> pd.DataFrame:
    """Fija Rectoría y Sede, borra columnas demográficas y Banner, quita la
    última fila (totales)."""
    df = df.copy()
    df[C.COL_RECTORIA] = C.VALOR_RECTORIA
    df[C.COL_SEDE] = C.VALOR_SEDE
    a_borrar = [c for c in C.COLS_DEMOGRAFICAS_A_BORRAR + [C.COL_CODIGO_BANNER] if c in df.columns]
    df = df.drop(columns=a_borrar)
    return df.iloc[:-1].reset_index(drop=True)


def convertir_columnas_a_numero(df: pd.DataFrame) -> pd.DataFrame:
    """ConvertirTextoANumero: Interlocutor, Código Centro Costo, Snies,
    # Factura, # Pedido. 'Tipo estudiante' NO se convierte: destruiría valores
    de texto como 'Nuevo' / 'Continuo'."""
    df = df.copy()
    for columna in (C.COL_INTERLOCUTOR, C.COL_CODIGO_CENTRO_COSTO, C.COL_SNIES,
                    C.COL_NUM_FACTURA, C.COL_NUM_PEDIDO):
        if columna in df.columns:
            df[columna] = pd.to_numeric(df[columna], errors="coerce")
    return df


def eliminar_filas_con_cero(df: pd.DataFrame) -> pd.DataFrame:
    """eliminarCeroAB + eliminarCeroAC: quita filas con Cant matricula o
    Ingreso bruto en cero. El VBA no filtra por # Pedido."""
    df = df.copy()
    if C.COL_CANT_MATRICULA in df.columns:
        df = df[df[C.COL_CANT_MATRICULA] != 0]
    if C.COL_INGRESO_BRUTO in df.columns:
        df = df[df[C.COL_INGRESO_BRUTO] != 0]
    return df.reset_index(drop=True)


def aplicar_sumif_ingreso_bruto(df: pd.DataFrame) -> pd.DataFrame:
    """Sumar_si: agrupa Ingreso bruto por # Factura (SUMIF sobre # Factura)."""
    df = df.copy()
    if C.COL_NUM_FACTURA in df.columns and C.COL_INGRESO_BRUTO in df.columns:
        df[C.COL_INGRESO_BRUTO] = df.groupby(C.COL_NUM_FACTURA)[C.COL_INGRESO_BRUTO].transform("sum")
    return df


def calcular_ingreso_neto(df: pd.DataFrame) -> pd.DataFrame:
    """suma: Ingreso neto = suma de las columnas financieras (validado con
    datos reales)."""
    df = df.copy()
    presentes = [c for c in C.COLS_SUMA_INGRESO_NETO if c in df.columns]
    for c in presentes:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    df[C.COL_INGRESO_NETO] = df[presentes].sum(axis=1)
    return df


def filtrar_por_prefijo_pedido(df: pd.DataFrame) -> pd.DataFrame:
    """EliminarFilaSiEmpiezaCon6/7: quita filas cuyo # Pedido empieza en 6 o 7."""
    df = df.copy()
    if C.COL_NUM_PEDIDO not in df.columns:
        return df
    prefijo = df[C.COL_NUM_PEDIDO].astype("Int64").astype(str)
    return df[~prefijo.str.match(r"^[67]")].reset_index(drop=True)


def aplicar_ajustes_hardcodeados(df: pd.DataFrame) -> pd.DataFrame:
    """modificarBeca + modificaridliz + FiltrarYEliminarDatosRepetidos
    (9 condiciones: 4 por nombre + 5 por pedido)."""
    df = df.copy()

    if C.COL_NUM_PEDIDO in df.columns and C.COL_BECA in df.columns:
        df.loc[df[C.COL_NUM_PEDIDO] == C.AJUSTE_BECA_PEDIDO, C.COL_BECA] = C.AJUSTE_BECA_VALOR

    if C.COL_NUM_PEDIDO in df.columns and C.COL_TIPO_ESTUDIANTE in df.columns:
        df.loc[df[C.COL_NUM_PEDIDO] == C.AJUSTE_TIPO_ESTUDIANTE_PEDIDO,
               C.COL_TIPO_ESTUDIANTE] = C.AJUSTE_TIPO_ESTUDIANTE_VALOR

    if C.COL_INTERLOCUTOR in df.columns and C.COL_NOMBRES in df.columns:
        for interlocutor, nombre in C.FILAS_A_ELIMINAR_POR_NOMBRE:
            df = df[~((df[C.COL_INTERLOCUTOR] == interlocutor) & (df[C.COL_NOMBRES] == nombre))]

    if C.COL_INTERLOCUTOR in df.columns and C.COL_NUM_PEDIDO in df.columns:
        for interlocutor, pedido in C.FILAS_A_ELIMINAR_POR_PEDIDO:
            df = df[~((df[C.COL_INTERLOCUTOR] == interlocutor) & (df[C.COL_NUM_PEDIDO] == pedido))]

    return df.reset_index(drop=True)


def normalizar_nombres_programa(df: pd.DataFrame) -> pd.DataFrame:
    """filtrarYModificarx/xx: corrige nombres de programa solo en los años que
    la macro corrige. Se aplica antes de segmentar para que quede en cada hoja."""
    df = df.copy()
    if C.COL_PROGRAMA not in df.columns:
        return df
    anio_col = df[C.COL_PERIODO_ACADEMICO].astype(str).str[:4]
    for incorrecto, correcto in C.CORRECCIONES_PROGRAMA.items():
        anios = C.ANIOS_POR_CORRECCION.get(incorrecto)
        mask = df[C.COL_PROGRAMA].astype(str).str.upper() == incorrecto
        if anios is not None:
            mask &= anio_col.isin(anios)
        df.loc[mask, C.COL_PROGRAMA] = correcto
    return df


def crear_llave_y_deduplicar(df: pd.DataFrame) -> pd.DataFrame:
    """Llave de 4 campos (Interlocutor + Periodo Académico + Código programa SAP
    + Concepto Matrícula), orden Matr. Financiera de Z a A para conservar 'SI'
    sobre 'NO', quita duplicados por la llave, ordena Interlocutor ascendente."""
    df = df.copy()
    df["_llave"] = (
        df[C.COL_INTERLOCUTOR].astype(str)
        + df[C.COL_PERIODO_ACADEMICO].astype(str)
        + df[C.COL_PROGRAMA_SAP].astype(str)
        + df[C.COL_CONCEPTO_MATRICULA].astype(str)
    )
    df = df.sort_values(C.COL_MATR_FINANCIERA, ascending=False)
    df = df.drop_duplicates(subset="_llave", keep="first")
    df = df.drop(columns="_llave")
    return df.sort_values(C.COL_INTERLOCUTOR, ascending=True).reset_index(drop=True)


def restaurar_columnas_duplicadas(df: pd.DataFrame) -> pd.DataFrame:
    """El archivo fuente tiene 'Crédito convenio' dos veces; pandas renombra la
    segunda a 'Crédito convenio.1' al leerla. Se restaura el nombre original."""
    return df.rename(columns=lambda c: "Crédito convenio" if c == "Crédito convenio.1" else c)


def segmentar_por_anio(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """CrearHojas + FiltrarPorAnios: separa en hojas por año del periodo
    académico (primeros 4 dígitos)."""
    df = df.copy()
    df["_anio"] = df[C.COL_PERIODO_ACADEMICO].astype(str).str[:4]
    return {
        anio: restaurar_columnas_duplicadas(grupo.drop(columns="_anio").reset_index(drop=True))
        for anio, grupo in df.groupby("_anio")
    }


def procesar_matricula_base(ruta_entrada) -> dict[str, pd.DataFrame]:
    """Ejecuta todo el proceso en el orden exacto de MetodoAbrirLibro y devuelve
    un diccionario {año: DataFrame}."""
    df = cargar_hoja_detalle(ruta_entrada)
    df = preprocesamiento_manual(df)
    df = limpiar_y_normalizar(df)
    df = convertir_columnas_a_numero(df)
    df = eliminar_filas_con_cero(df)
    df = aplicar_sumif_ingreso_bruto(df)
    df = calcular_ingreso_neto(df)
    df = filtrar_por_prefijo_pedido(df)
    df = aplicar_ajustes_hardcodeados(df)
    df = normalizar_nombres_programa(df)
    df = crear_llave_y_deduplicar(df)
    return segmentar_por_anio(df)

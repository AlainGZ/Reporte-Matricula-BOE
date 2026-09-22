"""Pruebas de las transformaciones de matrícula base.

Verifican que cada regla de negocio confirmada contra el VBA se cumpla, usando
DataFrames pequeños y controlados. No dependen de archivos externos.
"""

from __future__ import annotations
import pandas as pd

from reporte_matricula.dominio import columnas as C
from reporte_matricula.dominio import matricula_base as mb


def test_calcular_ingreso_neto_suma_columnas_correctas():
    # Caso real validado: 5619500 + 0 - 983960 + 0 + 0 - 699700 = 3935840
    df = pd.DataFrame({
        C.COL_INGRESO_BRUTO: [5619500],
        C.COL_BECA: [0],
        C.COL_DESCUENTO: [-983960],
        C.COL_VALOR_CONVENIO: [0],
        C.COL_DESC_PRONTO_PAGO: [0],
        C.COL_SUBSIDIO: [-699700],
    })
    resultado = mb.calcular_ingreso_neto(df)
    assert resultado[C.COL_INGRESO_NETO].iloc[0] == 3935840


def test_eliminar_filas_con_cero_quita_cant_e_ingreso_en_cero():
    df = pd.DataFrame({
        C.COL_CANT_MATRICULA: [1, 0, 1],
        C.COL_INGRESO_BRUTO: [100, 200, 0],
    })
    resultado = mb.eliminar_filas_con_cero(df)
    assert len(resultado) == 1
    assert resultado[C.COL_INGRESO_BRUTO].iloc[0] == 100


def test_filtrar_por_prefijo_pedido_quita_6_y_7():
    df = pd.DataFrame({C.COL_NUM_PEDIDO: [58241205, 60000000, 70000000, 55506999]})
    resultado = mb.filtrar_por_prefijo_pedido(df)
    prefijos = resultado[C.COL_NUM_PEDIDO].astype(str).str[0].tolist()
    assert "6" not in prefijos
    assert "7" not in prefijos
    assert len(resultado) == 2


def test_convertir_columnas_no_toca_tipo_estudiante():
    df = pd.DataFrame({
        C.COL_INTERLOCUTOR: ["4509"],
        C.COL_TIPO_ESTUDIANTE: ["Nuevo"],
    })
    resultado = mb.convertir_columnas_a_numero(df)
    assert resultado[C.COL_INTERLOCUTOR].iloc[0] == 4509
    assert resultado[C.COL_TIPO_ESTUDIANTE].iloc[0] == "Nuevo"


def test_sumif_agrupa_ingreso_bruto_por_factura():
    df = pd.DataFrame({
        C.COL_NUM_FACTURA: [111, 111, 222],
        C.COL_INGRESO_BRUTO: [100, 200, 50],
    })
    resultado = mb.aplicar_sumif_ingreso_bruto(df)
    # Las dos filas de la factura 111 quedan con la suma (300).
    assert resultado.loc[resultado[C.COL_NUM_FACTURA] == 111, C.COL_INGRESO_BRUTO].tolist() == [300, 300]
    assert resultado.loc[resultado[C.COL_NUM_FACTURA] == 222, C.COL_INGRESO_BRUTO].tolist() == [50]


def test_ajuste_beca_por_pedido():
    df = pd.DataFrame({
        C.COL_NUM_PEDIDO: [C.AJUSTE_BECA_PEDIDO, 99999999],
        C.COL_BECA: [0, 0],
        C.COL_INTERLOCUTOR: [1, 2],
        C.COL_NOMBRES: ["X", "Y"],
    })
    resultado = mb.aplicar_ajustes_hardcodeados(df)
    fila = resultado[resultado[C.COL_NUM_PEDIDO] == C.AJUSTE_BECA_PEDIDO]
    assert fila[C.COL_BECA].iloc[0] == C.AJUSTE_BECA_VALOR


def test_ajuste_tipo_estudiante_por_pedido():
    df = pd.DataFrame({
        C.COL_NUM_PEDIDO: [C.AJUSTE_TIPO_ESTUDIANTE_PEDIDO],
        C.COL_TIPO_ESTUDIANTE: ["Continuo"],
        C.COL_INTERLOCUTOR: [1],
        C.COL_NOMBRES: ["X"],
    })
    resultado = mb.aplicar_ajustes_hardcodeados(df)
    assert resultado[C.COL_TIPO_ESTUDIANTE].iloc[0] == C.AJUSTE_TIPO_ESTUDIANTE_VALOR


def test_eliminar_fila_por_nombre_y_por_pedido():
    interlocutor_nombre, nombre = C.FILAS_A_ELIMINAR_POR_NOMBRE[0]
    interlocutor_pedido, pedido = C.FILAS_A_ELIMINAR_POR_PEDIDO[0]
    df = pd.DataFrame({
        C.COL_INTERLOCUTOR: [interlocutor_nombre, interlocutor_pedido, 55555],
        C.COL_NOMBRES: [nombre, "OTRO", "OTRO"],
        C.COL_NUM_PEDIDO: [111, pedido, 222],
    })
    resultado = mb.aplicar_ajustes_hardcodeados(df)
    assert len(resultado) == 1
    assert resultado[C.COL_INTERLOCUTOR].iloc[0] == 55555


def test_deduplicar_conserva_si_sobre_no():
    # Con misma llave, el orden Z→A por Matr. Financiera conserva 'SI'.
    df = pd.DataFrame({
        C.COL_INTERLOCUTOR: [100, 100],
        C.COL_PERIODO_ACADEMICO: ["202625", "202625"],
        C.COL_PROGRAMA_SAP: ["ISY", "ISY"],
        C.COL_CONCEPTO_MATRICULA: ["MATRICULA", "MATRICULA"],
        C.COL_MATR_FINANCIERA: ["NO", "SI"],
    })
    resultado = mb.crear_llave_y_deduplicar(df)
    assert len(resultado) == 1
    assert resultado[C.COL_MATR_FINANCIERA].iloc[0] == "SI"


def test_llave_distingue_por_concepto_matricula():
    # Misma persona/periodo/programa pero distinto concepto => NO son duplicados.
    df = pd.DataFrame({
        C.COL_INTERLOCUTOR: [100, 100],
        C.COL_PERIODO_ACADEMICO: ["202625", "202625"],
        C.COL_PROGRAMA_SAP: ["ISY", "ISY"],
        C.COL_CONCEPTO_MATRICULA: ["MATRICULA", "OTRO CONCEPTO"],
        C.COL_MATR_FINANCIERA: ["SI", "SI"],
    })
    resultado = mb.crear_llave_y_deduplicar(df)
    assert len(resultado) == 2


def test_normalizar_programa_respeta_anios():
    df = pd.DataFrame({
        C.COL_PROGRAMA: ["INGENIERÍA DE SISTEMAS", "INGENIERÍA DE SISTEMAS"],
        C.COL_PERIODO_ACADEMICO: ["202325", "202725"],  # 2023 aplica, 2027 no
    })
    resultado = mb.normalizar_nombres_programa(df)
    assert resultado[C.COL_PROGRAMA].iloc[0] == "Ingeniería De Sistemas"
    assert resultado[C.COL_PROGRAMA].iloc[1] == "INGENIERÍA DE SISTEMAS"


def test_segmentar_por_anio_agrupa_correctamente():
    df = pd.DataFrame({
        C.COL_PERIODO_ACADEMICO: ["202516", "202625", "202507"],
        C.COL_INTERLOCUTOR: [1, 2, 3],
    })
    hojas = mb.segmentar_por_anio(df)
    assert set(hojas.keys()) == {"2025", "2026"}
    assert len(hojas["2025"]) == 2
    assert len(hojas["2026"]) == 1

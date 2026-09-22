"""Nombres de columna y reglas de negocio del reporte de matrícula.

Todos estos valores fueron confirmados contra el código VBA original de la macro
y validados con datos reales. Se centralizan aquí para que ninguna etapa dependa
de letras de columna de Excel (que se rompen al cambiar el orden), sino de los
nombres de encabezado, que son estables.
"""

from __future__ import annotations

HOJA_FUENTE_DETALLE = "Detalle Estudiantes"

# --- Columnas usadas como llaves y clasificadores ---
COL_INTERLOCUTOR = "Interlocutor"
COL_PERIODO_ACADEMICO = "Periodo Académico"
COL_PROGRAMA_SAP = "Código programa SAP"
COL_CONCEPTO_MATRICULA = "Concepto Matrícula"
COL_MATR_FINANCIERA = "Matr. Financiera"
COL_PROGRAMA = "Programa"
COL_NOMBRES = "Nombres"
COL_TIPO_ESTUDIANTE = "Tipo estudiante"

# --- Columnas de identificación numérica (ConvertirTextoANumero del VBA) ---
COL_CODIGO_CENTRO_COSTO = "Código Centro Costo"
COL_SNIES = "Snies"
COL_NUM_FACTURA = "# Factura"
COL_NUM_PEDIDO = "# Pedido"
COL_CANT_MATRICULA = "Cant matricula"

# --- Columnas fijas y a eliminar ---
COL_RECTORIA = "Rectoría/Vicerrectoría"
COL_SEDE = "Sede"
COL_VALOR_CONVENIO = "Valor Convenio"
COL_CCP_PROPIO = "CCP Propio"
COL_DESC_CONVENIOS = "Desc_convenios"
COL_CODIGO_BANNER = "Código Estudiante Banner"

# --- Columnas financieras ---
COL_INGRESO_BRUTO = "Ingreso bruto"
COL_BECA = "Beca"
COL_DESCUENTO = "Descuento"
COL_DESC_PRONTO_PAGO = "Desc. Pronto pago"
COL_SUBSIDIO = "Subsidio"
COL_INGRESO_NETO = "Ingreso neto"

VALOR_RECTORIA = "Rectoría Virtual"
VALOR_SEDE = "Uniminuto Virtual"

# Columnas AO:AY que la macro elimina (datos demográficos).
COLS_DEMOGRAFICAS_A_BORRAR = [
    "Discapacidad", "Estado Civil", "Estrato Social", "Etnia",
    "Fecha Nacimiento", "Género", "Sexualidad", "Hijos", "Sisben",
    "Tipo Estudiante", "Email Uniminuto",
]

# Columnas que se suman para el Ingreso neto (fórmula 'suma' del VBA, validada
# con datos reales: 5619500 + 0 - 983960 + 0 + 0 - 699700 = 3935840).
COLS_SUMA_INGRESO_NETO = [
    COL_INGRESO_BRUTO, COL_BECA, COL_DESCUENTO, COL_VALOR_CONVENIO,
    COL_DESC_PRONTO_PAGO, COL_SUBSIDIO,
]

# --- Ajustes puntuales por estudiante (modificarBeca / modificaridliz del VBA) ---
AJUSTE_BECA_PEDIDO = 53753460
AJUSTE_BECA_VALOR = -2660880
AJUSTE_TIPO_ESTUDIANTE_PEDIDO = 56398563
AJUSTE_TIPO_ESTUDIANTE_VALOR = "Nuevo"

# --- Filas a eliminar (FiltrarYEliminarDatosRepetidos del VBA, 9 condiciones) ---
FILAS_A_ELIMINAR_POR_NOMBRE = [
    (20176, "MARIA MARLENY"),
    (201100, "PAULA ANDREA"),
    (830602, "NANCY XIMENA"),
    (301274, "WIBELINA "),
]
FILAS_A_ELIMINAR_POR_PEDIDO = [
    (890729, 55512006),
    (920206, 55516333),
    (918086, 55500141),
    (758826, 55506999),
    (758826, 55506993),
]

# --- Correcciones de nombre de programa por año (filtrarYModificarx/xx del VBA) ---
CORRECCIONES_PROGRAMA = {
    "INGENIERÍA DE SISTEMAS": "Ingeniería De Sistemas",
    "ESPECIALIZACIÓN EN COMUNICACIÓN CORPORATIVA": "Especialización En Comunicación Corporativa",
}
ANIOS_POR_CORRECCION = {
    "INGENIERÍA DE SISTEMAS": {"2023", "2024"},
    "ESPECIALIZACIÓN EN COMUNICACIÓN CORPORATIVA": {"2023", "2024", "2025", "2026"},
}

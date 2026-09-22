# Proceso de negocio

Describe qué hace el programa en términos del proceso manual que reemplaza, para
que quien mantenga el código entienda el *porqué* de cada paso.

## Contexto

El equipo financiero virtual de UNIMINUTO genera un reporte diario de matrícula a
partir de un archivo descargado de SAP (`Matricula_Financiera-Detalle.xlsx`).
Hasta ahora ese reporte se producía con una macro VBA de Excel que tomaba entre
1 y 1.5 horas y dependía de un equipo específico. Este programa lo reemplaza.

## Fuente de datos

`Matricula_Financiera-Detalle.xlsx`, hoja **"Detalle Estudiantes"**:

- La fila 1 está vacía; los encabezados están en la fila 2.
- La columna A no tiene encabezado (es la columna vacía que el proceso manual usa
  para una llave temporal). El programa la descarta al leer.

## Pasos del proceso (equivalentes a la macro)

Se ejecutan en este orden exacto, replicando la subrutina `MetodoAbrirLibro`:

1. **Cargar** la hoja "Detalle Estudiantes".
2. **Preprocesamiento manual:** borrar las columnas `CCP Propio` y
   `Desc_convenios` si existen; poner `Valor Convenio` en 0.
3. **Limpieza:** fijar `Rectoría/Vicerrectoría` = "Rectoría Virtual" y `Sede` =
   "Uniminuto Virtual"; borrar columnas demográficas y `Código Estudiante Banner`;
   quitar la última fila (totales).
4. **Convertir a número:** `Interlocutor`, `Código Centro Costo`, `Snies`,
   `# Factura`, `# Pedido`. (`Tipo estudiante` NO se convierte: es texto.)
5. **Eliminar filas** con `Cant matricula` o `Ingreso bruto` en cero.
6. **SUMIF:** agrupar `Ingreso bruto` por `# Factura`.
7. **Calcular `Ingreso neto`** = suma de las columnas financieras
   (`Ingreso bruto` + `Beca` + `Descuento` + `Valor Convenio` +
   `Desc. Pronto pago` + `Subsidio`).
8. **Filtrar** las filas cuyo `# Pedido` empieza en 6 o 7.
9. **Ajustes puntuales** (reglas hardcodeadas confirmadas del VBA):
   - `# Pedido` = 53753460 → `Beca` = -2660880.
   - `# Pedido` = 56398563 → `Tipo estudiante` = "Nuevo".
   - Eliminar 9 filas específicas (4 por nombre + 5 por pedido).
10. **Normalizar nombres de programa** en los años correspondientes
    (`INGENIERÍA DE SISTEMAS` → `Ingeniería De Sistemas`, etc.).
11. **Crear llave y deduplicar:** llave = `Interlocutor` + `Periodo Académico` +
    `Código programa SAP` + `Concepto Matrícula`; ordenar `Matr. Financiera` de Z
    a A (para conservar "SI" sobre "NO"); quitar duplicados por la llave; borrar
    la llave; ordenar `Interlocutor` de menor a mayor.
12. **Segmentar por año** en hojas separadas según el `Periodo Académico`.

**Pausa:** el usuario revisa el reporte generado y puede corregir celdas antes de
aprobar.

## Validación

El cálculo del `Ingreso neto` se validó con un caso real:
`5619500 + 0 - 983960 + 0 + 0 - 699700 = 3935840`, que coincide con la salida de
la macro para el mismo estudiante. El resultado completo (62.787 registros en las
hojas 2025 y 2026 para el archivo de prueba) coincide con el de la macro.

## Puntos que conviene revisar periódicamente con el área financiera

- Las **reglas hardcodeadas** del paso 9 (ajustes por estudiante y filas a
  eliminar): pueden corresponder a casos de un período ya cerrado. Están
  centralizadas en `dominio/columnas.py` para poder actualizarlas fácil.
- Las **correcciones de nombre de programa** y los años en que aplican.

## Etapas siguientes del proceso (fuera del alcance de esta versión)

El proceso completo continúa con la conciliación de rectoría, recibos y
fortalecimiento regional, que dependen de archivos adicionales descargados
manualmente. La arquitectura está preparada para incorporarlas como etapas
nuevas (ver `docs/arquitectura.md` → "Cómo agregar una etapa nueva"), pero no
forman parte de esta entrega, centrada en el reemplazo de la macro.

# Manual de usuario

Dirigido al equipo financiero que usa el programa a diario. No requiere
conocimientos técnicos.

## Qué hace el programa

Toma el archivo de matrícula que descargas y genera, en segundos, el mismo
reporte que antes hacía la macro (organizado por año), dándote la oportunidad de
revisarlo y corregirlo antes de guardarlo.

## Antes de empezar (una sola vez)

Tu equipo debe tener Python instalado y las dependencias listas. Si no es así,
pídele al área técnica que siga el `manual_instalacion.md`. Para el uso diario no
necesitas hacer nada de eso.

## Paso a paso

### 1. Coloca el archivo de entrada

Descarga el archivo `Matricula_Financiera-Detalle...xlsx` como lo haces
normalmente y guárdalo en la carpeta **`datos/entrada`** del programa.

> No importa si el nombre trae una fecha al final (por ejemplo
> `Matricula_Financiera-Detalle_03.03.2026.xlsx`): el programa lo reconoce igual.

### 2. Abre el programa

Haz doble clic en **`scripts/ejecutar.bat`** (o pídele al área técnica que te deje
un acceso directo). Se abrirá una ventana con el título *"Reporte de Matrícula
Financiera — Uniminuto"*.

### 3. Presiona "Iniciar"

El programa procesa el archivo. En unos segundos verás una **vista previa** con
varias pestañas, una por cada año (2025, 2026, ...).

### 4. Revisa y corrige si hace falta

- Recorre las pestañas y revisa que los datos estén bien.
- Si necesitas cambiar un dato, **haz doble clic sobre la celda**, escribe el
  valor correcto y presiona **Enter**.
- Puedes corregir tantas celdas como quieras.

> La vista previa muestra las primeras 500 filas de cada año. Si necesitas
> revisar más allá de eso, avísale al área técnica.

### 5. Aprueba y termina

Cuando todo esté bien, presiona **"Aprobar y continuar"**. Tus correcciones se
guardan y el reporte final queda en la carpeta **`datos/salida`** con el nombre
`reporte_matricula_<fecha>.xlsx`.

## Preguntas frecuentes

**No aparece la vista previa y sale un error rojo.**
El programa no encontró el archivo o le falta una columna. Verifica que el
archivo esté en `datos/entrada` y que sea el correcto. El mensaje de error indica
qué pasó.

**Me equivoqué en una corrección.**
Vuelve a hacer doble clic en la celda y escribe el valor correcto antes de
aprobar. Nada se guarda hasta que presiones "Aprobar y continuar".

**¿Puedo cambiar la fecha del reporte?**
Sí, pero eso se hace desde la línea de comandos (`--fecha`). Pídele al área
técnica que te lo configure si lo necesitas seguido.

**El programa se ve distinto / no abre la ventana.**
Puede que Python no esté bien instalado en ese equipo. Consulta al área técnica y
al `manual_instalacion.md`.

## A quién acudir

Si algo no funciona y no está resuelto aquí, contacta al área técnica o a la
persona responsable del reporte en la Coordinación Financiera Virtual.

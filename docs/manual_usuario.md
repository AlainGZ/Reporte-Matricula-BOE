# Manual de usuario

Dirigido al equipo financiero que usa el programa a diario. No requiere
conocimientos técnicos.

## Qué hace el programa

Toma el archivo de matrícula que descargas y genera el mismo reporte que antes
hacía la macro (organizado por año), listo en la carpeta de salida.

## Antes de empezar (una sola vez)

Tu equipo debe tener Python instalado y las dependencias listas. Si no es así,
pídele al área técnica que siga el `manual_instalacion.md`. Para el uso diario no
necesitas hacer nada de eso.

## Paso a paso

### 1. Abre el programa

Haz doble clic en **`scripts/ejecutar.bat`** (o pídele al área técnica que te deje
un acceso directo). Se abrirá una ventana con el título *"Reporte de Matrícula
Financiera — Uniminuto"*.

### 2. Selecciona el archivo

Presiona **"Seleccionar archivo"**. Se abre el cuadro de búsqueda de archivos de
Windows: navega hasta donde tengas guardado el `Matricula_Financiera-Detalle...xlsx`
(Descargas, OneDrive, el escritorio, donde sea) y ábrelo. No es necesario copiarlo
a ninguna carpeta especial del programa.

### 3. El programa procesa y exporta el archivo automáticamente

Al elegir el archivo, el procesamiento empieza de inmediato: no hay que
presionar nada más. El reporte final queda guardado en la carpeta
**`datos/salida`** con el nombre `reporte_matricula_<fecha>.xlsx`, organizado
por año (2025, 2026, ...).

> Con el archivo completo de matrícula (unas 60.000 filas), el procesamiento y
> la exportación tardan alrededor de un minuto. Durante ese tiempo la ventana
> puede verse "sin responder": es normal, solo espera a que termine.

Esta primera versión no muestra una vista previa editable antes de exportar
—va directo de elegir el archivo a entregarlo en Excel—. Si más adelante se
necesita volver a revisar y corregir antes de guardar, la arquitectura ya lo
soporta (ver `docs/manual_tecnico.md`).

## Preguntas frecuentes

**Sale un mensaje en rojo y no exportó nada.**
El archivo que elegiste no tiene la estructura esperada (le falta una columna) o
no es el correcto. El mensaje de error indica qué pasó; cierra el programa,
verifica el archivo y vuelve a intentarlo.

**Me equivoqué de archivo o quiero volver a procesar.**
Cierra la ventana (botón "Cerrar" al terminar, o "Cancelar" antes) y vuelve a
abrir el programa; te pedirá seleccionar el archivo de nuevo.

**¿Puedo cambiar la fecha del reporte?**
Sí, pero eso se hace desde la línea de comandos (`--fecha`). Pídele al área
técnica que te lo configure si lo necesitas seguido.

**El programa se ve distinto / no abre la ventana.**
Puede que Python no esté bien instalado en ese equipo. Consulta al área técnica y
al `manual_instalacion.md`.

## A quién acudir

Si algo no funciona y no está resuelto aquí, contacta al área técnica o a la
persona responsable del reporte en la Coordinación Financiera Virtual.

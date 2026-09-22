# Arquitectura

Este documento explica cómo está organizado el código, por qué, y cómo se
extiende. Los diagramas que lo acompañan están en `docs/diagramas/` en formato
PlantUML.

## Objetivo de diseño

El programa reemplaza una macro VBA, pero el proceso real del que forma parte es
más grande (conciliación de rectoría, recibos, fortalecimiento regional). Por eso
la arquitectura no se construyó como un script de un solo uso, sino como una base
que permite **agregar etapas nuevas sin reescribir las existentes** y **cambiar
la interfaz sin tocar las reglas de negocio**.

## Capas

El código está dividido en cuatro capas con dependencias en una sola dirección
(las de arriba dependen de las de abajo, nunca al revés):

```
Interfaz  ->  Etapas  ->  Núcleo  ->  Dominio
(presenta)   (casos)     (infra)     (reglas puras)
```

### Dominio (`dominio/`)

Las reglas de negocio del reporte, como **funciones puras**: reciben un
`DataFrame` y devuelven uno nuevo, sin leer ni escribir disco y sin estado.

- `columnas.py` — nombres de columna y constantes de negocio (reglas
  hardcodeadas, correcciones por año, etc.), confirmadas contra el VBA original.
- `matricula_base.py` — cada transformación del proceso (limpieza, SUMIF, cálculo
  de ingreso neto, deduplicación, segmentación por año) como una función
  independiente, más `procesar_matricula_base()` que las encadena en el orden
  exacto de la macro.

**Por qué puras:** son fáciles de probar de forma aislada (una entrada, una
salida esperada) y de recombinar. Toda la lógica delicada del reporte vive aquí,
protegida de los detalles de la interfaz o del manejo de archivos.

**Por qué por nombre de columna y no por letra:** la macro operaba por letras de
Excel (`AA`, `S`), que se rompen al cambiar el orden de las columnas. El dominio
referencia siempre encabezados, que son estables.

### Núcleo (`nucleo/`)

La infraestructura que conduce el proceso, sin ninguna regla de negocio.

- `etapa.py` — la clase abstracta `Etapa` (el contrato: un método `ejecutar`) y
  el `Contexto` compartido que viaja por todas las etapas y guarda las rutas de
  los archivos producidos.
- `resultado.py` — `ResultadoEtapa` y `TipoResultado`, que modelan de forma
  explícita los cuatro desenlaces de una etapa: continuar, pedir revisión,
  esperar un archivo, o error.
- `orquestador.py` — ejecuta la lista de etapas en orden y **se detiene en cada
  pausa** hasta que la interfaz confirma. No sabe cómo se muestran las cosas.
- `excel_io.py` — lectura y escritura de Excel, centralizada.

### Etapas (`etapas/`)

Cada bloque del proceso como una subclase de `Etapa`. Hoy existe
`EtapaMatriculaBase`, que envuelve el dominio: localiza el archivo de entrada,
llama a `procesar_matricula_base()`, guarda el resultado y devuelve un
`ResultadoEtapa` pidiendo revisión.

### Interfaz (`interfaz/` y `consola.py`)

Traduce los `ResultadoEtapa` a algo que el usuario ve, y recoge sus decisiones.
No contiene lógica de negocio.

- `ventana_principal.py` — la ventana de escritorio (Tkinter): barra de progreso,
  mensajes y la vista previa editable.
- `tabla_editable.py` — la rejilla con edición de celda por doble clic.
- `consola.py` — una interfaz de texto alternativa, útil para pruebas o entornos
  sin pantalla.

## El patrón de puntos de pausa

El requisito central del proceso es que **una persona revise cada archivo
intermedio y decida si continúa**. Esto se modela con `TipoResultado`:

- `CONTINUAR` — la etapa terminó, el orquestador avanza solo.
- `REVISION_USUARIO` — hay un archivo para revisar; el orquestador espera a que
  la interfaz llame a `confirmar_y_continuar()`.
- `ESPERAR_ARCHIVO` — se necesita un archivo nuevo antes de seguir.
- `ERROR` — el proceso se detiene y muestra el detalle.

El orquestador nunca avanza solo cuando hay una pausa: **el humano controla el
ritmo**. Ver el diagrama de estados (`05_estados_orquestador.puml`).

## Cómo agregar una etapa nueva

1. Crear una clase en `etapas/` que herede de `Etapa` e implemente `ejecutar`.
2. Poner su lógica de negocio como funciones puras en `dominio/`.
3. Si necesita el resultado de una etapa previa, tomarlo del `Contexto` con
   `contexto.obtener(clave)`.
4. Devolver el `ResultadoEtapa` adecuado (revisión, espera de archivo, etc.).
5. Agregar la etapa a la lista en `ventana_principal.py` y `consola.py`.
6. Escribir sus pruebas en `tests/`.

No hace falta modificar el orquestador ni las etapas existentes.

## Decisiones registradas

- **Tkinter y no una librería web/externa:** viene incluido con Python en
  Windows, así que no agrega dependencias ni complica el empaquetado ni choca con
  la restricción de ejecutables no verificados.
- **Vista previa limitada a 500 filas por hoja:** `Treeview` no rinde bien con
  decenas de miles de filas. Para revisar y corregir puntualmente es suficiente;
  si se necesitara editar más allá, se agregaría un buscador/filtro.
- **`src/` layout:** el código vive bajo `src/` para separar el paquete
  instalable de los archivos del repositorio (tests, docs, scripts), un estándar
  que evita imports accidentales.

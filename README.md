# Automatización del Reporte de Matrícula Financiera

Reemplaza la macro VBA de Excel que hoy genera el reporte diario de matrícula de
la Rectoría Virtual de UNIMINUTO, un proceso manual que toma entre 1 y 1.5 horas.
Este programa lo hace en segundos, es portable a cualquier computador con Python,
y ofrece una interfaz gráfica con vista previa editable para que la persona
revise y corrija los datos antes de dar por bueno el resultado.

> **Alcance de esta versión:** cubre el reemplazo completo de la macro (la
> generación del reporte de matrícula base por año). La arquitectura está
> preparada para agregar las etapas siguientes del proceso (rectoría, recibos,
> fortalecimiento regional) sin reescribir lo existente. Ver `docs/proceso.md`.

## Tabla de contenido

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Arquitectura](#arquitectura)
- [Pruebas](#pruebas)
- [Empaquetado como ejecutable](#empaquetado-como-ejecutable)
- [Documentación](#documentación)

## Requisitos

- **Python 3.11 o superior** (en Windows, descargar de [python.org](https://www.python.org/downloads/) marcando *"Add python.exe to PATH"*).
- Dependencias listadas en `requirements.txt` (`pandas`, `openpyxl`).
- `tkinter` para la interfaz gráfica: viene incluido con la instalación estándar de Python en Windows.

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

1. Descarga el archivo `Matricula_Financiera-Detalle...xlsx` y colócalo en `datos/entrada/`.
2. Ejecuta el programa (o haz doble clic en `scripts/ejecutar.bat` en Windows):

   ```bash
   python main.py
   ```

3. Se abre una ventana. Presiona **Iniciar**: el programa procesa el archivo y
   muestra una **vista previa editable** con una pestaña por año. Revisa los
   datos y **corrige celdas con doble clic** si hace falta.
4. Al presionar **Aprobar y continuar**, tus ediciones se guardan y el reporte
   final queda en `datos/salida/`.

Opciones de línea de comandos:

```bash
python main.py --datos RUTA      # usar otra carpeta de datos
python main.py --fecha 03.03.2026 # fijar la fecha del reporte
python main.py --consola          # interfaz de consola en vez de ventana
```

## Arquitectura

El proyecto separa la lógica de negocio, la orquestación y la interfaz, de modo
que se puedan agregar nuevas etapas o cambiar la interfaz sin tocar las reglas
del reporte.

```
reporte-matricula/
├── main.py                       Punto de entrada
├── src/reporte_matricula/
│   ├── consola.py                Interfaz de consola (alternativa)
│   ├── interfaz/                 Interfaz gráfica de escritorio (Tkinter)
│   │   ├── ventana_principal.py    Ventana con flujo por pasos y vista previa
│   │   └── tabla_editable.py       Tabla editable (doble clic para editar celda)
│   ├── nucleo/                   Infraestructura del proceso (sin reglas de negocio)
│   │   ├── etapa.py                Contrato base Etapa + Contexto compartido
│   │   ├── orquestador.py          Ejecuta las etapas y gestiona las pausas
│   │   ├── resultado.py            Tipos de resultado y puntos de pausa
│   │   └── excel_io.py             Lectura/escritura de Excel
│   ├── dominio/                  Reglas de negocio puras (sin efectos secundarios)
│   │   ├── columnas.py             Nombres de columna y reglas confirmadas del VBA
│   │   └── matricula_base.py       Transformaciones del proceso
│   └── etapas/                   Cada bloque del proceso como una Etapa
│       └── etapa1_matricula_base.py
├── tests/                        Pruebas automáticas
├── docs/                         Documentación y diagramas
├── datos/                        Carpetas de trabajo (entrada, salida, historico, temporal)
└── scripts/                      Utilidades .bat (ejecutar, construir .exe)
```

Detalle en [`docs/arquitectura.md`](docs/arquitectura.md). Diagramas en
[`docs/diagramas/`](docs/diagramas/) (formato PlantUML).

## Pruebas

```bash
pytest -q
```

Las pruebas verifican cada regla de negocio confirmada contra el VBA original
(cálculo de ingreso neto, filtros, ajustes puntuales, deduplicación por llave).

## Empaquetado como ejecutable

El objetivo final es distribuir un `.exe` que corra en cualquier computador de
la organización. Ese paso se hace **cuando el proceso completo esté validado y
el área de sistemas autorice ejecutar el `.exe`**. Mientras tanto, el programa
corre con Python instalado (que sí está permitido). Ver
[`docs/manual_instalacion.md`](docs/manual_instalacion.md).

## Documentación

| Documento | Contenido |
|-----------|-----------|
| [`docs/manual_usuario.md`](docs/manual_usuario.md) | Cómo usar el programa, paso a paso, para el equipo financiero. |
| [`docs/manual_instalacion.md`](docs/manual_instalacion.md) | Instalación, ejecución y empaquetado del `.exe`. |
| [`docs/manual_tecnico.md`](docs/manual_tecnico.md) | Cómo está construido y cómo extenderlo. |
| [`docs/arquitectura.md`](docs/arquitectura.md) | Decisiones de diseño y estructura del código. |
| [`docs/proceso.md`](docs/proceso.md) | El proceso de negocio que el programa automatiza. |
| [`CHANGELOG.md`](CHANGELOG.md) | Historial de versiones. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Cómo contribuir y estándares de código. |

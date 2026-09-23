# Historial de versiones

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/) y el
proyecto usa [versionado semántico](https://semver.org/lang/es/).

## [1.0.0] — 2026-09-22

Primera versión funcional: reemplazo completo de la macro VBA de matrícula base.

### Agregado
- Procesamiento de la matrícula base equivalente a la macro `MetodoAbrirLibro`,
  más la deduplicación por llave de 4 campos del proceso manual.
- Interfaz gráfica de escritorio (Tkinter) con flujo por pasos, barra de progreso
  y vista previa editable (una pestaña por año, edición de celda por doble clic).
- Interfaz de consola alternativa (`--consola`).
- Arquitectura por capas (dominio / núcleo / etapas / interfaz) con orquestador y
  puntos de pausa explícitos, preparada para agregar etapas nuevas.
- 12 pruebas automáticas de las reglas de negocio.
- Documentación: README, manuales de usuario/instalación/técnico, arquitectura,
  proceso, y diagramas PlantUML (flujo, componentes, clases, secuencia, estados).
- Scripts de Windows para ejecutar (`ejecutar.bat`) y empaquetar (`construir_exe.bat`).
- Integración continua con GitHub Actions.

### Validado
- Salida idéntica a la de la macro para el archivo de prueba (62.787 registros en
  las hojas 2025 y 2026); cálculo de ingreso neto validado con caso real.

## [No liberado]

### Cambiado
- La ventana gráfica y la consola ahora abren un cuadro de selección de
  archivo (`filedialog`) para elegir el Excel de matrícula desde cualquier
  carpeta, en vez de exigir que se copie primero a `datos/entrada`. La
  búsqueda automática por carpeta se mantiene como respaldo.

### Pendiente
- Etapas de conciliación de rectoría, recibos y fortalecimiento regional.
- Empaquetado y autorización del `.exe` para equipos de la organización.
- Buscador/filtro en la vista previa para archivos con muchas filas.

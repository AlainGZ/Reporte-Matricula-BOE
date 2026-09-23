# Manual de instalación y despliegue

Dirigido a quien instala y mantiene el programa en los equipos de la
organización.

## 1. Requisitos

- **Windows** (el destino de la organización) o cualquier sistema con Python.
- **Python 3.11 o superior.**
- Conexión a internet la primera vez, para instalar dependencias.

## 2. Instalar Python

1. Descarga Python desde <https://www.python.org/downloads/>.
2. En el instalador, **marca la casilla "Add python.exe to PATH"** antes de
   instalar. Sin esto, los comandos no funcionan.
3. Verifica en una terminal (CMD o PowerShell):

   ```bat
   python --version
   ```

   Debe mostrar `Python 3.11.x` o superior.

> El instalador oficial de python.org está firmado y suele estar permitido por la
> política de seguridad de la organización, a diferencia de un `.exe` sin firmar.
> Si aun así está bloqueado, coordina con el área de sistemas.

## 3. Instalar el programa

1. Copia la carpeta del proyecto al equipo (por ejemplo dentro de OneDrive, para
   que esté disponible en cualquier equipo donde inicie sesión el usuario).
2. Abre una terminal en la carpeta del proyecto e instala las dependencias:

   ```bat
   pip install -r requirements.txt
   ```

## 4. Ejecutar

- **Forma fácil:** doble clic en `scripts\ejecutar.bat`.
- **Desde la terminal:**

  ```bat
  python main.py
  ```

Un archivo `.bat` es texto interpretado por `cmd.exe` (ya permitido en el
sistema), así que **no dispara la restricción de ejecutables no verificados**.

## 5. Estructura de carpetas de datos

El programa crea estas subcarpetas dentro de `datos/`:

| Carpeta | Para qué |
|---------|----------|
| `entrada` | Ya no es obligatoria para el uso diario: el archivo se elige con el cuadro de selección de Windows, esté donde esté. Se mantiene por compatibilidad (uso desde consola sin diálogo). |
| `salida` | Aquí queda el reporte generado. |
| `historico` | Reservada para etapas futuras. |
| `temporal` | Archivos intermedios de trabajo. |

## 6. Empaquetar como ejecutable (.exe) — paso final

> **Hacer esto solo cuando el proceso esté validado y el área de sistemas
> autorice ejecutar el `.exe` en los equipos.** Un `.exe` generado con
> PyInstaller no está firmado y será bloqueado por políticas que restrinjan
> ejecutables no verificados, hasta que se autorice explícitamente.

1. Instala las dependencias de desarrollo:

   ```bat
   pip install -r requirements-dev.txt
   ```

2. Ejecuta el script de construcción:

   ```bat
   scripts\construir_exe.bat
   ```

3. El ejecutable queda en `dist\ReporteMatricula.exe`. Ese único archivo trae
   Python y las librerías incluidas; se puede copiar a cualquier equipo Windows.

### Autorización del ejecutable

Para que el `.exe` corra en equipos con restricción, coordina con el área de
sistemas una de estas opciones:

- **Firma de código:** firmar el `.exe` con un certificado de la organización.
- **Lista de permitidos (allowlisting):** agregar el hash o la ruta del `.exe` a
  la política (AppLocker / Windows Defender Application Control).

Mientras tanto, el uso con Python instalado y `ejecutar.bat` es la vía válida.

## 7. Solución de problemas

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| `'python' no se reconoce...` | Python no está en el PATH. | Reinstalar marcando "Add to PATH". |
| `ModuleNotFoundError: pandas` | Faltan dependencias. | `pip install -r requirements.txt`. |
| La ventana no abre, error de `tkinter` | Instalación de Python sin Tcl/Tk. | Reinstalar Python (opción por defecto incluye Tkinter). |
| El `.bat` también está bloqueado | Política restringe scripts. | Ejecutar `python main.py` directo, o coordinar con sistemas. |

# Manual técnico

Dirigido a desarrolladores que mantienen o extienden el programa. Complementa a
`arquitectura.md` (el porqué del diseño) con el cómo operativo.

## Preparar el entorno de desarrollo

```bash
git clone <url-del-repositorio>
cd reporte-matricula
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/Mac: source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Ejecutar

```bash
python main.py            # interfaz gráfica
python main.py --consola  # interfaz de consola
pytest -q                 # pruebas
```

`main.py` agrega `src/` al `sys.path`, así que no hace falta instalar el paquete
para ejecutarlo. Con `pyproject.toml` también se puede `pip install -e .`.

## Mapa de módulos

| Módulo | Responsabilidad |
|--------|-----------------|
| `dominio/columnas.py` | Constantes: nombres de columna y reglas de negocio del VBA. |
| `dominio/matricula_base.py` | Transformaciones puras del reporte. |
| `nucleo/etapa.py` | Contrato `Etapa` y `Contexto` compartido. |
| `nucleo/resultado.py` | `ResultadoEtapa` y `TipoResultado` (puntos de pausa). |
| `nucleo/orquestador.py` | Ejecuta etapas y gestiona pausas. |
| `nucleo/excel_io.py` | Lectura/escritura de Excel. |
| `etapas/etapa1_matricula_base.py` | La etapa que envuelve el dominio. |
| `interfaz/ventana_principal.py` | Ventana Tkinter con vista previa. |
| `interfaz/tabla_editable.py` | Rejilla editable por doble clic. |
| `consola.py` | Interfaz de texto alternativa. |

## Cómo agregar una etapa nueva (receta)

Ejemplo: agregar la etapa de conciliación de rectoría.

1. **Dominio.** Crear `dominio/rectoria.py` con funciones puras
   (`DataFrame -> DataFrame`) para cada transformación, y sus constantes en un
   módulo de columnas si aplica.

2. **Etapa.** Crear `etapas/etapa2_rectoria.py`:

   ```python
   from ..nucleo.etapa import Etapa, Contexto
   from ..nucleo.resultado import ResultadoEtapa
   from ..etapas.etapa1_matricula_base import ARTEFACTO_MATRICULA_BASE

   class EtapaRectoria(Etapa):
       nombre = "rectoria"
       descripcion = "Consolida la matrícula en el detalle de rectoría."

       def ejecutar(self, contexto: Contexto) -> ResultadoEtapa:
           base = contexto.obtener(ARTEFACTO_MATRICULA_BASE)  # salida de la etapa 1
           # ... lógica; puede devolver esperar_archivo() para pedir un Excel nuevo
           return ResultadoEtapa.revision("Rectoría consolidada.", archivo=ruta)
   ```

3. **Registrar la etapa** en la lista de `ventana_principal.py` y `consola.py`:

   ```python
   etapas = [EtapaMatriculaBase(), EtapaRectoria()]
   ```

4. **Pruebas.** Agregar `tests/test_rectoria.py` con casos por cada función pura.

No se modifica el orquestador ni las etapas anteriores.

## Comunicación entre etapas

Una etapa deja su salida en el `Contexto` con `contexto.registrar(clave, ruta)`,
y la siguiente la toma con `contexto.obtener(clave)`. Las claves son constantes
exportadas por cada etapa (por ejemplo `ARTEFACTO_MATRICULA_BASE`).

## Puntos de pausa

Para pedir revisión: `ResultadoEtapa.revision(mensaje, archivo=ruta)`.
Para pedir un archivo nuevo: `ResultadoEtapa.esperar_archivo(mensaje, requerido)`
con un `ArchivoRequerido(nombre_sugerido, instrucciones)`.
La interfaz ya sabe reaccionar a cada tipo; no hay que tocarla salvo para
registrar la etapa.

## Convenciones de código

- Nombres en español (dominio del negocio en español), `snake_case` para
  funciones y variables, `PascalCase` para clases.
- Type hints en las firmas públicas.
- Las funciones de dominio son puras: no leen ni escriben disco, no mutan su
  entrada (usar `df.copy()`).
- Docstrings que expliquen el *porqué* y su equivalencia con el VBA cuando aplique.

## Pruebas

- Framework: `pytest`. Configuración en `pyproject.toml`
  (`pythonpath = ["src"]`, `testpaths = ["tests"]`).
- Cada regla de negocio tiene al menos una prueba con datos controlados.
- Al agregar o cambiar una regla, agregar/actualizar su prueba.
- CI: `.github/workflows/ci.yml` corre `pytest` en Python 3.11 y 3.12 en cada
  push y pull request.

## Depuración de datos reales

Para procesar un archivo real sin la interfaz:

```python
from reporte_matricula.dominio.matricula_base import procesar_matricula_base
hojas = procesar_matricula_base("ruta/al/archivo.xlsx")
print({anio: len(df) for anio, df in hojas.items()})
```

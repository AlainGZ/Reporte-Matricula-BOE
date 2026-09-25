"""Etapa 1 — Procesamiento de la matrícula base (reemplazo de la macro).

Toma el archivo Matricula_Financiera-Detalle, aplica toda la lógica validada
(equivalente a la macro original más la deduplicación por llave) y produce el
Excel segmentado por año. Al terminar pide revisión del usuario, porque este
archivo es la base de todo lo que sigue.
"""

from __future__ import annotations
from pathlib import Path

from ..nucleo.etapa import Etapa, Contexto
from ..nucleo.resultado import ResultadoEtapa
from ..nucleo import excel_io
from ..dominio import matricula_base

#: Clave con la que esta etapa registra su salida en el contexto, para que las
#: etapas siguientes (rectoría, etc.) la consuman.
ARTEFACTO_MATRICULA_BASE = "matricula_base_procesada"


class EtapaMatriculaBase(Etapa):
    nombre = "matricula-base"
    descripcion = "Procesa el detalle de matrícula y genera el reporte por año."

    #: Prefijo del nombre del archivo de entrada que se busca en la carpeta.
    prefijo_archivo_entrada = "Matricula_Financiera-Detalle"

    def ejecutar(self, contexto: Contexto) -> ResultadoEtapa:
        ruta_entrada = self._localizar_entrada(contexto)
        if ruta_entrada is None:
            return ResultadoEtapa.error(
                "No se encontró el archivo de matrícula.",
                detalle=(
                    f"Se buscó un archivo que empiece por '{self.prefijo_archivo_entrada}' "
                    f"en la carpeta de entrada: {contexto.carpeta_entrada}"
                ),
            )

        try:
            hojas = matricula_base.procesar_matricula_base(ruta_entrada)
        except KeyError as error:
            return ResultadoEtapa.error(
                "El archivo no tiene la estructura esperada (falta una columna).",
                detalle=str(error),
            )
        except ValueError as error:
            return ResultadoEtapa.error(
                "El archivo no pudo procesarse por un problema en los datos.",
                detalle=str(error),
            )

        if not hojas:
            return ResultadoEtapa.error(
                "El procesamiento no produjo ninguna fila.",
                detalle="Revisa que la hoja 'Detalle Estudiantes' tenga datos.",
            )

        ruta_salida = contexto.carpeta_salida / f"reporte_matricula_{contexto.fecha_reporte}.xlsx"
        excel_io.guardar_hojas(hojas, ruta_salida)
        contexto.registrar(ARTEFACTO_MATRICULA_BASE, ruta_salida)

        total = excel_io.contar_filas(hojas)
        # Primera versión: sin pausa de revisión. Procesa y exporta directo.
        # Si en el futuro se necesita volver a pedir revisión antes de exportar,
        # basta cambiar `continuar` por `revision` aquí; el resto de la ventana
        # ya sabe reaccionar a ambos casos.
        return ResultadoEtapa.continuar(
            mensaje=(
                f"Matrícula procesada y exportada: {total} registros en {len(hojas)} "
                f"hojas por año."
            ),
            archivo=ruta_salida,
            total_registros=total,
            total_hojas=len(hojas),
        )

    def _localizar_entrada(self, contexto: Contexto) -> Path | None:
        """Devuelve el archivo a procesar.

        Prioridad:
        1. `contexto.archivo_seleccionado`: la ruta que el usuario eligió con el
           cuadro de selección de archivo (puede estar en cualquier carpeta).
        2. Búsqueda automática en `carpeta_entrada` por prefijo de nombre, que se
           mantiene como respaldo para la interfaz de consola o uso sin diálogo.
        """
        if contexto.archivo_seleccionado is not None and contexto.archivo_seleccionado.exists():
            return contexto.archivo_seleccionado

        if not contexto.carpeta_entrada.exists():
            return None
        for patron in (f"{self.prefijo_archivo_entrada}*.xlsx", f"{self.prefijo_archivo_entrada}*.xls"):
            coincidencias = sorted(contexto.carpeta_entrada.glob(patron))
            if coincidencias:
                return coincidencias[0]
        return None

"""Orquestador del proceso: ejecuta las etapas en orden, deteniéndose en cada
punto de pausa hasta que el usuario aprueba o entrega lo que se necesita.

Está diseñado para ser manejado desde cualquier interfaz (consola o gráfica):
la interfaz llama a `avanzar()` y reacciona al `ResultadoEtapa` que recibe, sin
que el orquestador sepa cómo se muestran las cosas.
"""

from __future__ import annotations
from dataclasses import dataclass

from .etapa import Etapa, Contexto
from .resultado import ResultadoEtapa, TipoResultado


@dataclass
class EstadoProceso:
    """Posición actual dentro de la secuencia de etapas."""

    indice_actual: int = 0
    terminado: bool = False


class Orquestador:
    """Conduce la ejecución de una lista ordenada de etapas."""

    def __init__(self, etapas: list[Etapa], contexto: Contexto) -> None:
        if not etapas:
            raise ValueError("El orquestador necesita al menos una etapa.")
        self._etapas = etapas
        self._contexto = contexto
        self._estado = EstadoProceso()

    @property
    def etapa_actual(self) -> Etapa | None:
        if self._estado.terminado or self._estado.indice_actual >= len(self._etapas):
            return None
        return self._etapas[self._estado.indice_actual]

    @property
    def progreso(self) -> tuple[int, int]:
        """Devuelve (etapa_actual_1indexada, total) para mostrar 'Paso 2 de 5'."""
        return (min(self._estado.indice_actual + 1, len(self._etapas)), len(self._etapas))

    def avanzar(self) -> ResultadoEtapa:
        """Ejecuta la etapa actual y devuelve su resultado.

        No pasa automáticamente a la siguiente cuando hay una pausa: es la
        interfaz quien llama a `confirmar_y_continuar()` cuando el usuario está
        listo. Así el humano controla el ritmo.
        """
        etapa = self.etapa_actual
        if etapa is None:
            return ResultadoEtapa.continuar("El proceso ya terminó.")

        try:
            resultado = etapa.ejecutar(self._contexto)
        except Exception as excepcion:  # frontera: convertir un bug en error visible.
            return ResultadoEtapa.error(
                f"Error inesperado en la etapa '{etapa.nombre}'.",
                detalle=f"{type(excepcion).__name__}: {excepcion}",
            )

        # Una etapa que puede continuar sin intervención avanza el índice sola.
        if resultado.tipo is TipoResultado.CONTINUAR:
            self._marcar_completada()

        return resultado

    def confirmar_y_continuar(self) -> None:
        """La interfaz llama a esto cuando el usuario aprueba una revisión o ya
        entregó el archivo requerido; avanza a la siguiente etapa."""
        self._marcar_completada()

    def _marcar_completada(self) -> None:
        self._estado.indice_actual += 1
        if self._estado.indice_actual >= len(self._etapas):
            self._estado.terminado = True

    @property
    def contexto(self) -> Contexto:
        return self._contexto

    @property
    def terminado(self) -> bool:
        return self._estado.terminado

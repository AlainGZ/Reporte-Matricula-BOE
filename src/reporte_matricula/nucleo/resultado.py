"""Tipos que describen el resultado de ejecutar una etapa del proceso.

El proceso completo se detiene en varios puntos: unos porque el usuario debe
revisar un Excel intermedio y decidir si continúa, y otros porque debe traer un
archivo nuevo (una descarga externa). Estos tipos modelan esos puntos de pausa
de forma explícita, para que la interfaz sepa qué mostrar y qué esperar.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path


class TipoResultado(Enum):
    """Qué debe pasar después de que una etapa termina de ejecutarse."""

    CONTINUAR = auto()          # Terminó; se puede pasar a la siguiente sin intervención.
    REVISION_USUARIO = auto()   # Hay un archivo intermedio que el usuario debe revisar y aprobar.
    ESPERAR_ARCHIVO = auto()    # El usuario debe traer un archivo nuevo para continuar.
    ERROR = auto()              # La etapa falló; el proceso no puede continuar.


@dataclass
class ArchivoRequerido:
    """Describe un archivo que el usuario debe proporcionar para continuar."""

    nombre_sugerido: str            # Ej. "FACTURAS.xlsx"
    instrucciones: str              # Qué es y de dónde sale.
    datos_para_consultar: list[str] = field(default_factory=list)  # Ej. facturas a buscar.


@dataclass
class ResultadoEtapa:
    """Lo que devuelve toda etapa al terminar.

    `tipo` decide el flujo; los demás campos aportan el detalle que la interfaz
    necesita para mostrar la vista previa, el mensaje o el error.
    """

    tipo: TipoResultado
    mensaje: str = ""
    archivo_generado: Path | None = None          # Excel intermedio para vista previa/revisión.
    archivo_requerido: ArchivoRequerido | None = None
    detalle_error: str = ""
    metricas: dict[str, int] = field(default_factory=dict)  # Ej. {"filas": 62787}

    @classmethod
    def continuar(cls, mensaje: str, archivo: Path | None = None, **metricas: int) -> "ResultadoEtapa":
        return cls(TipoResultado.CONTINUAR, mensaje=mensaje, archivo_generado=archivo, metricas=metricas)

    @classmethod
    def revision(cls, mensaje: str, archivo: Path, **metricas: int) -> "ResultadoEtapa":
        return cls(TipoResultado.REVISION_USUARIO, mensaje=mensaje, archivo_generado=archivo, metricas=metricas)

    @classmethod
    def esperar_archivo(cls, mensaje: str, requerido: ArchivoRequerido) -> "ResultadoEtapa":
        return cls(TipoResultado.ESPERAR_ARCHIVO, mensaje=mensaje, archivo_requerido=requerido)

    @classmethod
    def error(cls, mensaje: str, detalle: str = "") -> "ResultadoEtapa":
        return cls(TipoResultado.ERROR, mensaje=mensaje, detalle_error=detalle)

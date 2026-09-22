"""Contrato base para toda etapa del proceso.

Cada bloque del proceso (matrícula base y, en el futuro, rectoría, recibos,
fortalecimiento regional) se implementa como una subclase de `Etapa`. El
orquestador las ejecuta en orden pasando un `Contexto` compartido que acumula
las rutas de los archivos que cada etapa produce y las siguientes consumen.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

from .resultado import ResultadoEtapa


@dataclass
class Contexto:
    """Estado compartido que viaja por todas las etapas.

    Guarda las carpetas de trabajo y un registro de los archivos producidos,
    para que una etapa posterior pueda tomar la salida de una anterior sin que
    el orquestador tenga que cablear rutas a mano.
    """

    carpeta_entrada: Path
    carpeta_salida: Path
    carpeta_historico: Path
    carpeta_temporal: Path
    fecha_reporte: str  # formato dd.mm.aaaa; sufijo de los archivos del día.
    artefactos: dict[str, Path] = field(default_factory=dict)

    def registrar(self, clave: str, ruta: Path) -> None:
        """Guarda la ruta de un archivo producido, identificado por una clave estable."""
        self.artefactos[clave] = ruta

    def obtener(self, clave: str) -> Path:
        """Recupera la ruta de un artefacto previo; falla explícito si no existe."""
        if clave not in self.artefactos:
            raise KeyError(
                f"La etapa requiere el artefacto '{clave}', que ninguna etapa previa "
                f"registró. Artefactos disponibles: {sorted(self.artefactos)}"
            )
        return self.artefactos[clave]


class Etapa(ABC):
    """Una unidad del proceso. Las subclases implementan solo `ejecutar`."""

    #: Nombre corto y estable de la etapa, usado en logs y en la interfaz.
    nombre: str = "etapa-sin-nombre"

    #: Descripción de una línea de lo que hace, para mostrar al usuario.
    descripcion: str = ""

    @abstractmethod
    def ejecutar(self, contexto: Contexto) -> ResultadoEtapa:
        """Ejecuta la lógica de la etapa y devuelve qué debe pasar después.

        No debe lanzar excepciones para errores esperables (archivo faltante,
        columna ausente): esos se devuelven como `ResultadoEtapa.error(...)` para
        que la interfaz los muestre con claridad. Solo deja propagar fallos
        realmente inesperados (bugs), que el orquestador captura como frontera.
        """
        raise NotImplementedError

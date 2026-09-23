"""Pruebas de cómo la Etapa 1 localiza el archivo de entrada.

Cubre la prioridad introducida para el selector de archivo: si el usuario
elige un archivo con el cuadro de diálogo (`contexto.archivo_seleccionado`),
ese archivo se usa sin importar la carpeta de entrada; si no eligió ninguno,
se mantiene la búsqueda automática por prefijo en `carpeta_entrada` (usada por
la consola sin diálogo).
"""

from __future__ import annotations
from pathlib import Path

from reporte_matricula.etapas.etapa1_matricula_base import EtapaMatriculaBase
from reporte_matricula.nucleo.etapa import Contexto


def _contexto(tmp_path: Path, archivo_seleccionado: Path | None = None) -> Contexto:
    return Contexto(
        carpeta_entrada=tmp_path / "entrada",
        carpeta_salida=tmp_path / "salida",
        carpeta_historico=tmp_path / "historico",
        carpeta_temporal=tmp_path / "temporal",
        fecha_reporte="01.01.2026",
        archivo_seleccionado=archivo_seleccionado,
    )


def test_prioriza_archivo_seleccionado_sobre_carpeta_entrada(tmp_path):
    carpeta_entrada = tmp_path / "entrada"
    carpeta_entrada.mkdir()
    archivo_en_carpeta = carpeta_entrada / "Matricula_Financiera-Detalle_viejo.xlsx"
    archivo_en_carpeta.touch()

    archivo_elegido = tmp_path / "cualquier_otra_carpeta" / "descarga.xlsx"
    archivo_elegido.parent.mkdir()
    archivo_elegido.touch()

    contexto = _contexto(tmp_path, archivo_seleccionado=archivo_elegido)
    ruta = EtapaMatriculaBase()._localizar_entrada(contexto)

    assert ruta == archivo_elegido


def test_ignora_archivo_seleccionado_inexistente_y_usa_carpeta_entrada(tmp_path):
    carpeta_entrada = tmp_path / "entrada"
    carpeta_entrada.mkdir()
    archivo_en_carpeta = carpeta_entrada / "Matricula_Financiera-Detalle_actual.xlsx"
    archivo_en_carpeta.touch()

    contexto = _contexto(tmp_path, archivo_seleccionado=tmp_path / "no_existe.xlsx")
    ruta = EtapaMatriculaBase()._localizar_entrada(contexto)

    assert ruta == archivo_en_carpeta


def test_sin_seleccion_ni_carpeta_devuelve_none(tmp_path):
    contexto = _contexto(tmp_path)
    ruta = EtapaMatriculaBase()._localizar_entrada(contexto)

    assert ruta is None

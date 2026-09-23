"""Interfaz de consola del proceso (alternativa a la ventana gráfica).

Traduce los `ResultadoEtapa` del orquestador en mensajes de texto y recoge la
confirmación del usuario en cada pausa. Útil para automatización, pruebas o
equipos sin entorno gráfico. No contiene lógica de negocio.
"""

from __future__ import annotations
from datetime import date
from pathlib import Path

from .nucleo.etapa import Contexto
from .nucleo.orquestador import Orquestador
from .nucleo.resultado import ResultadoEtapa, TipoResultado
from .etapas.etapa1_matricula_base import EtapaMatriculaBase


def _linea(caracter: str = "=", ancho: int = 60) -> str:
    return caracter * ancho


def construir_contexto(carpeta_datos: Path, fecha_reporte: str | None = None) -> Contexto:
    """Arma el contexto con las subcarpetas estándar dentro de `carpeta_datos`."""
    fecha = fecha_reporte or date.today().strftime("%d.%m.%Y")
    contexto = Contexto(
        carpeta_entrada=carpeta_datos / "entrada",
        carpeta_salida=carpeta_datos / "salida",
        carpeta_historico=carpeta_datos / "historico",
        carpeta_temporal=carpeta_datos / "temporal",
        fecha_reporte=fecha,
    )
    for carpeta in (contexto.carpeta_entrada, contexto.carpeta_salida,
                    contexto.carpeta_historico, contexto.carpeta_temporal):
        carpeta.mkdir(parents=True, exist_ok=True)
    return contexto


def _mostrar_resultado(resultado: ResultadoEtapa, progreso: tuple[int, int]) -> None:
    actual, total = progreso
    print(f"\n[Paso {actual} de {total}]  {resultado.mensaje}")
    for clave, valor in resultado.metricas.items():
        print(f"    - {clave.replace('_', ' ')}: {valor}")
    if resultado.archivo_generado:
        print(f"    Archivo generado: {resultado.archivo_generado}")


def _pausar_para_revision() -> bool:
    print("\n    >> Revisa el archivo indicado arriba.")
    print("       Si algo está mal, ciérralo, corrígelo y guárdalo en el mismo lugar.")
    respuesta = input("    ¿Continuar con el siguiente paso? (s/n): ").strip().lower()
    return respuesta in ("s", "si", "sí", "y", "yes")


def _pausar_para_archivo(resultado: ResultadoEtapa) -> None:
    requerido = resultado.archivo_requerido
    print(f"\n    >> Se necesita el archivo: {requerido.nombre_sugerido}")
    print(f"       {requerido.instrucciones}")
    input("    Cuando el archivo esté en la carpeta de entrada, presiona Enter para continuar...")


def _pedir_ruta_archivo() -> Path:
    """Pide al usuario la ruta del Excel de matrícula, esté donde esté."""
    while True:
        ruta_texto = input(
            "\nRuta completa del archivo de matrícula (o arrástralo a esta ventana): "
        ).strip().strip('"')
        ruta = Path(ruta_texto)
        if ruta.is_file():
            return ruta
        print(f"    No se encontró un archivo en: {ruta}. Intenta de nuevo.")


def ejecutar_proceso(carpeta_datos: Path, fecha_reporte: str | None = None) -> None:
    """Bucle principal: ejecuta cada etapa y gestiona sus pausas."""
    print(_linea())
    print("  AUTOMATIZACIÓN DEL REPORTE DE MATRÍCULA FINANCIERA")
    print(_linea())

    contexto = construir_contexto(carpeta_datos, fecha_reporte)
    contexto.archivo_seleccionado = _pedir_ruta_archivo()
    etapas = [EtapaMatriculaBase()]
    orquestador = Orquestador(etapas, contexto)

    while not orquestador.terminado:
        progreso = orquestador.progreso
        resultado = orquestador.avanzar()
        _mostrar_resultado(resultado, progreso)

        if resultado.tipo is TipoResultado.ERROR:
            print(f"\n    ERROR: {resultado.detalle_error}")
            print("    El proceso se detuvo. Corrige el problema y vuelve a ejecutar.")
            return

        if resultado.tipo is TipoResultado.REVISION_USUARIO:
            if _pausar_para_revision():
                orquestador.confirmar_y_continuar()
            else:
                print("\n    Proceso cancelado por el usuario.")
                return

        elif resultado.tipo is TipoResultado.ESPERAR_ARCHIVO:
            _pausar_para_archivo(resultado)
            orquestador.confirmar_y_continuar()

    print(f"\n{_linea()}")
    print("  PROCESO COMPLETADO")
    print(f"  Archivos finales en: {contexto.carpeta_salida}")
    print(_linea())

"""Punto de entrada del programa de automatización del reporte de matrícula.

Ejecución:
    python main.py                      # abre la ventana; usa la carpeta 'datos/'
    python main.py --datos RUTA         # usa otra carpeta de datos
    python main.py --fecha 03.03.2026   # fija la fecha del reporte (por defecto, hoy)
    python main.py --consola            # usa la interfaz de consola

Coloca el archivo descargado (Matricula_Financiera-Detalle...) dentro de la
subcarpeta 'entrada' de la carpeta de datos antes de ejecutar.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

# Permite ejecutar con 'python main.py' sin instalar el paquete: agrega src/ al path.
sys.path.insert(0, str(Path(__file__).parent / "src"))


def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automatiza el reporte de matrícula financiera de Uniminuto."
    )
    parser.add_argument(
        "--datos", type=Path, default=Path(__file__).parent / "datos",
        help="Carpeta de datos (contiene entrada/, salida/, historico/, temporal/).",
    )
    parser.add_argument(
        "--fecha", type=str, default=None,
        help="Fecha del reporte en formato dd.mm.aaaa. Por defecto, la fecha de hoy.",
    )
    parser.add_argument(
        "--consola", action="store_true",
        help="Usar la interfaz de consola en vez de la ventana gráfica.",
    )
    return parser.parse_args()


def main() -> None:
    args = parsear_argumentos()

    if args.consola:
        from reporte_matricula.consola import ejecutar_proceso
        try:
            ejecutar_proceso(args.datos, args.fecha)
        except KeyboardInterrupt:
            print("\n\nProceso interrumpido por el usuario.")
        finally:
            input("\nPresiona Enter para salir...")
    else:
        from reporte_matricula.interfaz.ventana_principal import iniciar_aplicacion
        iniciar_aplicacion(args.datos, args.fecha)


if __name__ == "__main__":
    main()

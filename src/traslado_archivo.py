from pathlib import Path
import logging


def movimiento_archivos(ruta_archivo_origen: Path, ruta_destino_carpeta: Path):
    ruta_archivo_destino = ruta_destino_carpeta / ruta_archivo_origen.name

    logging.info(f"pasar archivo de {ruta_archivo_origen} a {ruta_archivo_destino}")

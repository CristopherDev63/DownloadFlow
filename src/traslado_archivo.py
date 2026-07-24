from pathlib import Path
import logging


def movimiento_archivos(ruta_archivo_origen: Path, ruta_destino_carpeta: Path):
    """ Función que se didica mover archivos de punto A y B
    Args:
        - ruta_archivo_origen(Path): Ruta del origen del archivo.
        - ruta_desttino_carpeta(Path): Ruta de destino del archivo.
    """
    ruta_archivo_destino = ruta_destino_carpeta / ruta_archivo_origen.name

    logging.info(f"pasar archivo de {ruta_archivo_origen} a {ruta_archivo_destino}")

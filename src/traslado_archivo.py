from pathlib import Path
import logging
import shutil


RUTA_BASE = Path.home()


def renombramiento_archivo_duplicado(ruta_archivo_origen: Path, ruta_destino_carpeta: Path):
    """ Se encarga de modificar el nombre del archivo a un uno de duplicado para evitar conflictos. 
    Args:
        - ruta_archivo_origen(Path): La ruta de donde vamos a modificar el nombre.
        - ruta_destino_carpeta(Path): A donde va a para nuestro archivo con diferente nombre.
    """
    nombre_archivo = ruta_archivo_origen.stem
    extension_archivo = ruta_archivo_origen.suffix

    contador_archivos = 1
    ruta_archivo_nueva = ruta_destino_carpeta / f"{nombre_archivo}_copia_{contador_archivos}{extension_archivo}"

    while ruta_archivo_nueva.exists():
        contador_archivos += 1
        ruta_archivo_nueva = ruta_destino_carpeta / f"{nombre_archivo}_copia_{contador_archivos}{extension_archivo}"

    return ruta_archivo_nueva
    


def movimiento_archivos(ruta_archivo_origen: Path, ruta_destino_carpeta: Path) -> None:
    """ Función que se didica mover archivos de punto A y B.
    Args:
        - ruta_archivo_origen(Path): Ruta del origen del archivo.
        - ruta_desttino_carpeta(Path): Ruta base que se usara para hacer la ruta de destino del archivo.
    """
    ruta_archivo_origen = Path(ruta_archivo_origen)
    ruta_destino_carpeta = Path(ruta_destino_carpeta)

    ruta_archivo_destino = ruta_destino_carpeta / ruta_archivo_origen.name

    if not ruta_archivo_destino.exists():
        shutil.move(ruta_archivo_origen, ruta_archivo_destino)
        logging.info(f"Archivo [{ruta_archivo_origen.name}] movido de [{ruta_archivo_origen.relative_to(RUTA_BASE)}] a [{ruta_archivo_destino.relative_to(RUTA_BASE)}]")
        return 

    # En caso de que exista el archivo de destino.
    logging.warning(f"Archivo [{ruta_archivo_origen.name}] con mismo nombre en [{ruta_destino_carpeta.relative_to(RUTA_BASE)}]")
    ruta_archivo_destino = renombramiento_archivo_duplicado(ruta_archivo_origen, ruta_destino_carpeta)
    shutil.move(ruta_archivo_origen, ruta_archivo_destino)
    logging.info(f"Archivo [{ruta_archivo_origen.name}] movido y renombrado con [{ruta_archivo_origen.relative_to(RUTA_BASE)}] a [{ruta_archivo_destino.relative_to(RUTA_BASE)}] como nuevo nombre")

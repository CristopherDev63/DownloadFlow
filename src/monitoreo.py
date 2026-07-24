from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from typing import Callable
from pathlib import Path
import logging 


class Monitoreo(PatternMatchingEventHandler):
    """ Clase monitoreo en tiempo real """
    def __init__(self, extensiones: list[str], ruta_base: Path, movimiento_archivo: Callable[[Path], None], ruta_origen_carpeta: Path, ruta_destino_carpeta: Path) -> None:
        """ Dentro de este constructor definimos los filtros del monitoreo.
        Args:
            - extensiones(list(str)): Una lista de extensiones a darle monitoreo.
            - ruta_proyecto(Path): La ruta base del proyecto.
            - movimiento_archivo(Callable): Función encargada de mover los archivos.
        """
        self.ruta_base = ruta_base
        self.movimiento_archivo = movimiento_archivo
        self.ruta_origen_carpeta = ruta_origen_carpeta
        self.ruta_destino_carpeta = ruta_destino_carpeta

        super().__init__(
                patterns=extensiones,
                ignore_directories=True,
                case_sensitive=False
        )


    def _acortador_ruta(self, ruta: Path) -> Path | None:
        """ Función que acorta rutas.
        Args:
            - ruta(Path): La ruta a acortar.
        """
        try:
            ruta = Path(ruta)
            return ruta.relative_to(self.ruta_base)
        except ValueError as e:
            logging.error(f"Problema al a cortar la ruta {e}")

        

    def on_created(self, event) -> None:
        """ Cuando se crean nuevos archivos se encarga de manejar sus eventos """
        ruta_origen_archivo = self._acortador_ruta(event.src_path)
        
        logging.debug(f"Detección de archivo nuevo [{ruta_origen_archivo}]")
        self.movimiento_archivo(event.src_path, self.ruta_destino_carpeta)


def creacion_monitorizacion(extensiones: list[str], ruta_proyecto: Path, movimiento_archivo: Callable[[Path], None], ruta_origen_carpeta: Path, ruta_destino_carpeta: Path) -> Observer:
    """ Función que crea el Observer para despues ser activado.
    Args:
        - extensiones(list(str)): Una lista de extensiones a darle monitoreo.
        - ruta_proyecto(Path): La ruta base del proyecto.
        - movimiento_archivo(Callable): Función encargada de mover los archivos.

    """
    observer = Observer()
    handler = Monitoreo(extensiones, ruta_proyecto, movimiento_archivo, ruta_origen_carpeta, ruta_destino_carpeta)

    observer.schedule(handler, path=ruta_origen_carpeta, recursive=True)

    return observer


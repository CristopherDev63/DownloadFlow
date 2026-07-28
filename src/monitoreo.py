from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from typing import Callable
from pathlib import Path
import logging 
import time


class Monitoreo(PatternMatchingEventHandler):
    """ Clase monitoreo en tiempo real """
    def __init__(self, extensiones: list[str], ruta_base: Path, movimiento_archivo: Callable[[Path, Path], None], ruta_origen_carpeta: Path, ruta_destino_carpeta: Path) -> None:
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
                ignore_patterns=["*.crdownload", "*.temp", "*.part"],
                ignore_directories=True,
                case_sensitive=False
        )


    def _acortador_ruta(self, ruta: Path) -> Path | None:
        """ Función que acorta rutas.
        Args:
            - ruta(Path): La ruta a acortar.
        Returns:
            - Path or None: La ruta de archivo acortado.
        """
        try:
            ruta = Path(ruta)
            return ruta.relative_to(self.ruta_base)
        except ValueError as e:
            logging.error(f"Problema al a cortar la ruta {e}")

    
    def _esperar_escritura_completa(self, ruta_archivo: Path, timeout=60) -> bool | None:
        """ Función que se encarga de verificar nom cambie el tamaño durante un segundo consecutivo
        Args:
            - ruta_archivo(Path): La ruta del archivo a comprobar el tamaño.
            - timeout(int): El tiempo máximo o de limite que tiene el script.

        """
        ruta_archivo = Path(ruta_archivo)
        tiempo_inicio = time.time()
        tamano_previo_archivo = -1

        while time.time() - tiempo_inicio < timeout:
            if ruta_archivo.exists():
                try:
                    tamano_actual = ruta_archivo.stat().st_size
                    if tamano_actual > 0 and tamano_actual == tamano_previo_archivo:
                        return True 

                    tamano_previo_archivo = tamano_actual

                except OSError:
                    pass

            time.sleep(1)
        
        return False 


    def on_created(self, event) -> None:
        """ Cuando se crean nuevos archivos se encarga de manejar sus eventos """
        ruta_archivo = Path(event.src_path)
        ruta_origen_archivo = self._acortador_ruta(ruta_archivo)
        
        logging.debug(f"Detección de archivo nuevo [{ruta_origen_archivo}]")

        if self._esperar_escritura_completa(ruta_archivo):
            self.movimiento_archivo(ruta_archivo, self.ruta_destino_carpeta)


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


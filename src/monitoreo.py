from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from pathlib import Path
import logging 


logging.getLogger(__name__)


class Monitoreo(PatternMatchingEventHandler):
    """ Clase monitoreo en tiempo real """
    def __init__(self, extensiones: list[str], ruta_proyecto: Path) -> None:
        """ Dentro de este constructor definimos los filtros del monitoreo.
        Args:
            - extensiones(list(str)): Una lista de extensiones a darle monitoreo.
        """
        self.ruta_proyecto = ruta_proyecto

        super().__init__(
                patterns=extensiones,
                ignore_directories=True,
                case_sensitive=False
        )


    def _acortador_ruta(self, ruta: Path) -> Path | None:
        """ Función que acorta rutas PARA MOSTRAR AL USUARIO, no para uso técnico.
        Args:
            - ruta(Path): La ruta a acortar.
        """
        try:
            return ruta.relative_to(self.ruta_proyecto)
        except ValueError as e:
            logging.error(f"Problema al a cortar la ruta {e}")

        

    def on_created(self, event) -> None:
        """ Cuando se crean nuevos archivos se encarga de manejar sus eventos """
        ruta = self._acortador_ruta(event.src_path)



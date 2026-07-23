from watchdog.observers import Observer
from monitoreo import creacion_monitorizacion
from config import carga_configuracion
from traslado_archivo import movimiento_archivos
from pathlib import Path 
import logging 
import time


RUTA_BASE = Path.home()
RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_REGISTROS = RUTA_PROYECTO / "registros.log"
RUTA_CONFIGURACION = RUTA_PROYECTO / "config.yaml"


logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(RUTA_REGISTROS)
            ]
        )

logging.getLogger(__name__)
logging.getLogger("fsevents").setLevel(logging.WARNING) # Desactivamos el logging de fsevents


if __name__ == "__main__":
    data_configuracion = carga_configuracion(RUTA_CONFIGURACION)
    ruta_origen_carpeta = data_configuracion.carpeta_origen
    ruta_destino_carpeta = data_configuracion.carpeta_destino
    lista_extensiones = data_configuracion.Filtrado.lista_patrones

    observer = creacion_monitorizacion(lista_extensiones, RUTA_BASE, movimiento_archivos, ruta_origen_carpeta, ruta_destino_carpeta)
    observer.start()
    logging.info(f"Comenzado Monitoreo en [{ruta_origen_carpeta.relative_to(RUTA_BASE)}] {"-"*4}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info(f"Monitoreo Detenido {"-"*4}")
    
    observer.join()
    

from pydantic import BaseModel
from pathlib import Path 
import yaml 


class contrato_datos_configuracion(BaseModel):
    """ Contrato de datos para verificación de configuración """
    carpeta_origen: Path
    carpeta_destino: Path


def carga_configuracion(ruta: Path) -> contrato_datos_configuracion:
    """ Función que se encarga de cargar toda deserialización
    Args:
        - ruta(path): La ruta del archivo de configuración.
    Returns:
        - Dict: La data deserializada 
    """
    with open(ruta, "r") as f:
        data_sinprocesar = yaml.safe_load(f)

    return contrato_datos_configuracion(**data_sinprocesar)

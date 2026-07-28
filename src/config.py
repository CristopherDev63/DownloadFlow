from pydantic import BaseModel, field_validator, model_validator
from pathlib import Path 
import yaml 


class lista_extensiones(BaseModel):
    extensiones_agregar: list[str]
    palabras_clave: list[str]
    
    lista_patrones: list [str] = []

    @field_validator("extensiones_agregar", mode="before")
    @classmethod
    def traduccion_datos(cls, value):
        """ Se dedica en dejar en limpio las exntesiones de la configuración. """
        patron = []

        for ext in value:
            ext_limpio = ext.strip().lstrip(".") # Quitamos espacios y puntos

            if ext_limpio:
                patron.append(f"*.{ext_limpio}")

        return patron


    @field_validator("palabras_clave", mode="before")
    @classmethod
    def traduccion_palabras_clave(cls, value):
        """ Función encargada de dejar limpio los datos de patrones de nombres de archivos """
        patron = []

        for ext in value:
            ext_limpio = ext.strip()
            
            if ext_limpio:
                patron.append(f"*{ext_limpio}*.*")

        return patron

    
    @model_validator(mode="after")
    def lista_patrones_completo(self) -> "lista_extensiones":
        """ Función encargada de combinar la lista de exntesiones y nombres de archivos. """
        self.lista_patrones = self.extensiones_agregar + self.palabras_clave 

        return self


class contrato_datos_configuracion(BaseModel):
    """ Contrato de datos para verificación de configuración """
    carpeta_origen: Path
    carpeta_destino: Path
    filtrado: lista_extensiones



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

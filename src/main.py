from pathlib import Path 

RUTA_BASE = Path.home()
RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_CONFIGURACION = RUTA_PROYECTO / "config.yaml"


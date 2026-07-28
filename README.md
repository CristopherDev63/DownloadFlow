# DownloadFlow

Script en Python que monitoriza la carpeta de Descargas (o cualquier carpeta configurada) y mueve automáticamente los archivos nuevos a una carpeta de destino según extensiones y palabras clave definidas.

## Características

- **Monitoreo en tiempo real** con `watchdog` — detecta archivos nuevos al instante.
- **Filtrado por extensión y nombre** — solo mueve archivos que coincidan con los patrones configurados (ej. `*.png`, `*factura*.*`).
- **Espera a que la descarga termine** — verifica que el tamaño del archivo se estabilice antes de moverlo (evita mover archivos incompletos).
- **Manejo de duplicados** — si ya existe un archivo con el mismo nombre en el destino, lo renombra automáticamente (`archivo_copia_1.json`, `archivo_copia_2.json`, ...).
- **Configuración vía YAML** — fácil de modificar sin tocar código.
- **Persistencia en segundo plano** — crea una tarea `@reboot` en crontab para que el script se ejecute automáticamente al iniciar sesión.
- **Logging detallado** — registros en consola y archivo (`registros.log`).

## Requisitos

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) (gestor de proyectos y entornos virtuales)

## Instalación

```bash
uv sync
```

Si no usas `uv`, puedes crear un venv manualmente:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # o pyproject.toml
```

## Configuración

Edita `config.yaml`:

```yaml
carpeta_origen: "/Users/tu_usuario/Downloads"
carpeta_destino: "/Users/tu_usuario/Documents/organizados"

filtrado:
  extensiones_agregar: ["png", "json", "py"]
  palabras_clave: ["factura", "documento_empresa", "reporte"]
```

- `carpeta_origen`: carpeta a monitorear.
- `carpeta_destino`: carpeta donde se moverán los archivos.
- `extensiones_agregar`: solo archivos con estas extensiones.
- `palabras_clave`: archivos cuyo nombre contenga alguna de estas palabras (independientemente de la extensión).

## Uso

```bash
python3 src/main.py
```

El script creará automáticamente una tarea en crontab para ejecutarse al reiniciar el sistema.

## Estructura

```
.
├── config.yaml          # Configuración del usuario
├── registros.log        # Archivo de logs
├── src/
│   ├── main.py          # Punto de entrada
│   ├── config.py        # Carga y validación de configuración (Pydantic)
│   ├── monitoreo.py     # Lógica de monitoreo con watchdog
│   ├── traslado_archivo.py  # Movimiento y renombrado de archivos
│   └── crear_tarea_segundo_plano.py  # Configuración de crontab
├── tests/
└── pyproject.toml
```

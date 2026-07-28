from crontab import CronTab
from pathlib import Path 



def crear_tarea_automatizacion(ruta_motor_script: Path, ruta_script: Path, ruta_registros: Path):
    """ Se encarga de crear una tarea en segundo plano. """
    cron = CronTab(user=True)
    

    cron.env["PATH"] = "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"
    cron.env["SHELL"] = "/bin/bash"
    cron.env["HOME"] = "/Users/cristopherrobledo/"


    cron.remove_all(comment="administrador_archivos_tarea")

    comando_final = f"{ruta_motor_script} {ruta_script} >> {ruta_registros} 2>&1"
    tarea = cron.new(command=comando_final, comment="administrador_archivos_tarea")
    
    tarea.setall("@reboot")
    cron.write()


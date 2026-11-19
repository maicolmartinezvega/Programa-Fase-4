# logger.py
# Módulo encargado de registrar eventos y errores en un archivo de texto (.log)

from datetime import datetime

class RegistradorLogs:
    """Gestiona la escritura de eventos y errores en un archivo sin usar bases de datos."""
    
    def __init__(self, nombre_archivo="eventos_sistema.log"):
# Nombre del archivo donde se guardará el historial
        self.nombre_archivo = nombre_archivo

    def registrar(self, nivel, mensaje):
        """Escribe una línea con fecha, hora, nivel (INFO/ERROR) y el mensaje."""
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{fecha_hora}] [{nivel}] {mensaje}\n"
        try:
# Abre el archivo en modo 'a' (agregar al final) con codificación UTF-8
            with open(self.nombre_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except Exception as e:
# Si falla la escritura en disco, se muestra por consola sin detener el programa
            print(f"Error crítico al escribir en el log: {e}")

    def info(self, mensaje):
        """Registra una operación exitosa o informativa."""
        self.registrar("INFO", mensaje)

    def error(self, mensaje):
        """Registra un error o excepción capturada."""
        self.registrar("ERROR", mensaje)
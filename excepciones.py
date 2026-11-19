# excepciones.py
# Módulo con las excepciones personalizadas del sistema Software FJ

class ErrorSoftwareFJ(Exception):
    """Excepción base para todos los errores controlados del sistema."""
    pass

class DatosInvalidosError(ErrorSoftwareFJ):
    """Se lanza cuando los datos ingresados (cédula, correo, valores) son incorrectos."""
    pass

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio no existe o ya está ocupado."""
    pass

class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva no cumple las reglas (ej. horas <= 0 o estado inválido)."""
    pass

class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando ocurre un fallo matemático o financiero al calcular costos."""
    pass
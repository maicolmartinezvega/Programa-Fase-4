# reserva.py
# Clase Reserva que integra Cliente, Servicio, duración y control de estados

from excepciones import ReservaInvalidaError, ServicioNoDisponibleError

class Reserva:
    """Gestiona una reserva individual para un cliente y un servicio específico."""
    
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA")

    def __init__(self, id_reserva, cliente, servicio, horas, impuesto=0.19, descuento=0.0):
        if not id_reserva or not str(id_reserva).strip():
            raise ReservaInvalidaError("El ID de la reserva no puede estar vacío.")
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("La reserva requiere un cliente y un servicio válidos.")
        
        self.id_reserva = str(id_reserva).strip()
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.impuesto = impuesto
        self.descuento = descuento
        self.estado = "PENDIENTE"
        
# Calcula y valida los parámetros desde la creación

        self.costo_total = self.servicio.calcular_costo(horas, impuesto, descuento)

    def confirmar(self):
        """Confirma la reserva si el servicio está disponible y cambia su estado."""
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError(f"No se puede confirmar la reserva {self.id_reserva} porque ya fue cancelada.")
        if self.estado == "CONFIRMADA":
            raise ReservaInvalidaError(f"La reserva {self.id_reserva} ya se encuentra confirmada.")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre}' no está disponible actualmente.")
        
        self.servicio.disponible = False
        self.estado = "CONFIRMADA"

    def cancelar(self):
        """Cancela la reserva y libera el servicio si estaba ocupado por esta reserva."""
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.id_reserva} ya estaba cancelada.")
        
        if self.estado == "CONFIRMADA":
            self.servicio.disponible = True
        self.estado = "CANCELADA"

    def obtener_detalle(self):
        return (
            f"Reserva [{self.id_reserva}] | Estado: {self.estado} | "
            f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre} | "
            f"Duración: {self.horas}h | Total: ${self.costo_total:,.2f}"
        )
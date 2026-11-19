# gestor.py
# Controlador principal del sistema Software FJ almacenamiento en listas y manejo avanzado de excepciones

from modelos import Cliente, Servicio
from reserva import Reserva
from excepciones import ErrorSoftwareFJ, DatosInvalidosError, ReservaInvalidaError
from logger import RegistradorLogs

class SistemaSoftwareFJ:
    """Administra clientes, servicios y reservas en memoria registrando cada evento en el log."""
    
    def __init__(self):
        
# Listas internas en memoria (sin bases de datos)

        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.log = RegistradorLogs()
        self.log.info("=== Inicio del sistema Software FJ ===")

    def buscar_cliente(self, id_cliente):
        for c in self.clientes:
            if c.id_entidad == id_cliente:
                return c
        return None

    def buscar_servicio(self, id_servicio):
        for s in self.servicios:
            if s.id_entidad == id_servicio:
                return s
        return None

    def buscar_reserva(self, id_reserva):
        for r in self.reservas:
            if r.id_reserva == id_reserva:
                return r
        return None

    def registrar_cliente(self, id_cliente, nombre, correo, telefono):
        """Registra un cliente usando try/except/else/finally."""
        nuevo_cliente = None
        try:
            if self.buscar_cliente(id_cliente) is not None:
                raise DatosInvalidosError(f"Ya existe un cliente con ID '{id_cliente}'.")
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
        except ErrorSoftwareFJ as e:
            self.log.error(f"Error al registrar cliente ({id_cliente}): {e}")
            print(f"[ERROR CONTROLADO] Cliente '{id_cliente}': {e}")
            return None
        else:
            self.clientes.append(nuevo_cliente)
            self.log.info(f"Cliente registrado exitosamente: {nuevo_cliente.obtener_resumen()}")
            print(f"[OK] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente
        finally:
            
# Bloque finally exigido en la guía para garantizar trazabilidad de cierre de operación

            self.log.info(f"Finalizó intento de registro de cliente ID: {id_cliente}")

    def registrar_servicio(self, servicio):
        """Agrega un objeto de tipo Servicio a la lista interna."""
        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError("El objeto proporcionado no es un Servicio válido.")
            if self.buscar_servicio(servicio.id_entidad) is not None:
                raise DatosInvalidosError(f"Ya existe un servicio con ID '{servicio.id_entidad}'.")
        except ErrorSoftwareFJ as e:
            self.log.error(f"Error al registrar servicio: {e}")
            print(f"[ERROR CONTROLADO] Servicio: {e}")
            return None
        else:
            self.servicios.append(servicio)
            self.log.info(f"Servicio registrado: {servicio.obtener_resumen()} | {servicio.describir_servicio()}")
            print(f"[OK] {servicio.obtener_resumen()}")
            return servicio

    def crear_y_confirmar_reserva(self, id_reserva, id_cliente, id_servicio, horas, impuesto=0.19, descuento=0.0):
        """Crea y confirma una reserva capturando cualquier excepción sin detener el sistema."""
        try:
            if self.buscar_reserva(id_reserva) is not None:
                raise ReservaInvalidaError(f"El ID de reserva '{id_reserva}' ya existe.")
            
            cliente = self.buscar_cliente(id_cliente)
            if cliente is None:
                raise ReservaInvalidaError(f"No existe el cliente con ID '{id_cliente}'.")
            
            servicio = self.buscar_servicio(id_servicio)
            if servicio is None:
                raise ReservaInvalidaError(f"No existe el servicio con ID '{id_servicio}'.")

            reserva = Reserva(id_reserva, cliente, servicio, horas, impuesto, descuento)
            reserva.confirmar()
        except ErrorSoftwareFJ as e:
            
# Si hubo excepción encadenada (__cause__), también se registra en el log

            detalle_causa = f" | Causa interna: {e.__cause__}" if e.__cause__ else ""
            self.log.error(f"Fallo en reserva '{id_reserva}': {e}{detalle_causa}")
            print(f"[ERROR CONTROLADO] Reserva '{id_reserva}': {e}{detalle_causa}")
            return None
        else:
            self.reservas.append(reserva)
            self.log.info(f"Reserva confirmada: {reserva.obtener_detalle()}")
            print(f"[OK] {reserva.obtener_detalle()}")
            return reserva
        finally:
            self.log.info(f"Procesamiento de reserva '{id_reserva}' concluido.")

    def cancelar_reserva(self, id_reserva):
        """Cancela una reserva existente y libera el recurso."""
        try:
            reserva = self.buscar_reserva(id_reserva)
            if reserva is None:
                raise ReservaInvalidaError(f"No se encontró la reserva '{id_reserva}' para cancelar.")
            reserva.cancelar()
        except ErrorSoftwareFJ as e:
            self.log.error(f"Fallo al cancelar reserva '{id_reserva}': {e}")
            print(f"[ERROR CONTROLADO] Cancelación '{id_reserva}': {e}")
        else:
            self.log.info(f"Reserva cancelada correctamente: {reserva.obtener_detalle()}")
            print(f"[OK] Reserva '{id_reserva}' cancelada y servicio liberado.")
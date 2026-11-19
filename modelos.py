# modelos.py
# Contiene las clases abstractas, Cliente y los servicios especializados

from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError, CalculoInconsistenteError

class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad general del sistema."""
    
    def __init__(self, id_entidad):
        if not id_entidad or not str(id_entidad).strip():
            raise DatosInvalidosError("El ID de la entidad no puede estar vacío.")
        self._id_entidad = str(id_entidad).strip()

    @property
    def id_entidad(self):
        return self._id_entidad

    @abstractmethod
    def obtener_resumen(self):
        """Método abstracto que obliga a las clases hijas a describirse."""
        pass


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""
    
    def __init__(self, id_cliente, nombre, correo, telefono):
        super().__init__(id_cliente)
# Se usan los setters para validar desde el momento de creación
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in valor or "." not in valor:
            raise DatosInvalidosError(f"Correo electrónico inválido: '{valor}'.")
        self.__correo = valor.strip()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor or not str(valor).isdigit() or len(str(valor)) < 7:
            raise DatosInvalidosError(f"Teléfono inválido (debe tener mínimo 7 dígitos): '{valor}'.")
        self.__telefono = str(valor).strip()

    def obtener_resumen(self):
        return f"Cliente [{self.id_entidad}]: {self.__nombre} | Tel: {self.__telefono} | Email: {self.__correo}"


class Servicio(EntidadSistema, ABC):
    """Clase abstracta que define la estructura base de todos los servicios de Software FJ."""
    
    def __init__(self, id_servicio, nombre, tarifa_hora):
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio no puede estar vacío.")
        if tarifa_hora <= 0:
            raise DatosInvalidosError("La tarifa por hora debe ser mayor a cero.")
        
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, horas):
        """Valida reglas específicas de cada tipo de servicio."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Devuelve la descripción detallada del servicio."""
        pass

    def calcular_costo(self, horas, impuesto=0.19, descuento=0.0):
        """
        Método con parámetros opcionales (sobrecarga funcional) para calcular costos
        con IVA por defecto (19%) y descuentos opcionales.
        """
        try:
            self.validar_parametros(horas)
            if impuesto < 0 or descuento < 0 or descuento > 1:
                raise CalculoInconsistenteError("Porcentajes de impuesto o descuento fuera de rango.")
            
            subtotal = self._tarifa_hora * horas
            valor_descuento = subtotal * descuento
            base_imponible = subtotal - valor_descuento
            total = base_imponible * (1 + impuesto)
            
            if total <= 0:
                raise CalculoInconsistenteError("El costo total calculado no puede ser menor o igual a cero.")
            return round(total, 2)
        except Exception as e:
 # Encadenamiento de excepciones exigido en la guía
            raise CalculoInconsistenteError(f"Fallo al calcular el costo del servicio '{self._nombre}'.") from e

    def obtener_resumen(self):
        estado = "Disponible" if self._disponible else "Ocupado"
        return f"Servicio [{self.id_entidad}] {self._nombre} (${self._tarifa_hora}/h) - {estado}"


class ReservaSala(Servicio):
    """Servicio especializado 1: Alquiler de salas de reuniones o capacitación."""
    
    def __init__(self, id_servicio, nombre, tarifa_hora, capacidad_personas):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if capacidad_personas <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a 0 personas.")
        self.capacidad_personas = capacidad_personas

    def validar_parametros(self, horas):
        if horas < 1 or horas > 12:
            raise DatosInvalidosError("Las salas solo se reservan entre 1 y 12 horas.")

    def describir_servicio(self):
        return f"Sala '{self._nombre}' con capacidad para {self.capacidad_personas} personas."


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Alquiler de equipos tecnológicos."""
    
    def __init__(self, id_servicio, nombre, tarifa_hora, tipo_equipo):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if not tipo_equipo or not tipo_equipo.strip():
            raise DatosInvalidosError("Debe especificar el tipo de equipo.")
        self.tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, horas):
        if horas < 2:
            raise DatosInvalidosError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def describir_servicio(self):
        return f"Equipo '{self._nombre}' (Categoría: {self.tipo_equipo})."


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Consultoría y asesoría técnica."""
    
    def __init__(self, id_servicio, nombre, tarifa_hora, especialidad):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if not especialidad or not especialidad.strip():
            raise DatosInvalidosError("Debe indicar el área de especialidad de la asesoría.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, horas):
        if horas <= 0 or horas > 8:
            raise DatosInvalidosError("Las asesorías deben durar entre 1 y 8 horas.")

    def describir_servicio(self):
        return f"Asesoría en {self.especialidad}: '{self._nombre}'."
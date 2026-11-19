# main.py
# Script principal de ejecución y simulación de 12 operaciones para Software FJ

from gestor import SistemaSoftwareFJ
from modelos import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import DatosInvalidosError

def ejecutar_simulacion():
    print("   SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ (FASE 4 UNAD)")

    sistema = SistemaSoftwareFJ()

    print("1. REGISTRO DE CLIENTES (VÁLIDOS E INVÁLIDOS)")
# Operación 1: Cliente válido
    sistema.registrar_cliente("C001", "Maicol Martínez", "mamartinezv2@unadvirtual.edu.co", "3105551234")
# Operación 2: Cliente válido
    sistema.registrar_cliente("C002", "Laura Gómez", "laura.gomez@empresa.com", "3209876543")
# Operación 3: Cliente inválido (correo sin @ y teléfono corto) -> El sistema captura el error y sigue
    sistema.registrar_cliente("C003", "Carlos Ruiz", "correo_invalido.com", "123")
# Operación 4: Cliente duplicado -> Error controlado
    sistema.registrar_cliente("C001", "Maicol Duplicado", "otro@correo.com", "3001112233")

    print("\n--- 2. CREACIÓN DE SERVICIOS (POLIMORFISMO Y VALIDACIONES) ---")
# Operación 5: Servicio válido - Sala
    sala1 = ReservaSala("S001", "Sala Innovación Norte", 80000, 15)
    sistema.registrar_servicio(sala1)

# Operación 6: Servicio válido - Equipo
    equipo1 = AlquilerEquipo("E001", "Workstation Dell Precision", 35000, "Computador Alto Rendimiento")
    sistema.registrar_servicio(equipo1)

# Operación 7: Servicio válido - Asesoría
    asesoria1 = AsesoriaEspecializada("A001", "Arquitectura Cloud y Python", 120000, "Ingeniería de Software")
    sistema.registrar_servicio(asesoria1)

# Operación 8: Creación inválida de servicio (tarifa negativa) -> Captura directa en instanciación
    try:
        sala_invalida = ReservaSala("S002", "Sala Error", -50000, 10)
        sistema.registrar_servicio(sala_invalida)
    except DatosInvalidosError as e:
        sistema.log.error(f"Error al instanciar servicio S002: {e}")
        print(f"[ERROR CONTROLADO] Instanciación de servicio S002: {e}")

    print("\n--- 3. GESTIÓN DE RESERVAS (EXITOSAS, FALLIDAS Y SOBRECARGA) ---")
# Operación 9: Reserva exitosa (con IVA por defecto del 19% y sin descuento)
    sistema.crear_y_confirmar_reserva("R001", "C001", "S001", horas=4)

# Operación 10: Reserva fallida (intentar reservar la misma sala S001 que ya está ocupada)
    sistema.crear_y_confirmar_reserva("R002", "C002", "S001", horas=2)

# Operación 11: Reserva fallida por validación polimórfica + encadenamiento de excepciones
# (AlquilerEquipo exige mínimo 2 horas; al pasar 1 hora lanza DatosInvalidosError encadenado en CalculoInconsistenteError)
    sistema.crear_y_confirmar_reserva("R003", "C002", "E001", horas=1)

# Operación 12: Reserva exitosa usando sobrecarga de parámetros (10% de descuento aplicado)
    sistema.crear_y_confirmar_reserva("R004", "C002", "A001", horas=3, impuesto=0.19, descuento=0.10)

    print("\n--- 4. CANCELACIÓN Y REUTILIZACIÓN DE SERVICIO ---")
# Cancelar R001 para liberar la Sala S001
    sistema.cancelar_reserva("R001")
# Ahora C002 sí puede reservar la Sala S001 que quedó libre
    sistema.crear_y_confirmar_reserva("R005", "C002", "S001", horas=2)


    print("   SIMULACIÓN FINALIZADA SIN INTERRUPCIONES")
    print(f"   Total Clientes: {len(sistema.clientes)} | Servicios: {len(sistema.servicios)} | Reservas: {len(sistema.reservas)}")
    print("   Revise el archivo 'eventos_sistema.log' para ver el historial.")


if __name__ == "__main__":
    ejecutar_simulacion()
"""
Módulo para la creación de hoteles, clientes y reservas.
"""

from class_hotel import Hotel
from class_customer import Customer
from class_reservation import Reservation


def crear_hotel():
    """Función para crear un nuevo hotel y guardarlo en la base de datos."""
    print("\n🏨 Creación de hotel")
    hotel_nombre = input("Ingrese el nombre del hotel: ").strip()
    ubicacion = input("Ingrese la ubicación del hotel: ").strip()

    try:
        habitaciones = int(
            input("Ingrese el número de habitaciones: ").strip()
        )
        if habitaciones <= 0:
            raise ValueError
    except ValueError:
        print(
            "❌ El número de habitaciones debe ser un número "
            "entero válido y mayor a 0."
        )
        return

    resultado = Hotel.crear_hotel(hotel_nombre, ubicacion, habitaciones)
    if resultado is True:
        print(f"✅ Hotel '{hotel_nombre}' creado correctamente.")
    else:
        print(resultado)


def crear_cliente():
    """Función para crear un nuevo cliente y guardarlo en la base de datos."""
    print("\n👤 Creación de cliente")
    cliente_nombre = input("Ingrese el nombre del cliente: ").strip()
    email = input("Ingrese el correo electrónico del cliente: ").strip()

    resultado = Customer.crear_cliente(cliente_nombre, email)
    if resultado is True:
        print(f"✅ Cliente '{cliente_nombre}' creado correctamente.")
    else:
        print(resultado)


def crear_reserva():
    """Función para crear una reserva verificando si el hotel y el cliente."""
    print("\n📅 Creación de reserva")
    hotel_nombre = input("Ingrese el nombre del hotel: ").strip()
    cliente_nombre = input("Ingrese el nombre del cliente: ").strip()

    # Cargar hoteles y clientes
    hoteles = Hotel.cargar_hoteles()
    clientes = Customer.cargar_clientes()

    # Validar si existen
    hotel_existe = any(hotel.nombre == hotel_nombre for hotel in hoteles)
    cliente_existe = any(
        cliente.nombre == cliente_nombre for cliente in clientes
    )

    if not hotel_existe:
        print("❌ No se encontró el hotel.")
        return

    if not cliente_existe:
        print("❌ No se encontró el cliente.")
        return

    # Crear la reserva
    resultado = Reservation.crear_reserva(hotel_nombre, cliente_nombre)
    if resultado is True:
        print(
            f"✅ Reserva creada en '{hotel_nombre}' para '{cliente_nombre}'."
        )
    else:
        print(resultado)

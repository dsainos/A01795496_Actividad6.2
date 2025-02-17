"""
Módulo para la eliminación de hoteles, clientes y reservas.
"""

import json


def eliminar_hotel():
    """Elimina un hotel si existe en la base de datos."""
    hotel_name = input("Nombre del hotel a eliminar: ").strip()

    try:
        with open("hoteles.json", "r+", encoding="utf-8") as file:
            hoteles = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ No se encontró el archivo de hoteles.")
        return

    hotel_existente = any(
        hotel.get("nombre") == hotel_name for hotel in hoteles
    )
    if not hotel_existente:
        print("❌ No se encontró el hotel.")
        return

    hoteles = [hotel for hotel in hoteles if hotel.get("nombre") != hotel_name]

    with open("hoteles.json", "w", encoding="utf-8") as file:
        json.dump(hoteles, file, indent=4)

    print(f"✅ Hotel '{hotel_name}' eliminado correctamente.")


def eliminar_cliente():
    """Elimina un cliente si existe en la base de datos."""
    cliente_name = input("Nombre del cliente a eliminar: ").strip()

    try:
        with open("clientes.json", "r+", encoding="utf-8") as file:
            clientes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ No se encontró el archivo de clientes.")
        return

    cliente_existente = any(
        cliente.get("nombre") == cliente_name for cliente in clientes
    )
    if not cliente_existente:
        print("❌ No se encontró el cliente.")
        return

    clientes = [
        cliente
        for cliente in clientes
        if cliente.get("nombre") != cliente_name
    ]

    with open("clientes.json", "w", encoding="utf-8") as file:
        json.dump(clientes, file, indent=4)

    print(f"✅ Cliente '{cliente_name}' eliminado correctamente.")


def cancelar_reserva():
    """Cancela una reserva si existe en la base de datos."""
    try:
        with open("reservas.json", "r+", encoding="utf-8") as file:
            reservas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ No hay reservas registradas.")
        return

    if not reservas:
        print("⚠️ No hay reservas para cancelar.")
        return

    print("\n📂 Reservas disponibles:")
    for i, reserva in enumerate(reservas, start=1):
        print(f"{i}. Cliente: {reserva['cliente']}, Hotel: {reserva['hotel']}")

    try:
        index = int(input("Ingrese el número de la reserva a cancelar: ")) - 1
        if index < 0 or index >= len(reservas):
            print("❌ Entrada no válida. Debes ingresar un número válido.")
            return

        reserva_cancelada = reservas.pop(index)

        with open("reservas.json", "w", encoding="utf-8") as file:
            json.dump(reservas, file, indent=4)

        print(
            f"✅ Reserva de {reserva_cancelada['cliente']} en "
            f"{reserva_cancelada['hotel']} ha sido cancelada."
        )

    except ValueError:
        print("❌ Entrada no válida. Debes ingresar un número.")

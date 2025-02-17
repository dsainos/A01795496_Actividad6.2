"""
Módulo para gestionar reservas en un sistema de hoteles.
"""

import json


class Reservation:
    """Clase para gestionar reservas"""

    ARCHIVO_RESERVAS = "reservas.json"

    def __init__(self, hotel, cliente):
        self.hotel = hotel
        self.cliente = cliente

    def to_dict(self):
        """Convierte una reserva a un diccionario"""
        return {"hotel": self.hotel, "cliente": self.cliente}

    @staticmethod
    def crear_reserva(hotel_nombre, cliente_nombre):
        """Crea una nueva reserva y la guarda"""
        if not hotel_nombre or not cliente_nombre:
            return "❌ El hotel y el cliente deben estar especificados."

        reservas = Reservation.cargar_reservas()
        nueva_reserva = Reservation(hotel_nombre, cliente_nombre)
        reservas.append(nueva_reserva)
        Reservation.guardar_reservas(reservas)
        return True

    @staticmethod
    def guardar_reservas(reservas):
        """Guarda la lista de reservas en un archivo JSON"""
        with open(Reservation.ARCHIVO_RESERVAS, "w", encoding="utf-8") as file:
            json.dump(
                [reserva.to_dict() for reserva in reservas], file, indent=4
            )

    @staticmethod
    def cargar_reservas():
        """Carga las reservas desde un archivo JSON"""
        try:
            with open(
                Reservation.ARCHIVO_RESERVAS, "r", encoding="utf-8"
            ) as file:
                reservas = json.load(file)
                return [
                    Reservation(r.get("hotel", ""), r.get("cliente", ""))
                    for r in reservas
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ No hay reservas registradas aún.")
            return []

"""
Módulo para gestionar la creación, modificación y eliminación de hoteles.
"""

import json


class Hotel:
    """Clase para gestionar hoteles"""

    ARCHIVO_HOTELES = "hoteles.json"

    def __init__(self, nombre, ubicacion, habitaciones):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.habitaciones = habitaciones
        self.reservas = []

    def to_dict(self):
        """Convierte un objeto Hotel a un diccionario"""
        return {
            "nombre": self.nombre,
            "ubicacion": self.ubicacion,
            "habitaciones": self.habitaciones,
            "reservas": self.reservas,
        }

    @staticmethod
    def guardar_hoteles(hoteles):
        """Guarda la lista de hoteles en un archivo JSON"""
        with open(Hotel.ARCHIVO_HOTELES, "w", encoding="utf-8") as file:
            json.dump([hotel.to_dict() for hotel in hoteles], file, indent=4)

    @staticmethod
    def cargar_hoteles():
        """Carga los hoteles desde un archivo JSON"""
        try:
            with open(Hotel.ARCHIVO_HOTELES, "r", encoding="utf-8") as file:
                hoteles = json.load(file)
                return [
                    Hotel(
                        h.get("nombre", ""),
                        h.get("ubicacion", ""),
                        h.get("habitaciones", 0),
                    )
                    for h in hoteles
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ No hay hoteles registrados aún.")
            return []

    @staticmethod
    def crear_hotel(nombre, ubicacion, habitaciones):
        """Crea un nuevo hotel y lo guarda"""
        if not nombre:
            return "❌ El nombre del hotel no puede estar vacío."
        if not ubicacion:
            return "❌ La ubicación del hotel no puede estar vacía."
        if not isinstance(habitaciones, int) or habitaciones <= 0:
            return (
                "❌ El número de habitaciones debe ser un número entero válido "
                "y mayor a 0."
            )

        hoteles = Hotel.cargar_hoteles()
        nuevo_hotel = Hotel(nombre, ubicacion, habitaciones)
        hoteles.append(nuevo_hotel)
        Hotel.guardar_hoteles(hoteles)
        return f"✅ Hotel '{nombre}' creado correctamente."

    @staticmethod
    def modificar_hotel(nombre, nueva_ubicacion, nuevas_habitaciones):
        """Modifica un hotel existente"""
        hoteles = Hotel.cargar_hoteles()
        for hotel in hoteles:
            if hotel.nombre.lower() == nombre.lower():
                hotel.ubicacion = nueva_ubicacion
                hotel.habitaciones = nuevas_habitaciones
                Hotel.guardar_hoteles(hoteles)
                return True
        return "❌ No se encontró el hotel."

    @staticmethod
    def eliminar_hotel(nombre):
        """Elimina un hotel existente"""
        hoteles = Hotel.cargar_hoteles()
        hoteles_filtrados = [
            hotel
            for hotel in hoteles
            if hotel.nombre.lower() != nombre.lower()
        ]

        if len(hoteles) == len(hoteles_filtrados):
            return "❌ No se encontró el hotel."

        Hotel.guardar_hoteles(hoteles_filtrados)
        return True

"""
Módulo para gestionar clientes en un sistema de reservas.
"""
import json
import os
import re


class Customer:
    """Clase para gestionar clientes"""

    ARCHIVO_CLIENTES = "clientes.json"

    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

    def to_dict(self):
        """Convierte un objeto Customer a un diccionario"""
        return {"nombre": self.nombre, "email": self.email}

    def validar_datos(self):
        """Valida los datos del cliente"""
        if not self.nombre:
            return "❌ El nombre del cliente no puede estar vacío."
        if not self.email:
            return "❌ El correo electrónico no puede estar vacío."
        if not re.match(
            r"[^@]+@[^@]+\.[^@]+", self.email
        ):  # Validación de email agregada
            return "❌ El correo electrónico no es válido."
        return True

    @staticmethod
    def crear_cliente(nombre, email):
        """Crea un nuevo cliente y lo guarda"""
        cliente = Customer(nombre, email)
        validacion = cliente.validar_datos()
        if validacion is not True:
            return validacion

        clientes = Customer.cargar_clientes()
        clientes.append(cliente)
        Customer.guardar_clientes(clientes)
        return True

    @staticmethod
    def eliminar_cliente(nombre):
        """Elimina un cliente por nombre"""
        clientes = Customer.cargar_clientes()
        clientes_filtrados = [
            cliente
            for cliente in clientes
            if cliente.nombre.lower() != nombre.lower()
        ]

        if len(clientes) == len(clientes_filtrados):
            return "❌ No se encontró el cliente."

        Customer.guardar_clientes(clientes_filtrados)
        return True

    @staticmethod
    def guardar_clientes(clientes):
        """Guarda la lista de clientes en un archivo JSON"""
        with open(Customer.ARCHIVO_CLIENTES, "w", encoding="utf-8") as file:
            json.dump(
                [cliente.to_dict() for cliente in clientes], file, indent=4
            )

    @staticmethod
    def cargar_clientes():
        """Carga los clientes desde un archivo JSON"""
        if not os.path.exists(Customer.ARCHIVO_CLIENTES):
            print("⚠️ No hay clientes registrados aún.")
            return []

        try:
            with open(
                Customer.ARCHIVO_CLIENTES, "r", encoding="utf-8"
            ) as file:
                clientes = json.load(file)
                if not isinstance(clientes, list):
                    raise json.JSONDecodeError("Formato incorrecto", "", 0)
                return [
                    Customer(c.get("nombre", ""), c.get("email", ""))
                    for c in clientes
                    if "nombre" in c and "email" in c
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ No hay clientes registrados aún.")
            return []

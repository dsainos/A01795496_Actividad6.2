"""
Pruebas unitarias.
"""

import unittest
from unittest.mock import patch

# import json
# from io import StringIO
from creacion_semimanual import crear_hotel, crear_cliente, crear_reserva


class TestCreacionSemimanual(unittest.TestCase):
    """Pruebas para la gestión"""
    @patch("builtins.input", side_effect=["Hotel Prueba", "CDMX", "10"])
    @patch("builtins.print")
    def test_crear_hotel_exitoso(self, mock_print, _):
        """Prueba la creación de un hotel con datos válidos"""
        crear_hotel()
        mock_print.assert_any_call(
            "✅ Hotel 'Hotel Prueba' creado correctamente."
        )

    @patch(
        "builtins.input", side_effect=["Hotel Prueba", "CDMX", "abc"]
    )  # Entrada inválida para habitaciones
    @patch("builtins.print")
    def test_crear_hotel_habitaciones_invalidas(self, mock_print, _):
        """No se pueda crear un hotel con habitaciones no numéricas"""
        crear_hotel()
        mock_print.assert_any_call(
            "❌ El número de habitaciones debe ser un número "
            "entero válido y mayor a 0."
        )

    @patch("builtins.input", side_effect=["Juan Pérez", "juan@example.com"])
    @patch("builtins.print")
    def test_crear_cliente_exitoso(self, mock_print, _):
        """Prueba la creación de un cliente con datos válidos"""
        crear_cliente()
        mock_print.assert_any_call(
            "✅ Cliente 'Juan Pérez' creado correctamente."
        )

    @patch(
        "builtins.input", side_effect=["", "juan@example.com"]
    )  # Nombre vacío
    @patch("builtins.print")
    def test_crear_cliente_nombre_vacio(self, mock_print, _):
        """Prueba que no se pueda crear un cliente con nombre vacío"""
        crear_cliente()
        mock_print.assert_any_call(
            "❌ El nombre del cliente no puede estar vacío."
        )

    @patch(
        "builtins.input", side_effect=["Juan Pérez", "correo-invalido"]
    )  # Email inválido
    @patch("builtins.print")
    def test_crear_cliente_email_invalido(self, mock_print, _):
        """Prueba que no se pueda crear un cliente con un email inválido"""
        crear_cliente()
        mock_print.assert_any_call("❌ El correo electrónico no es válido.")

    @patch("builtins.input", side_effect=["Hotel Prueba", "Juan Pérez"])
    @patch("builtins.print")
    def test_crear_reserva_exitosa(self, mock_print, _):
        """Prueba la creación de una reserva con datos válidos"""
        crear_reserva()
        mock_print.assert_any_call(
            "✅ Reserva creada en 'Hotel Prueba' para 'Juan Pérez'."
        )

    @patch(
        "builtins.input", side_effect=["Hotel Fantasma", "Juan Pérez"]
    )  # Hotel no existe
    @patch("builtins.print")
    def test_crear_reserva_hotel_no_existe(self, mock_print, _):
        """Prueba que no se pueda crear una reserva si el hotel no existe"""
        crear_reserva()
        mock_print.assert_any_call("❌ No se encontró el hotel.")

    @patch(
        "builtins.input", side_effect=["Hotel Prueba", "Cliente Fantasma"]
    )  # Cliente no existe
    @patch("builtins.print")
    def test_crear_reserva_cliente_no_existe(self, mock_print, _):
        """Prueba que no se pueda crear una reserva si el cliente no existe"""
        crear_reserva()
        mock_print.assert_any_call("❌ No se encontró el cliente.")


if __name__ == "__main__":
    unittest.main()

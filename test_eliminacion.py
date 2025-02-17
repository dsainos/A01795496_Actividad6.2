"""
Pruebas de eliminacion.
"""

import unittest
from unittest.mock import patch, mock_open
import json

# from io import StringIO
from eliminacion_semimanual import eliminar_hotel, eliminar_cliente


class TestEliminacionSemimanual(unittest.TestCase):
    """Pruebas para eliminacion"""
    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_eliminar_hotel_archivo_no_existente(self, mock_print, _):
        """Prueba eliminar un hotel cuando el archivo no existe"""
        with patch(
            "builtins.input", side_effect=["Hotel X"]
        ):  # 🔥 agrega `patch("builtins.input")`
            eliminar_hotel()
            mock_print.assert_any_call(
                "❌ No se encontró el archivo de hoteles."
            )

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_eliminar_cliente_archivo_no_existente(
        self, mock_print, _
    ):
        """Prueba eliminar un cliente cuando el archivo no existe"""
        with patch(
            "builtins.input", side_effect=["Cliente X"]
        ):  # 🔥 Se agrega `patch("builtins.input")`
            eliminar_cliente()
            mock_print.assert_any_call(
                "❌ No se encontró el archivo de clientes."
            )

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    @patch("builtins.print")
    def test_eliminar_hotel_no_existente(self, mock_print, _):
        """Prueba eliminar un hotel que no existe"""
        with patch(
            "builtins.input", side_effect=["Hotel Fantasma"]
        ):  # 🔥 Se agrega `patch("builtins.input")`
            eliminar_hotel()
            mock_print.assert_any_call("❌ No se encontró el hotel.")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    @patch("builtins.print")
    def test_eliminar_cliente_no_existente(self, mock_print, _):
        """Prueba eliminar un cliente que no existe"""
        with patch(
            "builtins.input", side_effect=["Cliente Desconocido"]
        ):  # 🔥 Se agrega `patch("builtins.input")`
            eliminar_cliente()
            mock_print.assert_any_call("❌ No se encontró el cliente.")


if __name__ == "__main__":
    unittest.main()

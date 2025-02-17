"""
Pruebas de reservas.
"""

import unittest
from unittest.mock import patch, mock_open
import json
from io import StringIO
from eliminacion_semimanual import (
    eliminar_hotel,
    eliminar_cliente,
    cancelar_reserva,
)
from class_reservation import Reservation


class TestReservas(unittest.TestCase):
    """Pruebas para reservas"""
    @patch("builtins.input", side_effect=["Juan Pérez"])
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [
                {"nombre": "Juan Pérez", "email": "juan@example.com"}
            ]  # Cliente existente en JSON
        ),
    )
    def test_eliminar_cliente(self, _mock_file, _mock_input):
        """Prueba eliminar un cliente existente"""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            eliminar_cliente()
            output = mock_stdout.getvalue().strip()
            self.assertIn(
                "✅ Cliente 'Juan Pérez' eliminado correctamente.", output
            )

    @patch("builtins.input", side_effect=["Hotel Prueba"])
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [
                {
                    "nombre": "Hotel Prueba",
                    "ubicacion": "CDMX",
                    "habitaciones": 10,
                }
            ]  # Hotel existen JSON
        ),
    )
    def test_eliminar_hotel(self, _mock_file, _mock_input):
        """Prueba eliminar un hotel existente"""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            eliminar_hotel()
            output = mock_stdout.getvalue().strip()
            self.assertIn(
                "✅ Hotel 'Hotel Prueba' eliminado correctamente.", output
            )

    @patch(
        "builtins.open", new_callable=mock_open, read_data=json.dumps([])
    )  # No hay reservas
    @patch(
        "builtins.input", side_effect=["1"]
    )  # Intentamos cancelar la reserva 1
    def test_cancelar_reserva_sin_reservas(self, _mock_file, _mock_input):
        """Prueba cancelar una reserva cuando no hay reservas registradas"""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            cancelar_reserva()
            output = mock_stdout.getvalue().strip()
            self.assertIn("⚠️ No hay reservas para cancelar.", output)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [
                {"cliente": "Juan Pérez", "hotel": "Hotel Prueba"}
            ]  # Reserva existente
        ),
    )
    @patch(
        "builtins.input", side_effect=["1"]
    )  # Seleccionamos la única reserva existente
    def test_cancelar_reserva_existente(self, _mock_file, _mock_input):
        """Prueba cancelar una reserva existente"""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            cancelar_reserva()
            output = mock_stdout.getvalue().strip()
            self.assertIn(
                "✅ Reserva de Juan Pérez en Hotel Prueba ha sido cancelada.",
                output,
            )

    @patch(
        "builtins.open", new_callable=mock_open, read_data="{invalid json}"
    )  # JSON corrupto
    @patch("builtins.print")
    def test_cargar_reservas_json_corrupto(self, mock_print, _):
        """Prueba cargar reservas con un JSON corrupto"""
        reservas = Reservation.cargar_reservas()
        self.assertEqual(reservas, [])
        mock_print.assert_any_call("⚠️ No hay reservas registradas aún.")

    @patch("builtins.open", side_effect=FileNotFoundError)  # Archivo no existe
    @patch("builtins.print")
    def test_cargar_reservas_sin_archivo(self, mock_print, _):
        """Prueba cargar reservas cuando el archivo no existe"""
        reservas = Reservation.cargar_reservas()
        self.assertEqual(reservas, [])
        mock_print.assert_any_call("⚠️ No hay reservas registradas aún.")

    @patch(
        "builtins.open", new_callable=mock_open, read_data=json.dumps([])
    )  # JSON vacío
    @patch("builtins.print")
    def test_crear_reserva(self, _mock_print, _):
        """Prueba crear una nueva reserva"""
        nueva_reserva = Reservation("Juan Pérez", "Hotel Prueba")
        reservas = [nueva_reserva]
        with patch("json.dump") as mock_json:
            Reservation.guardar_reservas(reservas)
            mock_json.assert_called_once()


if __name__ == "__main__":
    unittest.main()

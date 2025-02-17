"""
Pruebas unitarias para la clase Hotel.
"""

import unittest
from unittest.mock import patch, mock_open
import json
from class_hotel import Hotel


class TestHotel(unittest.TestCase):
    """Pruebas para la gestión de hoteles."""
    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_cargar_hoteles_sin_archivo(self, mock_print, _):
        """Prueba cuando el archivo de hoteles no existe"""
        hoteles = Hotel.cargar_hoteles()
        self.assertEqual(hoteles, [])
        mock_print.assert_any_call("⚠️ No hay hoteles registrados aún.")

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
            ]
        ),
    )
    def test_cargar_hoteles_existente(self, _):
        """Prueba la carga de hoteles existentes"""
        hoteles = Hotel.cargar_hoteles()
        self.assertEqual(len(hoteles), 1)
        self.assertEqual(hoteles[0].nombre, "Hotel Prueba")
        self.assertEqual(hoteles[0].ubicacion, "CDMX")
        self.assertEqual(hoteles[0].habitaciones, 10)

    @patch("builtins.open", new_callable=mock_open, read_data="{invalid json}")
    @patch("builtins.print")
    def test_cargar_hoteles_json_corrupto(self, mock_print, _):
        """Prueba la carga de hoteles con un JSON corrupto"""
        hoteles = Hotel.cargar_hoteles()
        self.assertEqual(hoteles, [])
        mock_print.assert_any_call("⚠️ No hay hoteles registrados aún.")

    def test_validar_hotel_sin_nombre(self):
        """Prueba que no se pueda crear un hotel sin nombre"""
        resultado = Hotel.crear_hotel("", "CDMX", 10)
        self.assertEqual(
            resultado, "❌ El nombre del hotel no puede estar vacío."
        )

    def test_validar_hotel_sin_ubicacion(self):
        """Prueba que no se pueda crear un hotel sin ubicación"""
        resultado = Hotel.crear_hotel("Hotel Prueba", "", 10)
        self.assertEqual(
            resultado, "❌ La ubicación del hotel no puede estar vacía."
        )

    def test_validar_hotel_habitaciones_invalidas(self):
        """Prueba no crear un hotel con número de habitaciones inválido"""
        resultado = Hotel.crear_hotel("Hotel Prueba", "CDMX", -5)
        self.assertEqual(
            resultado,
            (
                "❌ El número de habitaciones debe ser un número entero válido "
                "y mayor a 0."
            ),
        )

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_guardar_hotel(self, _):
        """Prueba si `guardar_hoteles()` escribe datos correctamente"""
        hoteles = [Hotel("Hotel Prueba", "CDMX", 10)]
        with patch("json.dump") as mock_json:
            Hotel.guardar_hoteles(hoteles)
            mock_json.assert_called_once()

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
            ]
        ),
    )
    def test_eliminar_hotel_existente(self, _):
        """Prueba que se elimine un hotel existente"""
        resultado = Hotel.eliminar_hotel("Hotel Prueba")
        self.assertEqual(resultado, True)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [{"nombre": "Otro Hotel", "ubicacion": "GDL", "habitaciones": 20}]
        ),
    )
    def test_eliminar_hotel_no_existente(self, _):
        """Prueba eliminar un hotel que no existe"""
        resultado = Hotel.eliminar_hotel("Hotel Prueba")
        self.assertEqual(resultado, "❌ No se encontró el hotel.")


if __name__ == "__main__":
    unittest.main()

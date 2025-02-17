"""
Pruebas unitarias para la clase Customer.
"""

import unittest
from unittest.mock import patch, mock_open
import json
from class_customer import Customer


class TestCustomer(unittest.TestCase):
    """Pruebas para la gestión de clientes."""
    @patch(
        "builtins.open", side_effect=FileNotFoundError
    )  # Simular que el archivo no existe
    @patch("builtins.print")  # Simular la impresión en consola
    def test_cargar_clientes_sin_archivo(self, mock_print, _):
        """Prueba cuando el archivo de clientes no existe o está vacío"""
        clientes = Customer.cargar_clientes()
        self.assertEqual(clientes, [])
        mock_print.assert_any_call("⚠️ No hay clientes registrados aún.")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [{"nombre": "Juan", "email": "juan@example.com"}]
        ),
    )
    def test_cargar_clientes_existente(self, _):
        """Prueba la carga de clientes existentes"""
        clientes = Customer.cargar_clientes()
        self.assertEqual(len(clientes), 1)
        self.assertEqual(clientes[0].nombre, "Juan")
        self.assertEqual(clientes[0].email, "juan@example.com")

    @patch("builtins.open", new_callable=mock_open, read_data="{invalid json}")
    @patch("builtins.print")  # Simular impresión en consola
    def test_cargar_clientes_json_corrupto(self, mock_print, _):
        """Prueba la carga de clientes con un JSON corrupto"""
        clientes = Customer.cargar_clientes()
        self.assertEqual(clientes, [])
        mock_print.assert_any_call("⚠️ No hay clientes registrados aún.")

    def test_validar_cliente_sin_nombre(self):
        """Prueba que no se pueda crear un cliente sin nombre"""
        cliente = Customer("", "juan@example.com")
        self.assertEqual(
            cliente.validar_datos(),
            "❌ El nombre del cliente no puede estar vacío.",
        )

    def test_validar_cliente_sin_email(self):
        """Prueba que no se pueda crear un cliente sin email"""
        cliente = Customer("Juan", "")
        self.assertEqual(
            cliente.validar_datos(),
            "❌ El correo electrónico no puede estar vacío.",
        )

    def test_validar_cliente_email_invalido(self):
        """Prueba que no se acepte un email inválido"""
        cliente = Customer("Juan", "correo-invalido")
        self.assertEqual(
            cliente.validar_datos(), "❌ El correo electrónico no es válido."
        )

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_guardar_cliente(self, _):
        """Prueba si `guardar_clientes()` escribe datos correctamente"""
        clientes = [Customer("Juan", "juan@example.com")]
        with patch("json.dump") as mock_json:
            Customer.guardar_clientes(clientes)
            mock_json.assert_called_once()

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [{"nombre": "Juan", "email": "juan@example.com"}]
        ),
    )
    def test_eliminar_cliente_existente(self, _):
        """Prueba que se elimine un cliente existente"""
        resultado = Customer.eliminar_cliente("Juan")
        self.assertEqual(resultado, True)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [{"nombre": "Pedro", "email": "pedro@example.com"}]
        ),
    )
    def test_eliminar_cliente_no_existente(self, _):
        """Prueba eliminar un cliente que no existe"""
        resultado = Customer.eliminar_cliente("Juan")
        self.assertEqual(resultado, "❌ No se encontró el cliente.")


if __name__ == "__main__":
    unittest.main()

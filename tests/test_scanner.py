
import unittest
from unittest.mock import patch, MagicMock

from main import port_tara


class TestPortScanner(unittest.TestCase):

    @patch("main.socket.socket")
    def test_acik_port(self, mock_socket):
        baglanti = MagicMock()
        baglanti.connect_ex.return_value = 0

        mock_socket.return_value.__enter__.return_value = baglanti

        sonuc = port_tara(5432)

        self.assertEqual(sonuc, "ACIK")

    @patch("main.socket.socket")
    def test_kapali_port(self, mock_socket):
        baglanti = MagicMock()
        baglanti.connect_ex.return_value = 111

        mock_socket.return_value.__enter__.return_value = baglanti

        sonuc = port_tara(5432)

        self.assertEqual(sonuc, "KAPALI/ERISILEMIYOR")

    @patch("main.socket.socket")
    def test_baglanti_hatasi(self, mock_socket):
        mock_socket.side_effect = OSError("Baglanti hatasi")

        sonuc = port_tara(5432)

        self.assertEqual(sonuc, "HATA")


if __name__ == "__main__":
    unittest.main()

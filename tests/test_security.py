
import unittest

from risk_engine import risk_analiz
from recommendation_engine import guvenlik_onerileri


class TestShadowNet(unittest.TestCase):

    def test_kapali_port_riski(self):
        sonuc = risk_analiz(5432, "KAPALI/ERISILEMIYOR")
        self.assertEqual(sonuc["seviye"], "YOK")

    def test_acik_postgresql_riski(self):
        sonuc = risk_analiz(5432, "ACIK")
        self.assertEqual(sonuc["seviye"], "INCELE")

    def test_kapali_port_onerileri(self):
        sonuc = guvenlik_onerileri(
            5432,
            "KAPALI/ERISILEMIYOR",
            {"adresler": []}
        )
        self.assertEqual(sonuc["oneri_sayisi"], 0)

    def test_postgresql_onerileri(self):
        sonuc = guvenlik_onerileri(
            5432,
            "ACIK",
            {"adresler": ["0.0.0.0", "::"]}
        )
        self.assertEqual(sonuc["oneri_sayisi"], 4)


if __name__ == "__main__":
    unittest.main()

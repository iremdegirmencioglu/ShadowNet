
import socket
import json
from datetime import datetime
from pathlib import Path

from risk_engine import risk_analiz
from service_detector import servis_tespit
from exposure_analyzer import erisim_analiz
from recommendation_engine import guvenlik_onerileri
from html_report import html_rapor_olustur


# ==========================================
# SHADOWNET v0.9 - SECURITY ANALYZER
# ==========================================

HEDEF = "127.0.0.1"

SERVISLER = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8080: "HTTP-Alternatif"
}


def port_tara(port):
    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as baglanti:

            baglanti.settimeout(1)
            sonuc = baglanti.connect_ex((HEDEF, port))

            if sonuc == 0:
                return "ACIK"

            return "KAPALI/ERISILEMIYOR"

    except OSError:
        return "HATA"


def main():

    print("=" * 60)
    print("SHADOWNET v0.9 - SECURITY ANALYZER")
    print("=" * 60)

    sonuclar = []

    # 1. PORT TARAMASI
    for port, servis in SERVISLER.items():

        durum = port_tara(port)

        # 2. RISK ANALIZI
        risk = risk_analiz(port, durum)

        # 3. SERVIS VE AG ERISIM ANALIZI
        if durum == "ACIK":

            servis_bilgisi = servis_tespit(port)
            erisim_bilgisi = erisim_analiz(port)

        else:

            servis_bilgisi = {
                "durum": "TARANMADI",
                "islemler": []
            }

            erisim_bilgisi = {
                "durum": "TARANMADI",
                "adresler": [],
                "aciklama": "Port acik degil."
            }

        # 4. GUVENLIK ONERILERI
        oneri_bilgisi = guvenlik_onerileri(
            port,
            durum,
            erisim_bilgisi
        )

        # 5. RAPOR VERILERI
        bilgi = {
            "port": port,
            "olasi_servis": servis,
            "durum": durum,
            "servis_tespiti": servis_bilgisi,
            "ag_erisimi": erisim_bilgisi,
            "risk_seviyesi": risk["seviye"],
            "risk_aciklamasi": risk["aciklama"],
            "guvenlik_onerileri": oneri_bilgisi
        }

        sonuclar.append(bilgi)

        # 6. TERMINAL CIKTISI
        print("\n" + "-" * 60)
        print(f"Port: {port}")
        print(f"Olasi servis: {servis}")
        print(f"Durum: {durum}")

        for islem in servis_bilgisi["islemler"]:
            print(f"Gercek islem: {islem['islem_adi']}")
            print(f"PID: {islem['pid']}")

        print(
            f"Ag erisim durumu: "
            f"{erisim_bilgisi['durum']}"
        )

        print(
            f"Dinleme adresleri: "
            f"{erisim_bilgisi['adresler']}"
        )

        print(
            f"Ag aciklamasi: "
            f"{erisim_bilgisi['aciklama']}"
        )

        print(
            f"Risk degerlendirmesi: "
            f"{risk['seviye']}"
        )

        print(
            f"Risk aciklamasi: "
            f"{risk['aciklama']}"
        )

        print("Guvenlik onerileri:")

        if oneri_bilgisi["oneriler"]:
            for oneri in oneri_bilgisi["oneriler"]:
                print(f"  - {oneri}")
        else:
            print("  - Oneri bulunmuyor.")

    # 7. JSON RAPORUNU OLUSTUR
    rapor = {
        "proje": "ShadowNet",
        "versiyon": "0.9",
        "hedef": HEDEF,
        "tarih": datetime.now().isoformat(),
        "sonuclar": sonuclar
    }

    rapor_klasoru = (
        Path(__file__).resolve().parent / "reports"
    )

    rapor_klasoru.mkdir(
        parents=True,
        exist_ok=True
    )

    dosya_adi = datetime.now().strftime(
        "scan_%Y%m%d_%H%M%S_%f.json"
    )

    dosya_yolu = rapor_klasoru / dosya_adi

    # 8. JSON RAPORUNU KAYDET
    with open(
        dosya_yolu,
        "w",
        encoding="utf-8"
    ) as dosya:

        json.dump(
            rapor,
            dosya,
            indent=4,
            ensure_ascii=False
        )

    # 9. HTML RAPORUNU OTOMATIK OLUSTUR
    html_yolu = html_rapor_olustur(dosya_yolu)

    # 10. GENEL GUVENLIK OZETI
    acik_sayisi = sum(
        1
        for sonuc in sonuclar
        if sonuc["durum"] == "ACIK"
    )

    inceleme_sayisi = sum(
        1
        for sonuc in sonuclar
        if sonuc["risk_seviyesi"] == "INCELE"
    )

    ag_inceleme_sayisi = sum(
        1
        for sonuc in sonuclar
        if sonuc["ag_erisimi"]["durum"] == "INCELE"
    )

    toplam_oneri = sum(
        sonuc["guvenlik_onerileri"]["oneri_sayisi"]
        for sonuc in sonuclar
    )

    # 11. RAPOR OZETI
    print("\n" + "=" * 60)
    print("SHADOWNET v0.9 - GUVENLIK RAPORU")
    print("=" * 60)

    print(f"Hedef: {HEDEF}")
    print(f"Kontrol edilen port: {len(sonuclar)}")
    print(f"Acik port sayisi: {acik_sayisi}")
    print(f"Risk inceleme sayisi: {inceleme_sayisi}")
    print(f"Ag erisim inceleme sayisi: {ag_inceleme_sayisi}")
    print(f"Toplam guvenlik onerisi: {toplam_oneri}")

    print(f"\nJSON raporu: {dosya_yolu}")
    print(f"HTML raporu: {html_yolu}")

    print("\nAnaliz tamamlandi!")


if __name__ == "__main__":
    main()

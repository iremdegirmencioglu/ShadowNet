
import psutil


def erisim_analiz(port):
    adresler = set()

    try:
        baglantilar = psutil.net_connections(kind="tcp")

        for baglanti in baglantilar:
            if baglanti.status != psutil.CONN_LISTEN:
                continue

            if not baglanti.laddr:
                continue

            if baglanti.laddr.port == port:
                adresler.add(baglanti.laddr.ip)

    except (psutil.AccessDenied, OSError) as hata:
        return {
            "durum": "HATA",
            "adresler": [],
            "aciklama": str(hata)
        }

    if not adresler:
        return {
            "durum": "BILINMIYOR",
            "adresler": [],
            "aciklama": "Dinleme adresi bulunamadi."
        }

    if "0.0.0.0" in adresler or "::" in adresler:
        durum = "INCELE"
        aciklama = "Servis tum ag arayuzlerinde dinliyor olabilir."

    elif adresler.issubset({"127.0.0.1", "::1"}):
        durum = "YEREL"
        aciklama = "Servis sadece yerel baglantilari dinliyor."

    else:
        durum = "INCELE"
        aciklama = "Servis belirli ag arayuzlerinde dinliyor."

    return {
        "durum": durum,
        "adresler": sorted(adresler),
        "aciklama": aciklama
    }


if __name__ == "__main__":
    print("SHADOWNET v0.6 - NETWORK EXPOSURE ANALYZER")
    print(erisim_analiz(5432))

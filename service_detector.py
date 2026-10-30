
import psutil


def servis_tespit(port):
    bulunan_islemler = []
    gorulen_pidler = set()

    try:
        baglantilar = psutil.net_connections(kind="tcp")

        for baglanti in baglantilar:
            if baglanti.status != psutil.CONN_LISTEN:
                continue

            if not baglanti.laddr:
                continue

            if baglanti.laddr.port != port:
                continue

            pid = baglanti.pid

            if pid is None or pid in gorulen_pidler:
                continue

            gorulen_pidler.add(pid)

            try:
                islem = psutil.Process(pid)

                bulunan_islemler.append({
                    "pid": pid,
                    "islem_adi": islem.name()
                })

            except (psutil.NoSuchProcess,
                    psutil.AccessDenied):
                bulunan_islemler.append({
                    "pid": pid,
                    "islem_adi": "BILINMIYOR"
                })

    except (psutil.AccessDenied, OSError) as hata:
        return {
            "durum": "HATA",
            "aciklama": str(hata),
            "islemler": []
        }

    return {
        "durum": "TAMAMLANDI",
        "islemler": bulunan_islemler
    }


if __name__ == "__main__":
    print("SHADOWNET - SERVICE DETECTOR")

    sonuc = servis_tespit(5432)

    print(sonuc)

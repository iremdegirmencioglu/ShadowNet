
def guvenlik_onerileri(port, durum, erisim_bilgisi):
    oneriler = []

    if durum != "ACIK":
        return {
            "oneri_sayisi": 0,
            "oneriler": []
        }

    if port == 21:
        oneriler.append(
            "FTP yerine SFTP veya FTPS kullanimi degerlendirilmeli."
        )

    elif port == 22:
        oneriler.append(
            "SSH icin guclu kimlik dogrulama ve erisim sinirlari kontrol edilmeli."
        )

    elif port == 80:
        oneriler.append(
            "HTTP trafigi icin HTTPS kullanimi degerlendirilmeli."
        )

    elif port == 3306:
        oneriler.append(
            "MySQL erisimi yalnizca gerekli istemcilerle sinirlandirilmali."
        )

    elif port == 5432:
        oneriler.append(
            "PostgreSQL pg_hba.conf erisim kurallari incelenmeli."
        )
        oneriler.append(
            "Veritabani kullanicilarina en az yetki verilmeli."
        )

    adresler = erisim_bilgisi.get("adresler", [])

    if "0.0.0.0" in adresler or "::" in adresler:
        oneriler.append(
            "Servisin tum ag arayuzlerinde dinlemesi gerekli mi kontrol edilmeli."
        )
        oneriler.append(
            "Guvenlik duvari ile gereksiz ag erisimleri engellenmeli."
        )

    if not oneriler:
        oneriler.append(
            "Servis surumu, erisim izinleri ve guvenlik ayarlari incelenmeli."
        )

    return {
        "oneri_sayisi": len(oneriler),
        "oneriler": oneriler
    }


if __name__ == "__main__":
    test_erisimi = {
        "durum": "INCELE",
        "adresler": ["0.0.0.0", "::"]
    }

    sonuc = guvenlik_onerileri(
        5432,
        "ACIK",
        test_erisimi
    )

    print("SHADOWNET v0.7 - SECURITY RECOMMENDATION ENGINE")

    for oneri in sonuc["oneriler"]:
        print(f"- {oneri}")

    print(f"Toplam oneri: {sonuc['oneri_sayisi']}")

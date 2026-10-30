
# ShadowNet - Risk Analysis Engine

RISK_KURALLARI = {
    21: {
        "seviye": "INCELE",
        "aciklama": "FTP servisi olabilir. "
                    "Sifrelenmemis veri aktarimi kontrol edilmeli."
    },
    22: {
        "seviye": "BILGI",
        "aciklama": "SSH servisi olabilir. "
                    "Kimlik dogrulama ayarlari incelenmeli."
    },
    80: {
        "seviye": "INCELE",
        "aciklama": "HTTP servisi olabilir. "
                    "HTTPS yonlendirmesi kontrol edilmeli."
    },
    3306: {
        "seviye": "INCELE",
        "aciklama": "MySQL servisi olabilir. "
                    "Veritabani erisim izinleri incelenmeli."
    },
    5432: {
        "seviye": "INCELE",
        "aciklama": "PostgreSQL servisi olabilir. "
                    "Ag erisimi ve kimlik dogrulama incelenmeli."
    }
}


def risk_analiz(port, durum):
    if durum != "ACIK":
        return {
            "seviye": "YOK",
            "aciklama": "Acik TCP portu tespit edilmedi."
        }

    if port in RISK_KURALLARI:
        return RISK_KURALLARI[port].copy()

    return {
        "seviye": "BILGI",
        "aciklama": "Acik port tespit edildi. "
                    "Calisan servis dogrulanmali."
    }

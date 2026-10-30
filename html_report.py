
import json
import html
from pathlib import Path


def guvenli(deger):
    return html.escape(str(deger), quote=True)


def html_rapor_olustur(json_yolu):
    json_yolu = Path(json_yolu)

    with open(json_yolu, "r", encoding="utf-8") as dosya:
        rapor = json.load(dosya)

    sonuclar = rapor.get("sonuclar", [])

    toplam = len(sonuclar)
    acik = sum(
        1 for s in sonuclar
        if s.get("durum") == "ACIK"
    )
    kapali = sum(
        1 for s in sonuclar
        if s.get("durum") == "KAPALI/ERISILEMIYOR"
    )
    hata = toplam - acik - kapali

    riskli = sum(
        1 for s in sonuclar
        if s.get("risk_seviyesi") == "INCELE"
    )

    toplam_oneri = sum(
        len(s.get("guvenlik_onerileri", {}).get("oneriler", []))
        for s in sonuclar
    )

    def yuzde(sayi):
        return round(sayi / toplam * 100, 1) if toplam else 0

    satirlar = []

    for s in sonuclar:
        port = guvenli(s.get("port", "-"))
        servis = guvenli(s.get("olasi_servis", "-"))
        durum = s.get("durum", "-")
        risk = s.get("risk_seviyesi", "-")

        servis_bilgisi = s.get("servis_tespiti", {})
        islemler = servis_bilgisi.get("islemler", [])

        if islemler:
            islem_metni = ", ".join(
                f"{guvenli(i.get('islem_adi', '-'))} "
                f"(PID: {guvenli(i.get('pid', '-'))})"
                for i in islemler
            )
        else:
            islem_metni = "-"

        erisim = s.get("ag_erisimi", {})
        adresler = ", ".join(
            guvenli(a) for a in erisim.get("adresler", [])
        ) or "-"

        oneriler = s.get(
            "guvenlik_onerileri", {}
        ).get("oneriler", [])

        if oneriler:
            oneri_metni = "<ul>" + "".join(
                f"<li>{guvenli(o)}</li>"
                for o in oneriler
            ) + "</ul>"
        else:
            oneri_metni = "-"

        durum_sinifi = (
            "success" if durum == "ACIK"
            else "muted"
        )
        risk_sinifi = (
            "warning" if risk == "INCELE"
            else "muted"
        )

        satirlar.append(f"""
        <tr>
            <td>{port}</td>
            <td>{servis}</td>
            <td>
                <span class="pill {durum_sinifi}">
                    {guvenli(durum)}
                </span>
            </td>
            <td>{islem_metni}</td>
            <td>{adresler}</td>
            <td>
                <span class="pill {risk_sinifi}">
                    {guvenli(risk)}
                </span>
                <p>{guvenli(s.get("risk_aciklamasi", ""))}</p>
            </td>
            <td>{oneri_metni}</td>
        </tr>
        """)

    satir_html = "\n".join(satirlar)

    # Grafik dilimleri, toplam port sayisina gore hesaplanir.
    acik_yuzde = yuzde(acik)
    kapali_yuzde = yuzde(kapali)
    hata_yuzde = yuzde(hata)

    html_icerik = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ShadowNet Security Dashboard</title>
<style>
:root {
    color-scheme: dark;
    --bg: #0b1020;
    --panel: #151d31;
    --border: #29344c;
    --text: #edf2ff;
    --muted: #a2aec6;
    --green: #34d399;
    --blue: #60a5fa;
    --orange: #fbbf24;
    --red: #fb7185;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: "Segoe UI", Arial, sans-serif;
}

.container {
    max-width: 1450px;
    margin: auto;
    padding: 32px 22px;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 28px;
}

h1 {
    font-size: 30px;
    margin: 0 0 8px;
}

h2 { font-size: 19px; margin-top: 0; }

.subtitle, .note, td p {
    color: var(--muted);
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.card, .panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px;
}

.card .number {
    font-size: 36px;
    font-weight: 750;
    margin-top: 10px;
}

.card .label { color: var(--muted); }

.charts {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 18px;
    margin-bottom: 24px;
}

.donut {
    width: 210px;
    height: 210px;
    margin: 20px auto;
    border-radius: 50%;
    display: grid;
    place-items: center;
    position: relative;
}

.donut::after {
    content: "";
    position: absolute;
    inset: 35px;
    background: var(--panel);
    border-radius: 50%;
}

.donut span {
    z-index: 1;
    font-size: 29px;
    font-weight: bold;
}

.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    justify-content: center;
}

.dot {
    display: inline-block;
    width: 11px;
    height: 11px;
    border-radius: 50%;
    margin-right: 6px;
}

.bar-row {
    margin: 22px 0;
}

.bar-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.track {
    height: 16px;
    background: #29344c;
    border-radius: 20px;
    overflow: hidden;
}

.fill {
    height: 100%;
    border-radius: 20px;
}

.table-wrap { overflow-x: auto; }

table {
    border-collapse: collapse;
    width: 100%;
    min-width: 1000px;
}

th, td {
    text-align: left;
    padding: 14px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
    font-size: 13px;
}

th {
    color: var(--muted);
    font-weight: 600;
}

.pill {
    display: inline-block;
    border-radius: 20px;
    padding: 5px 10px;
    font-size: 12px;
}

.success {
    background: #064e3b;
    color: #a7f3d0;
}

.warning {
    background: #78350f;
    color: #fde68a;
}

.muted {
    background: #334155;
    color: #cbd5e1;
}

ul { padding-left: 18px; }
li { margin-bottom: 7px; }

footer {
    color: var(--muted);
    text-align: center;
    margin-top: 30px;
    font-size: 12px;
}

@media (max-width: 600px) {
    .container { padding: 18px 12px; }
    h1 { font-size: 24px; }
}
</style>
</head>
<body>
<div class="container">

<header>
    <div>
        <h1>ShadowNet Security Dashboard</h1>
        <div class="subtitle">
            Yerel sistem guvenlik analizi | Surum: __VERSION__
        </div>
    </div>
    <div class="subtitle">
        Hedef: __TARGET__<br>
        Tarih: __DATE__
    </div>
</header>

<section class="cards">
    <div class="card">
        <div class="label">Taranan Port</div>
        <div class="number">__TOTAL__</div>
    </div>
    <div class="card">
        <div class="label">Acik Port</div>
        <div class="number">__OPEN__</div>
    </div>
    <div class="card">
        <div class="label">Incelenecek Risk</div>
        <div class="number">__RISK__</div>
    </div>
    <div class="card">
        <div class="label">Guvenlik Onerisi</div>
        <div class="number">__RECOMMENDATIONS__</div>
    </div>
</section>

<section class="charts">
    <div class="panel">
        <h2>Port Durum Dagilimi</h2>
        <div class="donut" style="background:conic-gradient(
            var(--green) 0% __OPEN_PCT__%,
            var(--blue) __OPEN_PCT__% __CLOSED_END__%,
            var(--red) __CLOSED_END__% 100%
        );">
            <span>__TOTAL__</span>
        </div>
        <div class="legend">
            <span><i class="dot" style="background:var(--green)"></i>Acik: __OPEN__</span>
            <span><i class="dot" style="background:var(--blue)"></i>Kapali/Erisilemiyor: __CLOSED__</span>
            <span><i class="dot" style="background:var(--red)"></i>Hata: __ERROR__</span>
        </div>
    </div>

    <div class="panel">
        <h2>Risk ve Durum Analizi</h2>

        <div class="bar-row">
            <div class="bar-label"><span>Acik portlar</span><span>__OPEN_PCT__%</span></div>
            <div class="track">
                <div class="fill" style="width:__OPEN_PCT__%;background:var(--green)"></div>
            </div>
        </div>

        <div class="bar-row">
            <div class="bar-label"><span>Incelenecek riskler</span><span>__RISK_PCT__%</span></div>
            <div class="track">
                <div class="fill" style="width:__RISK_PCT__%;background:var(--orange)"></div>
            </div>
        </div>

        <div class="bar-row">
            <div class="bar-label"><span>Tarama hatalari</span><span>__ERROR_PCT__%</span></div>
            <div class="track">
                <div class="fill" style="width:__ERROR_PCT__%;background:var(--red)"></div>
            </div>
        </div>

        <p class="note">
            Risk isaretleri otomatik degerlendirmedir;
            dogrulanmis guvenlik acigi anlamina gelmez.
        </p>
    </div>
</section>

<section class="panel">
    <h2>Detayli Port ve Servis Analizi</h2>
    <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>Port</th>
                    <th>Olası Servis</th>
                    <th>Durum</th>
                    <th>Gercek Islem</th>
                    <th>Dinleme Adresleri</th>
                    <th>Risk</th>
                    <th>Guvenlik Onerileri</th>
                </tr>
            </thead>
            <tbody>
                __ROWS__
            </tbody>
        </table>
    </div>
</section>

<footer>
    ShadowNet v1.0 | Yerel analiz raporu |
    Sadece izinli sistemlerde kullanin.
</footer>

</div>
</body>
</html>
"""

    degiskenler = {
        "__VERSION__": "1.0",
        "__TARGET__": guvenli(rapor.get("hedef", "-")),
        "__DATE__": guvenli(rapor.get("tarih", "-")),
        "__TOTAL__": str(toplam),
        "__OPEN__": str(acik),
        "__CLOSED__": str(kapali),
        "__ERROR__": str(hata),
        "__RISK__": str(riskli),
        "__RECOMMENDATIONS__": str(toplam_oneri),
        "__OPEN_PCT__": str(acik_yuzde),
        "__CLOSED_END__": str(round(acik_yuzde + kapali_yuzde, 1)),
        "__RISK_PCT__": str(yuzde(riskli)),
        "__ERROR_PCT__": str(hata_yuzde),
        "__ROWS__": satir_html
    }

    for anahtar, deger in degiskenler.items():
        html_icerik = html_icerik.replace(anahtar, deger)

    html_yolu = json_yolu.with_suffix(".html")

    with open(html_yolu, "w", encoding="utf-8") as dosya:
        dosya.write(html_icerik)

    return html_yolu


if __name__ == "__main__":
    rapor_klasoru = Path(__file__).resolve().parent / "reports"

    raporlar = sorted(
        rapor_klasoru.glob("scan_*.json"),
        key=lambda yol: yol.stat().st_mtime
    )

    if not raporlar:
        print("Henuz JSON raporu bulunamadi.")
    else:
        html_yolu = html_rapor_olustur(raporlar[-1])
        print(f"HTML raporu olusturuldu: {html_yolu}")

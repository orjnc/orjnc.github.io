import requests
import re

# --- AYARLAR ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.todtv.com.tr/",
    "Origin": "https://www.todtv.com.tr"
}

def ercdn_avla(url):
    """TOD/Ercdn sunucusundaki m3u8 linkini ve guncel tokeni yakalar."""
    try:
        print(f"🕵️ Kaynak Taraniyor: {url}")
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            # Ters slashlari temizle
            icerik = r.text.replace("\\/", "/")
            # Ercdn uzerindeki her turlu m3u8 linkini (st ve e parametreleri dahil) yakala
            match = re.search(r'["\'](https?://[a-z0-9\.-]*?ercdn\.com/[^"\']*?\.m3u8\?[^"\']*?)["\']', icerik)
            if match:
                link = match.group(1)
                print(f"✅ LINK BULUNDU: {link[:50]}...")
                return link
    except Exception as e:
        print(f"❌ Hata: {e}")
    return url

# --- KANAL LISTESI ---
kanallar = [
    {"isim": "TRT 1", "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "logo": "trt1.jpg"},
    {"isim": "Kanal D HD", "url": "https://www.todtv.com.tr/canli-tv/kanal-d", "logo": "kanald.jpg", "mod": "ercdn"},
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "tabiispor.jpg", "sabit": True},
    {"isim": "DMAX TR", "url": "https://www.dmax.com.tr/canli-izle", "logo": "dmax.jpg"},
    {"isim": "TLC TR", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "tlc.jpg"},
    {"isim": "TRT Spor", "url": "https://www.tabii.com/tr/watch/live/trtspor?trackId=150002", "logo": "trtspor.jpg"},
    {"isim": "TRT Spor Yildiz", "url": "https://www.trtspor.com.tr/canli-yayin-izle/trt-spor-yildiz", "logo": "trtsporyildiz.jpg", "ozel_yol": True},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "tabiispor.jpg"},
    {"isim": "Nickelodeon", "url": "https://www.todtv.com.tr/canli-tv/nickelodeon-sd", "logo": "nickelodeon.jpg", "mod": "ercdn"}
]

# --- PLAYLIST OLUSTURMA ---
output = "#EXTM3U\n"
for k in kanallar:
    # Link bulma
    if k.get("sabit"):
        link = k["url"]
    elif k.get("mod") == "ercdn":
        link = ercdn_avla(k["url"])
    else:
        # Genel m3u8 tarama (TRT vb. icin)
        link = ercdn_avla(k["url"])

    # Logo yolu
    if k.get("ozel_yol"):
        logo = "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"
    else:
        logo = f"https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/{k['logo']}"

    output += f'#EXTINF:-1 tvg-logo="{logo}", {k["isim"]}\n{link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(output)

print("🏁 Islem Tamam! Nickelodeon ve Kanal D 'ercdn' avcisi ile eklendi.")

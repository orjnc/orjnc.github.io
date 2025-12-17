import requests
import re

# --- AYARLAR ---
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/"
}

def link_bul(url, regex_pattern):
    try:
        print(f"Taraniyor: {url}")
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            match = re.search(regex_pattern, r.text)
            if match:
                temiz_link = match.group(1).replace("\\/", "/")
                print(f"BULUNDU: {temiz_link}")
                return temiz_link
    except Exception as e:
        print(f"Hata: {e}")
    return None

# --- KANAL LISTESI ---
kanallar = [
    # 1. TRT 1 (Kucuk harf: trt1.jpg)
    {
        "isim": "TRT 1",
        "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002",
        "regex": r'["\'](https:[^"\']*?trt1[^"\']*?\.m3u8[^"\']*?)["\']', 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"
    },
    # 2. TRT SPOR (Kucuk harf: trtspor.jpg)
    {
        "isim": "TRT Spor",
        "url": "https://www.tabii.com/tr/watch/live/trtspor?trackId=150002",
        "regex": r'["\'](https:[^"\']*?trtspor[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"
    },
    # 3. TRT SPOR YILDIZ (Senin verdigin OZEL LINK)
    {
        "isim": "TRT Spor Yildiz",
        "url": "https://www.trtspor.com.tr/canli-yayin-izle/trt-spor-yildiz",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        # DIKKAT: Verdigin ozel linki birebir kullandim:
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"
    },
    # 4. TABII SPOR (Kucuk harf: tabiispor.jpg)
    {
        "isim": "Tabii Spor",
        "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"
    },
    # 5. DMAX (Kucuk harf: dmax.jpg)
    {
        "isim": "DMAX TR",
        "url": "https://www.dmax.com.tr/canli-izle",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"
    },
    # 6. TLC (Kucuk harf: tlc.jpg)
    {
        "isim": "TLC TR",
        "url": "https://www.tlctv.com.tr/canli-izle",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"
    },
    # 7. TABII COCUK (Kucuk harf: tabiicocuk.jpg)
    {
        "isim": "Tabii Cocuk",
        "url": "https://www.tabii.com/tr/watch/live/tabii-cocuk?trackId=516992",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiicocuk.jpg"
    }
]

# --- KAYDETME ---
dosya_icerigi = "#EXTM3U\n"

for k in kanallar:
    canli_link = link_bul(k["url"], k["regex"])
            
    if canli_link:
        dosya_icerigi += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)

print("Liste guncellendi: Kucuk harf kuralina uyuldu.")

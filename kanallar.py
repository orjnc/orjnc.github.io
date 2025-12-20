import requests
import re
import json

def link_yakala(url):
    # Eğer link zaten doğrudan m3u8 ise dokunma
    if ".m3u8" in url and "atv" not in url and "startv" not in url:
        return url
        
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": url,
            "Accept": "*/*"
        }

        # --- ÖZEL API SÖKÜCÜLER (ATV, STAR, KANAL 7 GİBİLER İÇİN) ---
        # Bu kısım sitenin içindeki gizli API dosyalarına sızar
        if "atv.com.tr" in url:
            # TMGrup (ATV, A2 vb.) için gizli token API'si
            api_r = requests.get("https://v.tmgrup.com.tr/getv_test?atv", headers=headers, timeout=10)
            atv_match = re.search(r'["\'](https?://.*?\.m3u8.*?)["\']', api_r.text.replace("\\/", "/"))
            if atv_match: return atv_match.group(1)
            return "https://atv-live.daioncdn.net/atv/atv.m3u8" # Yedek link

        if "startv.com.tr" in url:
            # Star TV / Doğuş Grubu CDN yolu
            return "https://dogus-live.daioncdn.net/startv/startv.m3u8"

        if "kanal7.com" in url:
            # Kanal 7 CDN yolu
            return "https://kanal7-live.daioncdn.net/kanal7/kanal7.m3u8"

        # --- GENEL DERİN TARAMA ---
        r = requests.get(url, headers=headers, timeout=15)
        # Unicode ve kaçış karakterlerini temizle (\/ -> /)
        icerik = r.text.replace("\\/", "/").replace("\\\\", "\\")
        
        # Regex 1: Standart tırnak içi m3u8 araması
        match = re.search(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', icerik)
        if match:
            link = match.group(1)
            if "ads" not in link.lower() and "vpaid" not in link.lower():
                return link

        # Regex 2: JSON içindeki gizli 'src' veya 'url' değerlerini bulma
        json_pattern = r'(?:src|url|file|videoUrl)["\']?\s*[:=]\s*["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']'
        json_match = re.search(json_pattern, icerik, re.IGNORECASE)
        if json_match:
            return json_match.group(1)

    except Exception as e:
        print(f"Hata ({url}): {e}")
        
    return url

# --- KANAL LİSTESİ ---
kanallar = [
    {"isim": "TRT 1", "url": "https://trt.daioncdn.net/trt-1/master.m3u8?app=web", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"},
    {"isim": "ATV", "url": "https://www.atv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/atv.jpg"},
    {"isim": "Kanal D", "url": "https://www.kanald.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg"},
    {"isim": "Star TV", "url": "https://www.startv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/star.jpg"},
    {"isim": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/showtv.jpg"},
    {"isim": "NOW TV", "url": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/now.jpg"},
    {"isim": "TV8", "url": "https://tv8.daioncdn.net/tv8/tv8.m3u8?app=7ddc255a-ef47-4e81-ab14-c0e5f2949788&ce=3", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tv8.jpg"},
    {"isim": "Beyaz TV", "url": "https://www.beyaztv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/beyaztv.jpg"},
    {"isim": "Teve2", "url": "https://www.teve2.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/teve2.jpg"},
    {"isim": "Kanal 7", "url": "https://www.kanal7.com/canli-izle/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanal7.jpg"},
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"},
    {"isim": "DMAX TR", "url": "https://www.dmax.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"},
    {"isim": "TLC TR", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"},
    {"isim": "TRT Spor", "url": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"},
    {"isim": "TRT Spor Yildiz", "url": "https://tv-trtspor2.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"}
]

m3u_icerik = "#EXTM3U\n"
print("📡 Evrensel Avcı başlatıldı. Kanallar sökülüyor...")

for k in kanallar:
    canli_link = link_yakala(k["url"])
    m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'
    print(f"✔️ {k['isim']} yakalandı: {canli_link[:50]}...")

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)

print("\n✅ İşlem başarılı! 'playlist.m3u' dosyası 'adam gibi' güncellendi.")

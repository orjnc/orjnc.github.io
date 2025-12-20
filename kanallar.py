import requests
import re
import json

def link_yakala(url):
    # Eğer link zaten doğrudan m3u8 ise dokunma
    if ".m3u8" in url and "atv" not in url and "startv" not in url:
        return url
        
    try:
        # Gerçek bir tarayıcı gibi davranmak için gelişmiş başlıklar
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": url,
            "Accept": "*/*"
        }
        
        r = requests.get(url, headers=headers, timeout=15)
        icerik = r.text
        
        # 1. YÖNTEM: Unicode ve Ters Bölü (\/) Temizliği yaparak m3u8 arama
        # Bu yöntem Star, ATV ve Kanal 7'nin gizlediği linkleri bulur
        icerik_temiz = icerik.replace("\\/", "/").replace("\\\\", "\\")
        
        # Regex: Tırnak içindeki m3u8 linklerini her türlü karakterle yakalar
        match = re.search(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', icerik_temiz)
        
        if match:
            link = match.group(1)
            # Reklam/Vpaid linklerini ele
            if "vpaid" not in link.lower() and "ads" not in link.lower():
                return link

        # 2. YÖNTEM: Eğer yukarıdaki bulamazsa JSON içinde "videoUrl" veya "src" ara
        # Bazı siteler (TMGrup) linki JSON objesi olarak basar
        json_match = re.search(r'["\']?(?:videoUrl|src|file)["\']?\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']', icerik_temiz)
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

print("📡 Kanallar taranıyor, bu biraz sürebilir...")

for k in kanallar:
    canli_link = link_yakala(k["url"])
    m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'
    print(f"✔️ {k['isim']} tamamlandı.")

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)

print("\n✅ Tüm linkler güncellendi ve 'playlist.m3u' dosyasına kaydedildi.")

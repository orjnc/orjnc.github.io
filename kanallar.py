import requests
import re

# --- AYARLAR ---
# Bu headers, robotun kendini bir mobil tarayici (WVC gibi) tanitmasini saglar
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36",
    "Referer": "https://www.todtv.com.tr/",
    "X-Requested-With": "com.instantbits.cast.webvideo"
}

def kanald_ozel_avci(url):
    """
    Kanal D'yi TOD TV uzerinden avlamak icin en agresif tarama.
    """
    try:
        print(f"🕵️ Avlaniyor: {url}")
        # Not: Eger calismazsa buraya bir Proxy eklenebilir. 
        # Simdilik en guclu Header ile deniyoruz.
        r = requests.get(url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            # WVC'nin yaptigi gibi tum m3u8 uzantili linkleri ayikla
            # Sadece 'master.m3u8' veya 'index.m3u8' degil, her seyi dener.
            links = re.findall(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', r.text)
            
            if links:
                # Genelde TOD linkleri icinde 'stream' veya 'live' kelimesi gecer
                for link in links:
                    if "todtv" in link or "daioncdn" in link:
                        print(f"✅ HEDEF BULUNDU: {link}")
                        return link.replace("\\/", "/")
                
                # Hicbiri uymazsa ilk buldugunu ver
                return links[0].replace("\\/", "/")
    except Exception as e:
        print(f"❌ Avlama Hatasi: {e}")
    return None

# --- KANAL LISTESI ---
kanallar = [
    {"isim": "TRT 1", "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "logo": "trt1.jpg", "mod": "ara"},
    {"isim": "Kanal D HD", "url": "https://www.todtv.com.tr/canli-tv/kanal-d", "logo": "kanald.jpg", "mod": "ozel"},
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "tabiispor.jpg", "mod": "sabit"},
    {"isim": "DMAX TR", "url": "https://www.dmax.com.tr/canli-izle", "logo": "dmax.jpg", "mod": "ara"},
    {"isim": "TLC TR", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "tlc.jpg", "mod": "ara"},
    {"isim": "TRT Spor", "url": "https://www.tabii.com/tr/watch/live/trtspor?trackId=150002", "logo": "trtspor.jpg", "mod": "ara"},
    {"isim": "TRT Spor Yildiz", "url": "https://www.trtspor.com.tr/canli-yayin-izle/trt-spor-yildiz", "logo": "trtsporyildiz.jpg", "mod": "ara"},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "tabiispor.jpg", "mod": "ara"}
]

# --- KAYDETME ---
dosya_icerigi = "#EXTM3U\n"
for k in kanallar:
    # Logo Ayari
    logo_path = f"https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/{k['logo']}"
    if k['isim'] == "TRT Spor Yildiz":
        logo_path = "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"

    # Link Bulma
    if k['mod'] == "sabit":
        link = k['url']
    elif k['mod'] == "ozel":
        link = kanald_ozel_avci(k['url']) or k['url']
    else:
        # Diger kanallar icin standart arama
        link = kanald_ozel_avci(k['url']) or k['url']

    dosya_icerigi += f'#EXTINF:-1 tvg-logo="{logo_path}", {k["isim"]}\n{link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)

print("🏁 Islem Tamam!")

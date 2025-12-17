import requests
import re

# --- AYARLAR ---
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.kanald.com.tr/",
    "Origin": "https://www.kanald.com.tr"
}

def kanald_resmi_bul(url):
    try:
        print(f"🕵️ Kanal D Resmi Sitesi Taraniyor: {url}")
        r = requests.get(url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            # 1. Hamle: Sayfa icindeki m3u8 linkini ara (Genelde 'contentUrl' veya 'src' icindedir)
            # Bu regex hem normal hem de ters slashli (\/) linkleri yakalar
            match = re.search(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', r.text)
            
            if match:
                link = match.group(1).replace("\\/", "/")
                print(f"✅ KANAL D BULUNDU: {link}")
                return link
            
            # 2. Hamle: Eger ilk yontem yemezse, daha agresif ara (daioncdn veya ercdn odakli)
            agresif_match = re.search(r'(https?://[^"\'\s<>]*?(?:daioncdn|ercdn|kanald)[^"\'\s<>]*?\.m3u8[^"\'\s<>]*)', r.text)
            if agresif_match:
                link = agresif_match.group(0).replace("\\/", "/")
                print(f"✅ KANAL D BULUNDU (Agresif): {link}")
                return link
                
    except Exception as e:
        print(f"❌ Hata: {e}")
    return None

# --- KANAL LISTESI ---
kanallar = [
    # 1. TRT 1
    {"isim": "TRT 1", "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "logo": "trt1.jpg", "mod": "ara"},
    
    # 2. KANAL D HD (YENI LINK - 2. SIRA)
    {"isim": "Kanal D HD", "url": "https://www.kanald.com.tr/canli-yayin", "logo": "kanald.jpg", "mod": "kanald_ozel"},
    
    # 3. TABII TV (SABIT)
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "tabiispor.jpg", "mod": "sabit"},
    
    # DIGERLERI
    {"isim": "DMAX TR", "url": "https://www.dmax.com.tr/canli-izle", "logo": "dmax.jpg", "mod": "ara"},
    {"isim": "TLC TR", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "tlc.jpg", "mod": "ara"},
    {"isim": "TRT Spor", "url": "https://www.tabii.com/tr/watch/live/trtspor?trackId=150002", "logo": "trtspor.jpg", "mod": "ara"},
    {"isim": "TRT Spor Yildiz", "url": "https://www.trtspor.com.tr/canli-yayin-izle/trt-spor-yildiz", "logo": "trtsporyildiz.jpg", "mod": "ara"},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "tabiispor.jpg", "mod": "ara"}
]

# --- KAYDETME ---
dosya_icerigi = "#EXTM3U\n"
for k in kanallar:
    # Logo Yolu
    logo_path = f"https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/{k['logo']}"
    if k['isim'] == "TRT Spor Yildiz":
        logo_path = "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"

    # Link Belirleme
    if k['mod'] == "sabit":
        link = k['url']
    elif k['mod'] == "kanald_ozel":
        link = kanald_resmi_bul(k['url']) or k['url']
    else:
        # TRT ve Digerleri icin genel tarama fonksiyonu
        link = kanald_resmi_bul(k['url']) or k['url']

    dosya_icerigi += f'#EXTINF:-1 tvg-logo="{logo_path}", {k["isim"]}\n{link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)

print("🏁 Yeni Kanal D sitesi tarandi ve liste guncellendi!")

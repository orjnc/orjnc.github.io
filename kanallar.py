import requests
import re
import json

# --- UST DUZEY TARAYICI TAKLIDI ---
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}

def link_bul(url, tip="standart"):
    """
    Url'yi tarar. 'tip' parametresine gore basit veya derinlemesine arama yapar.
    """
    try:
        print(f"🕵️ Taraniyor ({tip}): {url}")
        r = requests.get(url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            icerik = r.text
            
            # --- YONTEM 1: Standart m3u8 Arama ---
            match = re.search(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', icerik)
            if match:
                link = match.group(1).replace("\\/", "/")
                print(f"✅ BULUNDU (Standart): {link}")
                return link
            
            # --- YONTEM 2: JSON/Script Ici Derin Arama (Kanal D/TOD Icin) ---
            if tip == "derin":
                print("⏳ Derin analiz (JSON/Script) yapiliyor...")
                # Genelde player config icinde 'file': '...', 'src': '...' gibi saklanir
                # Tokenli ve uzun linkleri yakalamak icin genis regex
                # Ornek: "secureUrl":"https://..." veya file:"https://..."
                
                # Regex: tırnak icinde http ile baslayip m3u8 ile biten her sey
                gizli_matchler = re.findall(r'(https?://[^"\'\s<>]*?\.m3u8[^"\'\s<>]*)', icerik)
                
                if gizli_matchler:
                    # En uzun link genelde en dogru/kaliteli olandir
                    en_iyi_link = max(gizli_matchler, key=len).replace("\\/", "/")
                    print(f"✅ BULUNDU (Derin Analiz): {en_iyi_link}")
                    return en_iyi_link
                    
    except Exception as e:
        print(f"❌ Hata: {e}")
    return None

# --- KANAL LISTESI ---
kanallar = [
    # 1. TRT 1
    {
        "isim": "TRT 1",
        "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002",
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg",
        "mod": "standart"
    },
    # 2. KANAL D HD (TOD TV - DERIN ANALIZ MODU)
    {
        "isim": "Kanal D HD",
        "url": "https://www.todtv.com.tr/canli-tv/kanal-d",
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg",
        "mod": "derin" # Ozel mod aktif
    },
    # 3. TABII TV (SABIT)
    {
        "isim": "Tabii TV",
        "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8",
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg",
        "mod": "sabit" 
    },
    # 4. DMAX
    {
        "isim": "DMAX TR",
        "url": "https://www.dmax.com.tr/canli-izle",
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg",
        "mod": "standart"
    },
    # 5. TLC
    {
        "isim": "TLC TR",
        "url": "https://www.tlctv.com.tr/canli-izle",
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg",
        "mod": "standart"
    },
    # 6. TRT SPOR
    {
        "isim": "TRT Spor",
        "url": "https://www.tabii.com/tr/watch/live/trtspor?trackId=150002",
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg",
        "mod": "standart"
    },
    # 7. TRT SPOR YILDIZ
    {
        "isim": "TRT Spor Yildiz",
        "url": "https://www.trtspor.com.tr/canli-yayin-izle/trt-spor-yildiz",
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg",
        "mod": "standart"
    },
    # 8. TABII SPOR
    {
        "isim": "Tabii Spor",
        "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002",
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg",
        "mod": "standart"
    }
]

# --- KAYDETME ---
dosya_icerigi = "#EXTM3U\n"

for k in kanallar:
    canli_link = None
    
    # Moduna gore islem yap
    if k.get("mod") == "sabit":
        canli_link = k["url"]
        print(f"SABIT EKLENDI: {k['isim']}")
    else:
        # Standart veya Derin analiz yap
        canli_link = link_bul(k["url"], k["mod"])
            
    # Link bulunamazsa bile site adresini yaz (Listede gozuksun)
    if not canli_link:
        print(f"⚠️ {k['isim']} linki bulunamadi. Web adresi yaziliyor.")
        canli_link = k["url"]
            
    dosya_icerigi += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)

print("🚀 Liste guncellendi: Kanal D icin Derin Analiz Modu kullanildi.")

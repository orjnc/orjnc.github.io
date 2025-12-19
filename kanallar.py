import requests
import re

# BBC First için senin mantığına uygun sökücü
def bbc_ozel_yakala():
    target_url = "https://www.todtv.com.tr/canli-tv/bbc-first"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.153 Mobile Safari/537.36", "X-Requested-With": "com.instantbits.cast.webvideo"}
    try:
        r = requests.get(target_url, headers=headers, timeout=10)
        match = re.search(r'["\'](https?://dt-live-bc\.ercdn\.com/bc/bbcfirst/[^"\']*?\.m3u8[^"\']*?)["\']', r.text.replace("\\/", "/"))
        if match: return match.group(1)
    except: pass
    return "Link Bulunamadi"

def link_yakala(url):
    # Link zaten m3u8 ise (Tabii TV gibi) dokunma
    if ".m3u8" in url:
        return url
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        r = requests.get(url, headers=headers, timeout=10)
        # Sayfadaki m3u8 linkini çek (Kanal D ve diğerleri için)
        match = re.search(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', r.text.replace("\\/", "/"))
        if match:
            return match.group(1)
    except:
        pass
    return url

# --- SENİN ÇALIŞAN LİSTEN (HİÇBİR URL DEĞİŞMEDİ) ---
kanallar = [
    {
        "isim": "TRT 1", 
        "url": "https://trt.daioncdn.net/trt-1/master.m3u8?app=web", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"
    },
    {
        "isim": "Kanal D HD", 
        "url": "https://www.kanald.com.tr/canli-yayin", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg"
    },
    {
        "isim": "Tabii TV", 
        "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"
    },
    {
        "isim": "BBC First", 
        "url": "https://www.todtv.com.tr/canli-tv/bbc-first", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/bbcfirst.jpg"
    },
    {
        "isim": "DMAX TR", 
        "url": "https://www.dmax.com.tr/canli-izle", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"
    },
    {
        "isim": "TLC TR", 
        "url": "https://www.tlctv.com.tr/canli-izle", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"
    },
    {
        "isim": "TRT Spor", 
        "url": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"
    },
    {
        "isim": "TRT Spor Yildiz", 
        "url": "https://tv-trtspor2.medya.trt.com.tr/master.m3u8", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"
    },
    {
        "isim": "Tabii Spor", 
        "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"
    }
]

m3u_icerik = "#EXTM3U\n"

for k in kanallar:
    if k["url"] == "BBC_OZEL":
        canli_link = bbc_ozel_yakala()
    else:
        canli_link = link_yakala(k["url"])
    m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)

print("✅ Senin çalışan listen BBC eklenerek güncellendi.")

import time
import requests
import re
from playwright.sync_api import sync_playwright

def eski_yontem_link(url):
    """Senin hızlı regex yöntemin - Daioncdn ve Parametre önceliği eklendi"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": url
        }
        r = requests.get(url, headers=headers, timeout=10)
        text = r.text.replace("\\/", "/")
        matches = re.findall(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', text)
        
        if matches:
            # ÖNCELİK 1: Hem daioncdn olan hem de token/reklam kimliği (st, dfp, ppid) içeren link
            for m in matches:
                if "daioncdn" in m and any(x in m for x in ["st=", "dfp", "ppid", "app="]):
                    return m
            # ÖNCELİK 2: Sadece daioncdn olan link
            for m in matches:
                if "daioncdn" in m:
                    return m
            # VARSAYILAN: Hiçbiri yoksa ilk bulduğun m3u8 (Eski sistemin)
            return matches[0]
    except: pass
    return None

def tarayici_link_yakala(context, kanal_adi, url):
    """Playwright Yakalayıcı - En iyi linki (daioncdn) bulana kadar seçim yapar"""
    page = context.new_page()
    bulunan_link = [url]

    def istek_kontrol(request):
        u = request.url
        # .m3u8 kontrolü ve reklam/izleme linklerini eleme
        if ".m3u8" in u.lower() and not any(x in u.lower() for x in ["ads", "vpaid", "telemetry", "moat"]):
            
            # MAKİNE BURADA KARAR VERİYOR:
            # Yeni gelen link "Altın Link" kriterlerine (daioncdn + parametre) uyuyor mu?
            yeni_link_kaliteli = "daioncdn" in u and any(x in u for x in ["st=", "dfp", "ppid", "app="])
            mevcut_link_kaliteli = "daioncdn" in bulunan_link[0] and "st=" in bulunan_link[0]

            if yeni_link_kaliteli:
                # En iyi linki bulduk, bunu kaydet
                bulunan_link[0] = u
            elif "daioncdn" in u and not mevcut_link_kaliteli:
                # Mevcut link sıradan ama yeni gelen daioncdn ise onu al
                bulunan_link[0] = u
            elif bulunan_link[0] == url:
                # Henüz hiçbir şey bulunmadıysa ilk m3u8'i kaydet
                bulunan_link[0] = u

    page.on("request", istek_kontrol)
    try:
        # Sayfanın tamamen yüklenmesini ve tüm tokenların akmasını bekliyoruz
        page.goto(url, wait_until="networkidle", timeout=45000)
        time.sleep(5) # Asıl yayın linkinin düşmesi için ekstra zaman
    except: pass
    page.close()
    return bulunan_link[0]

# --- KANAL LİSTESİ VE ANA DÖNGÜ (Burası senin verdiğin iskeletle birebir aynı) ---
kanallar = [
    {"isim": "TRT 1", "url": "https://trt.daioncdn.net/trt-1/master.m3u8?app=web", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"},
    {"isim": "ATV", "url": "https://www.atv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/atv.jpg"},
    {"isim": "Kanal D", "url": "https://www.kanald.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg"},
    {"isim": "Star TV", "url": "https://www.startv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/star.jpg"},
    {"isim": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/showtv.jpg"},
    {"isim": "NOW TV", "url": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/now.jpg"},
    {"isim": "TV8", "url": "https://www.tv8.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tv8.jpg"},
    {"isim": "Beyaz TV", "url": "https://www.beyaztv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/beyaztv.jpg"},
    {"isim": "Teve2", "url": "https://www.teve2.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/teve2.jpg"},
    {"isim": "360", "url": "https://www.tv360.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/360.jpg"},
    {"isim": "a2", "url": "https://www.atv.com.tr/a2tv/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/a2.jpg"},
    {"isim": "Kanal 7", "url": "https://www.kanal7.com/canli-izle/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanal7.jpg"},
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"},
    {"isim": "FX", "url": "https://saran-live.ercdn.net/fx/index.m3u8?checkedby:iptvcat.com", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/fx.jpg"},
    {"isim": "DMAX", "url": "https://www.dmax.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"},
    {"isim": "TLC", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"},
    {"isim": "CNBC-e", "url": "https://www.cnbce.com/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/cnbce.jpg"},
    {"isim": "TRT Spor", "url": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"},
    {"isim": "TRT Spor Yildiz", "url": "https://tv-trtspor2.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"}
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    m3u_icerik = "#EXTM3U\n"
    for k in kanallar:
        canli_link = eski_yontem_link(k["url"])
        if not canli_link or ".m3u8" not in canli_link:
            canli_link = tarayici_link_yakala(context, k["isim"], k["url"])
        
        # Referer Ayarı
        if "atv" in k["url"] or "a2tv" in k["url"]: ref = "https://www.atv.com.tr/"
        elif "cnbce" in k["url"]: ref = "https://www.cnbce.com/"
        else: ref = k["url"]

        if any(x in canli_link for x in ["trt.daioncdn", "medya.trt.com.tr", "erbvr.com"]):
             m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'
        else:
             m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}|User-Agent=Mozilla/5.0&Referer={ref}\n'
        
        print(f"✅ {k['isim']} bitti.")
    
    browser.close()

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)
    

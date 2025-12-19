import requests
import re
import os

# --- 1. ADIM: GİZLİ BİLGİLERİ AL ---
USER_EMAIL = os.getenv('TOD_EMAIL')
USER_PASS = os.getenv('TOD_PASSWORD')

# --- 2. ADIM: TEK BİR OTURUM BAŞLAT ---
def oturum_hazirla():
    session = requests.Session()
    login_url = "https://www.todtv.com.tr/api/login"
    payload = {"username": USER_EMAIL, "password": USER_PASS, "rememberMe": True}
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Referer": "https://www.todtv.com.tr/giris"
    }
    try:
        r = session.post(login_url, json=payload, headers=headers, timeout=15)
        if r.status_code == 200:
            print("✅ Oturum başarıyla açıldı.")
            return session
    except:
        pass
    print("⚠️ Oturum açılamadı, standart modda devam ediliyor.")
    return requests # Oturum açılmazsa normal requests moduna döner

# --- 3. ADIM: HER KANALI SÖKEN GENEL FONKSİYON ---
def kanal_sokucu(url, baglanti):
    # Eğer link zaten m3u8 ise dokunma (TRT'ler gibi)
    if ".m3u8" in url:
        return url
    
    try:
        # Bu kısım her kanalda senin oturumunu (session) kullanır
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "X-Requested-With": "com.instantbits.cast.webvideo"
        }
        r = baglanti.get(url, headers=headers, timeout=10)
        
        # Sayfadaki m3u8 linkini çek (Kanal D, BBC, DMAX hepsi burada taranır)
        match = re.search(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', r.text.replace("\\/", "/"))
        if match:
            return match.group(1)
    except:
        pass
    return url

# --- 4. ADIM: SENİN ÇALIŞAN LİSTEN ---
kanallar = [
    {"isim": "TRT 1", "url": "https://trt.daioncdn.net/trt-1/master.m3u8?app=web", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"},
    {"isim": "Kanal D HD", "url": "https://www.kanald.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg"},
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"},
    {"isim": "BBC First", "url": "https://www.todtv.com.tr/canli-tv/bbc-first", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/bbcfirst.jpg"},
    {"isim": "DMAX TR", "url": "https://www.dmax.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"},
    {"isim": "TLC TR", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"},
    {"isim": "TRT Spor", "url": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"},
    {"isim": "TRT Spor Yildiz", "url": "https://tv-trtspor2.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"}
]

# --- 5. ADIM: İŞLEME VE KAYDETME ---
aktif_baglanti = oturum_hazirla()
m3u_icerik = "#EXTM3U\n"

for k in kanallar:
    # Her kanal için aynı sökücü çalışır
    canli_link = kanal_sokucu(k["url"], aktif_baglanti)
    m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)

print("✅ Her kanal oturum desteğiyle tarandı ve liste güncellendi.")

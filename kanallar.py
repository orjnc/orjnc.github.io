import requests
import re
import os

# --- 1. ADIM: GİZLİ BİLGİLER ---
USER_EMAIL = os.getenv('TOD_EMAIL')
USER_PASS = os.getenv('TOD_PASSWORD')

# --- 2. ADIM: GELİŞMİŞ OTURUM YÖNETİMİ ---
def oturum_hazirla():
    session = requests.Session()
    try:
        # Önce çerezleri almak için giriş sayfasına vur
        ana_sayfa = "https://www.todtv.com.tr/giris"
        headers_ilk = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        session.get(ana_sayfa, headers=headers_ilk, timeout=10)
        
        login_url = "https://www.todtv.com.tr/api/v1/login" 
        payload = {"email": USER_EMAIL, "password": USER_PASS, "rememberMe": True}
        headers_login = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Referer": "https://www.todtv.com.tr/giris",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        r = session.post(login_url, json=payload, headers=headers_login, timeout=15)
        if r.status_code == 200:
            print("✅ GİRİŞ BAŞARILI.")
            return session
    except:
        pass
    print("⚠️ Oturum açılamadı, misafir modunda devam ediliyor.")
    return None

# --- 3. ADIM: HER KANALI SÖKEN GENEL FONKSİYON ---
def kanal_sokucu(url, session):
    if ".m3u8" in url:
        return url
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        # Eğer oturum varsa onunla, yoksa standart requests ile sayfayı al
        if session:
            r = session.get(url, headers=headers, timeout=10)
        else:
            r = requests.get(url, headers=headers, timeout=10)
            
        text = r.text.replace("\\/", "/")
        match = re.search(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', text)
        if match:
            return match.group(1)
    except:
        pass
    return url

# --- 4. ADIM: SENİN EKSİKSİZ TAM LİSTEN ---
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

# --- 5. ADIM: İŞLEME ---
aktif_session = oturum_hazirla()
m3u_icerik = "#EXTM3U\n"

for k in kanallar:
    canli_link = kanal_sokucu(k["url"], aktif_session)
    m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)

print("✅ Liste TAM HALİYLE güncellendi.")

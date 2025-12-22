// TÜM ÖNERİLER BURADA TOPLANIYOR
const oneriListesi = [
    {
        title: "UZAK ŞEHİR",
        desc: "Bu Akşam 20:00'da Kanal D'de!",
        image: "https://i.imgur.com/reWzIZ1.jpeg", 
        targetChannel: "Kanal D"
    },
    {
        title: "BERGEN",
        desc: "Bu Akşam 20:00'da ATV'de!",
        image: "https://i.imgur.com/jnhG97F.jpeg", 
        targetChannel: "ATV"
    },
    {
        title: "MASTERCHEF",
        desc: "20:00'da Yeni Bölüm Heyecanı Başlıyor!",
        image: "https://i.imgur.com/ebSpKg0.jpeg",
        targetChannel: "TV8"
    }
];

let aktifSira = 0;
let slideInterval;

function setupFeatured() {
    const card = document.getElementById('featured-card');
    const title = document.getElementById('featured-title');
    const desc = document.getElementById('featured-desc');

    if (!card || oneriListesi.length === 0) return;

    // Listeden sıradaki veriyi al
    const veri = oneriListesi[aktifSira];

    // Fade efekti için hafifçe şeffaflaştır (Opsiyonel)
    card.style.opacity = "0.8";

    setTimeout(() => {
        title.innerText = veri.title;
        desc.innerText = veri.desc;
        card.style.backgroundImage = `linear-gradient(to bottom, transparent, rgba(0,0,0,0.9)), url('${veri.image}')`;
        card.style.backgroundSize = "cover";
        card.style.backgroundPosition = "center";
        card.style.opacity = "1";
    }, 300);

    // Bir sonraki sefere diğerine geç (Döngü)
    aktifSira = (aktifSira + 1) % oneriListesi.length;
}

function playFeatured() {
    // Tıklandığında o an ekranda hangi veri varsa (bir önceki index) onu açar
    let suAnkiIndex = (aktifSira === 0) ? oneriListesi.length - 1 : aktifSira - 1;
    const veri = oneriListesi[suAnkiIndex];
    
    // allChannels index.html'de global olduğu için burada çalışır
    const channel = allChannels.find(k => k.ad === veri.targetChannel);
    if (channel) {
        playChannel(channel.url, channel.ad, false, channel.kategori);
    }
}

// Başlatma
document.addEventListener('DOMContentLoaded', () => {
    // 1 saniye bekle ki kanallar yüklensin
    setTimeout(() => {
        setupFeatured();
        // Her 5 saniyede bir değiştir
        slideInterval = setInterval(setupFeatured, 5000);
    }, 1000);
});

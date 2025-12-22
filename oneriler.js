const oneriListesi = [
    { title: "UZAK ŞEHİR", desc: "Bu Akşam 20:00'da Kanal D'de!", image: "https://i.imgur.com/NKiF8WO.jpeg", targetChannel: "Kanal D" },
    { title: "BERGEN", desc: "Bu Akşam 20:00'da ATV'de!", image: "https://i.imgur.com/LNW86ek.jpeg", targetChannel: "ATV" },
    { title: "MASTERCHEF", desc: "20:00'da Yeni Bölüm Heyecanı Başlıyor!", image: "https://i.imgur.com/wAX4TER.jpeg", targetChannel: "TV8" }
];

let aktifSira = 0;

// Kartları ilk kez DOM'a basan fonksiyon
function initPromo() {
    const container = document.getElementById('promo-inner-container');
    if (!container) return;

    container.innerHTML = oneriListesi.map((item, index) => `
        <div class="promo-card ${index === 0 ? 'active' : ''}" 
             onclick="playFeatured(${index})"
             style="background-image: url('${item.image}')">
            <div>
                <h3 class="m-0" style="font-weight: 800;">${item.title}</h3>
                <div class="d-flex gap-2 mt-2 align-items-center">
                    <span class="badge bg-danger">LIVE</span>
                    <span class="small" style="opacity: 0.9;">${item.desc}</span>
                </div>
            </div>
        </div>
    `).join('');
    
    updateSlider();
}

// Kaydırma ve Odaklanma işlemini yapan fonksiyon
function updateSlider() {
    const container = document.getElementById('promo-inner-container');
    const cards = document.querySelectorAll('.promo-card');
    if (!container || cards.length === 0) return;

    cards.forEach((card, idx) => {
        card.classList.toggle('active', idx === aktifSira);
    });

    // Apple TV tarzı merkeze hizalama hesaplaması
    const card = cards[aktifSira];
    const containerWidth = document.getElementById('promo-slider').offsetWidth;
    const cardWidth = card.offsetWidth;
    const cardOffset = card.offsetLeft;

    // Kartı ekranın ortasına getirecek olan X mesafesini hesapla
    const moveX = (containerWidth / 2) - (cardWidth / 2) - cardOffset;

    container.style.transform = `translateX(${moveX}px)`;
}

// Otomatik geçiş için
function nextPromo() {
    aktifSira = (aktifSira + 1) % oneriListesi.length;
    updateSlider();
}

// Kart tıklandığında veya kanal açılmak istendiğinde
function playFeatured(index = null) {
    // Eğer dışarıdan index gelirse (kart tıklaması) o sıraya git
    if (index !== null) {
        if (aktifSira === index) {
            // Zaten o karttaysak kanalı aç
            const veri = oneriListesi[aktifSira];
            const channel = allChannels.find(k => k.ad === veri.targetChannel);
            if (channel) playChannel(channel.url, channel.ad, false, channel.kategori);
        } else {
            // O karta odaklan
            aktifSira = index;
            updateSlider();
        }
        return;
    }

    // featured-card id'li eski yapıdan çağrılırsa direkt aktif olanı aç
    const veri = oneriListesi[aktifSira];
    const channel = allChannels.find(k => k.ad === veri.targetChannel);
    if (channel) playChannel(channel.url, channel.ad, false, channel.kategori);
}

// Başlatıcı
document.addEventListener('DOMContentLoaded', () => {
    // Kanalların yüklenmesi için kısa bir bekleme
    setTimeout(() => {
        initPromo();
        setInterval(nextPromo, 5000); // 5 saniyede bir kaydır
    }, 1000);
});

// Ekran boyutu değişirse hizalamayı düzelt
window.addEventListener('resize', updateSlider);

# 🎬 Film Önerisi ve Yorum Analizi Projesi

Kullanıcıların tercihlerine göre film önerileri sunan ve filmlerin yorumlarını sentiment analizi ile değerlendiren web uygulaması.

## 📋 İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Özellikler](#özellikler)
- [Teknolojiler](#teknolojiler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [API Dokümantasyonu](#api-dokümantasyonu)
- [Ekran Görüntüleri](#ekran-görüntüleri)
- [Sorun Giderme](#sorun-giderme)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

## 🎯 Proje Hakkında

Bu proje, kullanıcıların film tercihlerine göre özelleştirilmiş öneriler sunan ve yapay zeka destekli yorum analizi yapan bir web uygulamasıdır. TMDB (The Movie Database) API'sini kullanarak gerçek film verilerini çeker ve TextBlob kütüphanesi ile sentiment analizi yapar.

### Proje Amacı

- Kullanıcılara kişiselleştirilmiş film önerileri sunmak
- Film yorumlarını otomatik olarak analiz ederek olumlu, nötr ve olumsuz şeklinde sınıflandırmak
- Modern ve kullanıcı dostu bir arayüz sunmak

## ✨ Özellikler

### 🎭 Film Filtreleme
- **Çoklu Tür Seçimi**: Aksiyon, Komedi, Romantik, Korku, Bilim Kurgu, Drama, Animasyon
- **Film Uzunluğu**: 60 dk'dan kısa, 60-90 dk, 90-120 dk, 120+ dk
- **Yönetmen Seçimi**: Ünlü yönetmenler veya diğer yönetmenler
- **Çıkış Tarihi**: 1950 öncesi, 1950-1975, 1975-2000, 2000-2010, 2010 sonrası
- **Hedef Kitle**: Çocuk, Yetişkin, Genel

### 🌟 Film Önerileri
- Her aramada farklı 3 film önerisi
- Filtre seçmeden de rastgele film önerisi
- Her tıklamada yeni ve farklı filmler
- Yüksek kaliteli film posterleri
- Detaylı film bilgileri (tür, süre, yönetmen, yıl)
- TMDB'den gerçek veriler

### 💬 Yorum Analizi
- Gerçek kullanıcı yorumları (TMDB API)
- Sentiment analizi (Olumlu/Nötr/Olumsuz)
- Emoji ile görsel geri bildirim
- İngilizce ve Türkçe yorum desteği

### 🎨 Kullanıcı Arayüzü
- Modern ve responsive tasarım
- Gradient renkler ve animasyonlar
- Kolay navigasyon
- Mobil uyumlu

## 🛠 Teknolojiler

### Frontend
- **HTML5**: Yapısal içerik
- **CSS3**: Stil ve animasyonlar
- **JavaScript (Vanilla)**: Dinamik etkileşim
- **Fetch API**: Backend iletişimi

### Backend
- **Python 3.7+**: Ana programlama dili
- **Flask 2.3.0**: Web framework
- **Flask-CORS**: CORS politikası yönetimi
- **Requests**: HTTP istekleri
- **TextBlob**: Sentiment analizi

### API
- **TMDB API**: Film verileri ve yorumlar

## 📦 Kurulum

### Gereksinimler

- Python 3.7 veya üzeri
- pip (Python paket yöneticisi)
- TMDB API Key (ücretsiz)

### 1. TMDB API Key Alma

1. [TMDB](https://www.themoviedb.org/) web sitesine gidin
2. Ücretsiz hesap oluşturun
3. Settings → API → "Request an API Key" tıklayın
4. "Developer" seçeneğini seçin
5. Proje bilgilerini doldurun
6. API Key'inizi kopyalayın

### 2. Proje Dosyalarını İndirme

```bash
# Proje klasörü oluşturun
mkdir film-oneri-projesi
cd film-oneri-projesi

# Backend klasörü
mkdir backend
cd backend

# Frontend klasörü
cd ..
mkdir frontend
```

### 3. Backend Kurulumu

```bash
# Backend klasörüne gidin
cd backend

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# app.py dosyasını düzenleyin ve API Key'inizi ekleyin
# TMDB_API_KEY = 'SIZIN_API_KEY_BURADA'
```

**requirements.txt içeriği:**
```
flask==2.3.0
flask-cors==4.0.0
requests==2.31.0
textblob==0.17.1
```

### 4. Frontend Kurulumu

Frontend için özel bir kurulum gerekmez. `index.html` dosyasını `frontend` klasörüne kopyalamanız yeterlidir.

## 🚀 Kullanım

### Backend Başlatma

```bash
# Backend klasöründe
cd backend
python app.py
```

Terminal çıktısı:
```
==================================================
🎬 Film Önerisi API Başlatılıyor...
==================================================
✅ Backend: http://localhost:5000
⚠️  TMDB API Key'inizi app.py dosyasına eklemeyi unutmayın!
==================================================
```

### Frontend Başlatma

**Seçenek 1: Tarayıcıda Doğrudan Açma**
```bash
# Frontend klasöründe index.html dosyasını çift tıklayın
```

**Seçenek 2: HTTP Server ile (Önerilen)**
```bash
# Frontend klasöründe
python -m http.server 8000

# Tarayıcıda açın: http://localhost:8000
```

### Uygulama Kullanımı

1. **Ana sayfada filtreleri seçin (opsiyonel)**
   - İstediğiniz kadar tür, süre, yönetmen seçebilirsiniz
   - Hiç filtre seçmeden de rastgele film önerisi alabilirsiniz

2. **"Film Öner" butonuna tıklayın**
   - Sistem size 3 farklı film önerisi getirecek
   - Her tıklamada farklı filmler gelecek
   - Her film için detaylı bilgiler gösterilecek

3. **"Yorumları Gör" butonuna tıklayın**
   - Filmin yorumlarını göreceksiniz
   - Her yorumun sentiment analizi (Olumlu/Nötr/Olumsuz) yapılacak

4. **"Geri Dön" veya "Önerilere Dön" ile navigasyon yapın**

**💡 İpucu:** Aynı filtreleri seçseniz bile her seferinde farklı filmler gelir!

## 📚 API Dokümantasyonu

### Endpoint'ler

#### 1. Film Önerisi Al

**URL:** `POST /api/recommend`

**Request Body:**
```json
{
  "genres": ["aksiyon", "bilim-kurgu"],
  "durations": ["90-120", "120+"],
  "directors": ["Christopher Nolan"],
  "releaseDates": ["2010+"],
  "audiences": ["yetiskin"]
}
```

**Response:**
```json
[
  {
    "id": "27205",
    "title": "Inception",
    "genre": "Aksiyon, Bilim Kurgu, Gizem",
    "duration": 148,
    "director": "Christopher Nolan",
    "year": 2010,
    "audience": "yetiskin",
    "poster": "https://image.tmdb.org/t/p/w500/...",
    "overview": "Film açıklaması..."
  }
]
```

#### 2. Film Yorumlarını Al

**URL:** `GET /api/reviews/{movie_id}`

**Response:**
```json
[
  {
    "text": "This movie was absolutely fantastic!",
    "sentiment": "positive"
  },
  {
    "text": "It was okay, nothing special.",
    "sentiment": "neutral"
  },
  {
    "text": "Very disappointing film.",
    "sentiment": "negative"
  }
]
```

#### 3. API Test

**URL:** `GET /api/test`

**Response:**
```json
{
  "status": "OK",
  "message": "Backend çalışıyor!"
}
```

## 🖼 Ekran Görüntüleri

### Ana Sayfa - Filtre Ekranı
Kullanıcıların tercihlerini seçtiği ana ekran. Çoklu seçim imkanı sunar.

### Film Önerileri Sayfası
Filtrelere göre önerilen 3 film, posterler ve detaylı bilgilerle gösterilir.

### Yorumlar Sayfası
Seçilen filme ait yorumlar ve her yorumun sentiment analizi sonucu görüntülenir.

## 🔧 Sorun Giderme

### Problem: "CORS hatası" alıyorum

**Çözüm:**
- Backend sunucusunun çalıştığından emin olun
- `flask-cors` paketinin yüklü olduğunu kontrol edin:
  ```bash
  pip install flask-cors
  ```

### Problem: "API Key hatası" alıyorum

**Çözüm:**
- `app.py` dosyasında API key'inizi doğru yazdığınızdan emin olun
- TMDB hesabınızın aktif olduğunu kontrol edin
- API key'de boşluk veya özel karakter olmadığından emin olun

### Problem: "Film bulunamadı" hatası

**Çözüm:**
- Daha az kısıtlayıcı filtreler seçin
- En az bir filtre seçtiğinizden emin olun
- İnternet bağlantınızı kontrol edin

### Problem: "Backend bağlantısı kurulamadı"

**Çözüm:**
- Backend'in port 5000'de çalıştığını kontrol edin:
  ```bash
  netstat -an | grep 5000
  ```
- Firewall ayarlarınızı kontrol edin
- `localhost` yerine `127.0.0.1` deneyin

### Problem: Yorumlar yüklenmiyor

**Çözüm:**
- TMDB API limitlerinizi kontrol edin (günde 40,000 istek)
- Bazı filmler için yorum olmayabilir, bu normal bir durumdur
- Backend konsol loglarını kontrol edin

### Problem: Sentiment analizi yanlış sonuç veriyor

**Çözüm:**
- TextBlob kütüphanesi İngilizce metinlerde daha başarılıdır
- Türkçe yorumlar için anahtar kelime tabanlı analiz kullanılır
- Daha gelişmiş modeller için BERT benzeri modeller eklenebilir

## 🏗 Proje Yapısı

```
film-oneri-projesi/
│
├── README.md                      # Bu dosya
│
├── backend/
│   ├── app.py                    # Flask ana sunucu
│   ├── sentiment_analyzer.py     # Sentiment analizi modülü
│   └── requirements.txt          # Python bağımlılıkları
│
└── frontend/
    └── index.html                # Web arayüzü (HTML+CSS+JS)
```

## 🔄 Geliştirme Önerileri

### Potansiyel İyileştirmeler

1. **Veritabanı Entegrasyonu**
   - Kullanıcı favorileri
   - İzleme geçmişi
   - Kişiselleştirilmiş öneriler

2. **Gelişmiş Sentiment Analizi**
   - BERT modeli kullanımı
   - Türkçe özel model
   - Daha detaylı duygusal analiz (mutlu, üzgün, kızgın vb.)

3. **Kullanıcı Yönetimi**
   - Kayıt/Giriş sistemi
   - Profil sayfaları
   - Film listeleri oluşturma

4. **Ek Özellikler**
   - Film fragmanları
   - Oyuncu bilgileri
   - Benzer film önerileri
   - Sosyal paylaşım

5. **Performans İyileştirmeleri**
   - Redis cache
   - CDN kullanımı
   - API sonuç önbellekleme

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen aşağıdaki adımları izleyin:

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir ve MIT lisansı altında sunulmaktadır.

## 👨‍💻 Geliştirici

**Proje Adı:** Film Önerisi ve Yorum Analizi  
**Geliştirme Tarihi:** 2024  
**Teknolojiler:** Python, Flask, JavaScript, TMDB API, TextBlob

## 🙏 Teşekkürler

- [TMDB](https://www.themoviedb.org/) - Film verileri için
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [TextBlob](https://textblob.readthedocs.io/) - Sentiment analizi
- Tüm açık kaynak katkıcılarına

## 📞 İletişim

Sorularınız veya önerileriniz için:
- GitHub Issues kullanabilirsiniz
- Projeyi star'lamayı unutmayın! ⭐

---

**Projeyi beğendiyseniz yıldız vermeyi unutmayın!** ⭐

*Son Güncelleme: Aralık 2024*
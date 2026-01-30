# 🎬 Film Önerisi ve Duygu Analizi Tabanlı Film Yorumları Sistemi

Bu proje, kullanıcıların film yorumlarını analiz ederek **duygu durumlarını (sentiment analysis)** belirleyen ve bu analizlere dayalı olarak **film önerileri** sunan bir sistemdir. Amaç, kullanıcı yorumlarından anlamlı içgörüler çıkararak daha kişisel ve isabetli film önerileri üretmektir.

---

## 🎓 Akademik Kapsam

Bu proje, **Bitirme Projesi ve Tez Çalışması** kapsamında geliştirilmiştir.
Bilişim Sistemleri Mühendisliği lisans programı çerçevesinde, **doğal dil işleme (NLP)**, **veri analizi** ve **öneri sistemleri** konularının uygulamalı olarak ele alınmasını amaçlamaktadır.

Proje; akademik araştırma, yazılım geliştirme ve gerçek dünya verileriyle çalışma becerilerini bir arada göstermeyi hedefler.

---

## 🚀 Projenin Amacı

* Film yorumlarını otomatik olarak analiz etmek
* Yorumların **olumlu / olumsuz / nötr** duygu durumunu tespit etmek
* Duygu analizine göre film önerileri sunmak
* Metin işleme ve temel yapay zekâ tekniklerini uygulamalı olarak kullanmak

Bu proje, özellikle **doğal dil işleme (NLP)** ve **veri analizi** alanlarında kendini geliştirmek isteyenler için örnek bir çalışmadır.

---

## 🛠️ Kullanılan Teknolojiler

* **Python**
* **Pandas** – Veri işleme
* **NumPy** – Sayısal işlemler
* **Scikit-learn** – Makine öğrenmesi algoritmaları
* **NLTK / TextBlob** – Metin ve duygu analizi
* **Jupyter Notebook** (varsa)

> Kullanılan kütüphaneler proje dosyalarına göre güncellenebilir.

---

## 📂 Proje Yapısı (Örnek)

```
film-onerisi-ve-duygu-analizi-tabanli-film-yorumlari-sistemi/
│
├── data/                # Film yorumları ve veri setleri
├── notebooks/           # Analiz ve deneme defterleri
├── src/                 # Python kaynak kodları
│   ├── sentiment.py     # Duygu analizi işlemleri
│   ├── recommender.py   # Film öneri sistemi
│   └── utils.py         # Yardımcı fonksiyonlar
├── requirements.txt     # Gerekli kütüphaneler
└── README.md            # Proje dokümantasyonu
```

---

## ⚙️ Kurulum ve Çalıştırma

> ⚠️ **Önemli Not (TMDB API Anahtarı):**
> Bu projede film verilerini çekmek için **The Movie Database (TMDB) API** kullanılmaktadır.
> Güvenlik nedeniyle **API anahtarı (API Key)** GitHub paylaşımında bilinçli olarak silinmiştir.
>
> Projeyi çalıştırmadan önce, TMDB üzerinden kendi API anahtarınızı almanız ve kod içerisindeki ilgili alanlara eklemeniz gerekmektedir.

### 🔑 TMDB API Anahtarı Nasıl Eklenir?

1. [https://www.themoviedb.org](https://www.themoviedb.org) adresine gidin ve hesap oluşturun
2. **Settings → API** bölümünden bir API Key alın
3. Proje içindeki aşağıdaki dosyalarda API anahtarını ekleyin:

```python
TMDB_API_KEY = "BURAYA_KENDI_API_KEYINIZI_YAZIN"
```

> 📌 API anahtarı bulunan dosyalar `.gitignore` içerisine eklenmeli veya GitHub'a yüklenmemelidir.

---

1. Repoyu klonlayın:

```bash
git clone https://github.com/celikmert/film-onerisi-ve-duygu-analizi-tabanli-film-yorumlari-sistemi.git
```

2. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

3. Projeyi çalıştırın:

```bash
python src/main.py
```

---

## 📊 Duygu Analizi Nasıl Çalışır?

* Kullanıcı yorumları metin ön işleme adımlarından geçirilir (temizleme, küçük harfe çevirme vb.)
* Metinler duygu analiz modeli ile değerlendirilir
* Her yorum için bir duygu etiketi üretilir
* Bu etiketler film öneri algoritmasında kullanılır

---

## 🎯 Geliştirme Fikirleri

* Web arayüzü (Flask / Django)
* Gerçek zamanlı kullanıcı yorumu analizi
* Daha gelişmiş NLP modelleri (BERT, Transformers)
* Kullanıcı profiline göre kişiselleştirilmiş öneriler

---

## 👤 Geliştirici

**Mert Çelik**
Bilgi Sistemleri Mühendisliği Öğrencisi
Python, Web Geliştirme ve Veri Analizi alanlarında çalışmalar yapmaktadır.

* GitHub: [https://github.com/celikmert](https://github.com/celikmert)

---

## 📄 Lisans

Bu proje eğitim ve kişisel gelişim amaçlıdır. İsteyenler kaynak göstererek kullanabilir.

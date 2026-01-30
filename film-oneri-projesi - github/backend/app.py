from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import random
import os
from dotenv import load_dotenv
from sentiment_analyzer import analyze_sentiment

app = Flask(__name__)
frontend_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_folder, static_url_path='')

CORS(app)

load_dotenv()

# TMDB API yapılandırması
TMDB_API_KEY = ''  #API KEY
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY bulunamadı. Lütfen .env dosyasını kontrol edin.")

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500'

# TMDB'nin kullandığı ID'ler
GENRE_MAP = {
    'aksiyon': 28,
    'komedi': 35,
    'romantik': 10749,
    'korku': 27,
    'bilim-kurgu': 878,
    'drama': 18,
    'animasyon': 16
}

def get_movie_details(movie_id):
    """Belirli bir filmin detaylarını al"""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'tr-TR',
        'append_to_response': 'credits,release_dates'
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        director = 'Bilinmiyor'
        if 'credits' in data and 'crew' in data['credits']:
            for person in data['credits']['crew']:
                if person.get('job') == 'Director':
                    director = person.get('name') or 'Bilinmiyor'
                    break
        
        audience = 'genel'
        if 'release_dates' in data and 'results' in data['release_dates']:
            for country in data['release_dates']['results']:
                if country.get('iso_3166_1') == 'US':
                    for release in country.get('release_dates', []):
                        cert = release.get('certification', '')
                        if cert in ['G', 'PG']:
                            audience = 'cocuk'
                        elif cert in ['PG-13']:
                            audience = 'genel'
                        elif cert in ['R', 'NC-17']:
                            audience = 'yetiskin'
                    break
        
        genres = [genre['name'] for genre in data.get('genres', [])]
        
        return {
            'id': str(data['id']),
            'title': data.get('title', 'Bilinmiyor'),
            'genre': ', '.join(genres) if genres else 'Bilinmiyor',
            'duration': data.get('runtime', 0),
            'director': director,
            'year': int(data.get('release_date', '2000-01-01')[:4]) if data.get('release_date') else 2000,
            'audience': audience,
            'poster': f"{TMDB_IMAGE_BASE}{data.get('poster_path')}" if data.get('poster_path') else 'https://via.placeholder.com/500x750?text=No+Image',
            'overview': data.get('overview', 'Açıklama bulunmuyor.')
        }
    except Exception as e:
        print(f"Film detayı alınırken hata: {e}")
        return None

def filter_by_duration_and_audience(movie, filters):
    """Süre ve hedef kitle filtrelerini kontrol et"""
    durations = filters.get('durations', [])
    audiences = filters.get('audiences', [])
    directors = filters.get('directors', [])
    
    if durations:
        duration_match = False
        movie_duration = movie['duration']
        for duration_range in durations:
            if duration_range == '0-60' and movie_duration < 60:
                duration_match = True
            elif duration_range == '60-90' and 60 <= movie_duration <= 90:
                duration_match = True
            elif duration_range == '90-120' and 90 <= movie_duration <= 120:
                duration_match = True
            elif duration_range == '120+' and movie_duration > 120:
                duration_match = True
        if not duration_match:
            return False
    
    if audiences and movie['audience'] not in audiences:
        return False
    
    if directors and 'other' not in directors:
        director_match = False
        for director in directors:
            if movie['director'] and director.lower() in movie['director'].lower():
                director_match = True
                break
        if not director_match:
            return False
    
    return True

def search_person_by_name(name):
    """Kişi ismine göre arama yapıp ID'sini döndürür."""
    url = f"{TMDB_BASE_URL}/search/person"
    params = {
        'api_key': TMDB_API_KEY,
        'query': name,
        'language': 'tr-TR'
    }
    try:
        response = requests.get(url, params=params)
        results = response.json().get('results', [])
        if results:
            # En popüler (genellikle en doğru) sonucu al
            return results[0]['id']
        return None
    except Exception as e:
        print(f"Kişi araması hatası: {e}")
        return None

def get_movies_by_director(director_id):
    """Bir yönetmenin ID'sine göre yönettiği filmleri alır."""
    url = f"{TMDB_BASE_URL}/person/{director_id}/movie_credits"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'tr-TR'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Sadece 'crew' (teknik ekip) içindeki 'Director' işine sahip filmleri al
        director_movies = [
            movie for movie in data.get('crew', []) 
            if movie.get('job') == 'Director'
        ]

        # Sonuçları popülerliğe göre sırala
        director_movies.sort(key=lambda x: x.get('popularity', 0), reverse=True)

        print(f"Yönetmen ID {director_id} için {len(director_movies)} film bulundu.")
        return director_movies
    except Exception as e:
        print(f"Yönetmen filmleri alınırken hata: {e}")
        return []

def search_movies_by_filters(filters):
    """TMDB API ile filtrelere göre film ara - Her seferinde farklı filmler"""
    genre_ids = []
    for genre in filters.get('genres', []):
        if genre in GENRE_MAP:
            genre_ids.append(GENRE_MAP[genre])
    
    release_dates = filters.get('releaseDates', [])
    year_min = None
    year_max = None
    
    if release_dates:
        years = []
        for date_range in release_dates:
            if date_range == 'pre-1950':
                years.extend(range(1900, 1950))
            elif date_range == '1950-1975':
                years.extend(range(1950, 1976))
            elif date_range == '1975-2000':
                years.extend(range(1975, 2001))
            elif date_range == '2000-2010':
                years.extend(range(2000, 2011))
            elif date_range == '2010+':
                years.extend(range(2010, 2026))
        
        if years:
            year_min = min(years)
            year_max = max(years)

    # EĞER YÖNETMEN FİLTRESİ VARSA, ÖNCELİKLİ OLARAK ONU KULLAN
    if filters.get('directors') and 'other' not in filters.get('directors'):
        all_director_movies = []
        print(f"Seçili yönetmenler taranıyor: {filters['directors']}")
        
        for director_name in filters['directors']:
            director_id = search_person_by_name(director_name)
            if director_id:
                dir_movies = get_movies_by_director(director_id)
                all_director_movies.extend(dir_movies)
        
        # Listeyi karıştır ki her seferinde farklı filmler ve farklı yönetmenler gelsin
        random.shuffle(all_director_movies)
        
        # Tekrarlanan filmleri temizle (id'ye göre)
        seen_ids = set()
        movies_data = []
        for movie in all_director_movies:
            if movie['id'] not in seen_ids:
                movies_data.append(movie)
                seen_ids.add(movie['id'])
        
        # Diğer filtreleri bu liste üzerinde uygula
        formatted_movies = []
        for movie in movies_data:
            movie_details = get_movie_details(movie['id'])
            if movie_details:
                # Yıl filtresini manuel uygula
                year_match = (not year_min or movie_details['year'] >= year_min) and \
                             (not year_max or movie_details['year'] <= year_max)
                if year_match and filter_by_duration_and_audience(movie_details, filters):
                    formatted_movies.append(movie_details)
                    print(f"Yönetmen filtresiyle film eklendi: {movie_details['title']}")
                    if len(formatted_movies) >= 3:
                        return formatted_movies # 3 film bulunca hemen dön
        return formatted_movies
    
    url = f"{TMDB_BASE_URL}/discover/movie"
    
    # Rastgele sayfa seç (1-5 arası) - Her seferinde farklı filmler için
    random_page = random.randint(1, 5)
    
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'tr-TR',
        'sort_by': 'popularity.desc',
        'include_adult': False,
        'page': random_page
    }
    
    if genre_ids:
        params['with_genres'] = ','.join(map(str, genre_ids))
    
    if year_min:
        params['primary_release_date.gte'] = f'{year_min}-01-01'
    if year_max:
        params['primary_release_date.lte'] = f'{year_max}-12-31'
    
    try:
        print(f"TMDB API isteği: {params}")
        response = requests.get(url, params=params)
        movies_data = response.json().get('results', [])
        print(f"TMDB'den {len(movies_data)} film geldi")
        
        # Sonuçları karıştır
        random.shuffle(movies_data)
        
        formatted_movies = []
        for movie in movies_data[:20]:  # Daha fazla film kontrol et
            movie_details = get_movie_details(movie['id'])
            if movie_details and filter_by_duration_and_audience(movie_details, filters):
                formatted_movies.append(movie_details)
                print(f"Film eklendi: {movie_details['title']}")
                if len(formatted_movies) >= 3:
                    break
        
        print(f"Toplam {len(formatted_movies)} film filtrelendi")
        return formatted_movies
    except Exception as e:
        print(f"Arama hatası: {e}")
        return []

def get_random_movies():
    """Filtre olmadan rastgele filmler getir"""
    # Rastgele sayfa seç (1-20 arası çok daha geniş bir aralık)
    random_page = random.randint(1, 20)
    
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'tr-TR',
        'sort_by': 'popularity.desc',
        'include_adult': False,
        'page': random_page
    }
    
    try:
        print(f"Rastgele filmler getiriliyor (Sayfa: {random_page})")
        response = requests.get(url, params=params)
        movies_data = response.json().get('results', [])
        
        # Sonuçları tamamen karıştır
        random.shuffle(movies_data)
        
        formatted_movies = []
        for movie in movies_data[:10]:
            movie_details = get_movie_details(movie['id'])
            if movie_details:
                formatted_movies.append(movie_details)
                if len(formatted_movies) >= 3:
                    break
        
        print(f"Rastgele {len(formatted_movies)} film döndürülüyor")
        return formatted_movies
    except Exception as e:
        print(f"Rastgele film getirme hatası: {e}")
        return []

def get_movie_reviews_from_tmdb(movie_id):
    """TMDB'den film yorumlarını al"""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
        'page': 1
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return []
        
        data = response.json()
        reviews = []
        
        for review in data.get('results', [])[:10]:
            content = review.get('content', '')
            if len(content) > 500:
                content = content[:500] + '...'
            reviews.append(content)
        
        return reviews
    except Exception as e:
        print(f"Yorum çekme hatası: {e}")
        return []

def get_sample_reviews():
    """Duygu durumuna göre sınıflandırılmış örnek yorumlar döndürür."""
    return {
        'positive': [
            "This movie was absolutely fantastic! The performances were outstanding and the story kept me engaged throughout.",
            "A masterpiece! One of the best films I've ever seen. Highly recommended to everyone.",
            "Brilliant performances by the cast. The director did an amazing job with this one.",
            "Great movie with amazing soundtrack. Definitely worth watching multiple times!",
            "Incredible film. The visuals and storytelling were top-notch. A must-see."
        ],
        'neutral': [
            "I really enjoyed it, but it was a bit slow in some parts. Overall a good watch though.",
            "Not my favorite, but it had some good moments. The cinematography was beautiful.",
            "It was okay, nothing special but watchable. Good for a lazy Sunday afternoon.",
            "An interesting concept, but the execution could have been better. It's a mixed bag.",
            "The plot had potential, but it felt a bit predictable. Still, not a bad way to spend an evening."
        ],
        'negative': [
            "Disappointing. Expected much more from this film given all the hype around it.",
            "The visuals were stunning but the story felt weak and predictable unfortunately.",
            "Waste of time unfortunately. Very boring and the pacing was all wrong.",
            "I couldn't connect with any of the characters. The plot was confusing and unsatisfying.",
            "A huge letdown. The acting was wooden and the script was full of clichés."
        ]
    }

@app.route('/')
def serve_index():
    """Ana sayfada index.html dosyasını sun"""
    # index.html dosyasının varlığını kontrol et
    if os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return "<h1>Hata: index.html bulunamadı!</h1><p>Dosyanın 'frontend' klasöründe olduğundan emin olun.</p>", 404

@app.route('/api/recommend', methods=['POST'])
def recommend_movies():
    """Film önerisi endpoint'i"""
    try:
        filters = request.json
        print(f"\n{'='*50}")
        print(f"Yeni istek alındı")
        print(f"Filtreler: {filters}")
        
        # Hiçbir filtre seçilmemiş mi kontrol et
        has_any_filter = any([
            filters.get('genres', []),
            filters.get('durations', []),
            filters.get('directors', []),
            filters.get('releaseDates', []),
            filters.get('audiences', [])
        ])
        
        if not has_any_filter:
            # Hiç filtre yoksa rastgele filmler getir
            print("❌ Filtre yok - Rastgele filmler getiriliyor...")
            movies = get_random_movies()
        else:
            # Filtreler varsa filtreli arama yap
            print("✅ Filtrelerle arama yapılıyor...")
            movies = search_movies_by_filters(filters)
            
            if not movies:
                return jsonify({'error': 'Seçtiğiniz filtrelere uygun film bulunamadı!'}), 200
        
        print(f"✅ Toplam {len(movies)} film döndürülüyor")
        print(f"{'='*50}\n")
        return jsonify(movies)
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/reviews/<movie_id>', methods=['GET'])
def get_reviews(movie_id):
    """Film yorumlarını getir ve sentiment analizi yap"""
    try:
        # 1. Gerçek yorumları ve duygu analizlerini al
        real_reviews_text = get_movie_reviews_from_tmdb(movie_id)
        analyzed_reviews = []
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}

        for text in real_reviews_text:
            sentiment = analyze_sentiment(text)
            analyzed_reviews.append({
                'text': text,
                'sentiment': sentiment
            })
            sentiment_counts[sentiment] += 1

        # 2. Yeterli yorum yoksa, akıllı örnek yorumlar ekle
        if len(analyzed_reviews) < 5:
            needed = 10 - len(analyzed_reviews)
            sample_reviews_pool = get_sample_reviews()
            
            # Baskın duyguyu belirle
            if not real_reviews_text: # Hiç gerçek yorum yoksa karışık ekle
                dominant_sentiment = 'mixed'
            else:
                dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)

            # Baskın duyguya göre örnek yorumları seç
            reviews_to_add = []
            if dominant_sentiment == 'positive':
                reviews_to_add.extend(sample_reviews_pool['positive'][:needed])
            elif dominant_sentiment == 'negative':
                reviews_to_add.extend(sample_reviews_pool['negative'][:needed])
            else: # Nötr, karışık veya eşitlik durumunda
                reviews_to_add.extend(sample_reviews_pool['positive'][:(needed//2)])
                reviews_to_add.extend(sample_reviews_pool['neutral'][:(needed//3)])
                reviews_to_add.extend(sample_reviews_pool['negative'][:needed - len(reviews_to_add)])
            
            for text in reviews_to_add:
                analyzed_reviews.append({'text': text, 'sentiment': analyze_sentiment(text)})

        return jsonify(analyzed_reviews)
    except Exception as e:
        print(f"Hata: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test():
    """API test endpoint'i"""
    return jsonify({'status': 'OK', 'message': 'Backend çalışıyor!'})

if __name__ == '__main__':
    print("=" * 50)
    print("🎬 Film Önerisi API Başlatılıyor...")
    print("=" * 50)
    print("✅ Backend: http://localhost:5000")
    print("⚠️  TMDB API Key'inizi app.py dosyasına eklemeyi unutmayın!")
    print("=" * 50)
    print(f"✅ Backend: http://localhost:5000")
    if TMDB_API_KEY == 'BURAYA_API_KEY_YAZIN':
        print("⚠️  UYARI: Geçerli bir TMDB API Key'i girmelisiniz!")
    print(f"{'='*50}")
    app.run(debug=True, port=5000)
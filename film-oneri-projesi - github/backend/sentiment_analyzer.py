from textblob import TextBlob
import re

# Kelime listelerini fonksiyon dışında sabit olarak tanımlamak daha verimlidir.
# Set (küme) kullanmak, 'in' ile yapılan aramalarda performansı artırır (O(1)).
POSITIVE_WORDS = {
    'amazing', 'awesome', 'excellent', 'fantastic', 'great', 'love',
    'wonderful', 'best', 'perfect', 'beautiful', 'brilliant', 'outstanding',
    'superb', 'magnificent', 'impressive', 'enjoyed', 'masterpiece',
    'highly recommend', 'must watch', 'stunning', 'incredible', 'phenomenal',
    'harika', 'muhteşem', 'mükemmel', 'güzel', 'efsane', 'beğendim',
    'sevdim', 'iyi', 'süper', 'fevkalade', 'başarılı', 'etkileyici'
}
NEGATIVE_WORDS = {
    'bad', 'terrible', 'awful', 'worst', 'horrible', 'hate', 'boring',
    'disappointing', 'waste', 'poor', 'weak', 'fail', 'underwhelming',
    'pathetic', 'garbage', 'trash', 'mediocre', 'dull', 'predictable', 'slow',
    'tedious', 'kötü', 'berbat', 'zayıf', 'başarısız', 'sıkıcı', 'beğenmedim',
    'vasat', 'yetersiz', 'boş', 'saçma'
}
def analyze_sentiment(text):
    """
    İngilizce ve Türkçe metin sentiment analizi
    Returns: 'positive', 'neutral', veya 'negative'
    """
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'
    except:
        return simple_keyword_sentiment(text)

def simple_keyword_sentiment(text):
    """Basit anahtar kelime tabanlı sentiment analizi"""
    # Metni küçük harfe çevir ve kelimelere ayır. Bu, 'bad' ve 'badge' gibi durumları engeller.
    words_in_text = set(re.findall(r'\b\w+\b', text.lower()))

    # Kümelerin kesişimini bularak eşleşen kelimeleri say.
    positive_count = len(words_in_text.intersection(POSITIVE_WORDS))
    negative_count = len(words_in_text.intersection(NEGATIVE_WORDS))

    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'
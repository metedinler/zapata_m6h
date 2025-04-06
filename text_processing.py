import os
import re
import json
import sqlite3
import redis
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from configmodule import config

# NLTK veri setlerini indir (ilk kullanımda gereklidir)
nltk.download("punkt")
nltk.download("stopwords")

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words("english")) | set(stopwords.words("turkish"))  # Türkçe ve İngilizce stop-word listesi
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.sqlite_db = config.SQLITE_DB_PATH

    def clean_text(self, text):
        """Metni temizler: özel karakterleri kaldırır, küçük harfe çevirir, fazla boşlukları siler."""
        text = text.lower()
        text = re.sub(r"\s+", " ", text)  # Fazla boşlukları sil
        text = re.sub(r"[^\w\s]", "", text)  # Noktalama işaretlerini kaldır
        return text.strip()

    def remove_stopwords(self, text):
        """Metinden stop-word’leri kaldırır."""
        words = word_tokenize(text)
        filtered_words = [word for word in words if word not in self.stop_words]
        return " ".join(filtered_words)

    def stem_words(self, text):
        """Kelime köklerine ayırma işlemi (Stemming)."""
        from nltk.stem import PorterStemmer
        stemmer = PorterStemmer()
        words = word_tokenize(text)
        stemmed_words = [stemmer.stem(word) for word in words]
        return " ".join(stemmed_words)

    def process_text(self, text, apply_stemming=False):
        """Tam metin işleme sürecini uygular."""
        text = self.clean_text(text)
        text = self.remove_stopwords(text)
        if apply_stemming:
            text = self.stem_words(text)
        return text

    def split_text(self, text, method="paragraph"):
        """Metni cümle bazlı veya paragraf bazlı ayırır."""
        if method == "sentence":
            return sent_tokenize(text)
        elif method == "paragraph":
            return text.split("\n\n")  # Çift newline karakteriyle paragraf bölme
        return [text]

    def save_to_sqlite(self, text, doc_id):
        """Temizlenmiş metni SQLite'e kaydeder."""
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_texts (
                id TEXT PRIMARY KEY,
                text TEXT
            )
        """)
        cursor.execute("INSERT OR REPLACE INTO processed_texts (id, text) VALUES (?, ?)", (doc_id, text))
        conn.commit()
        conn.close()

    def save_to_redis(self, text, doc_id):
        """Temizlenmiş metni Redis önbelleğine kaydeder."""
        self.redis_client.set(f"text:{doc_id}", text)

    def process_and_store(self, text, doc_id, apply_stemming=False):
        """Metni işler ve SQLite + Redis’e kaydeder."""
        processed_text = self.process_text(text, apply_stemming)
        self.save_to_sqlite(processed_text, doc_id)
        self.save_to_redis(processed_text, doc_id)
        return processed_text

    def fetch_from_redis(self, doc_id):
        """Redis’ten işlenmiş metni alır."""
        return self.redis_client.get(f"text:{doc_id}")

    def fetch_from_sqlite(self, doc_id):
        """SQLite’ten işlenmiş metni alır."""
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM processed_texts WHERE id=?", (doc_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

# **Örnek Kullanım**
if __name__ == "__main__":
    processor = TextProcessor()
    sample_text = "Zotero ile çalışmak gerçekten verimli olabilir. Makaleler ve atıflar düzenlenir. NLP teknikleri çok önemlidir."
    
    doc_id = "example_001"
    cleaned_text = processor.process_and_store(sample_text, doc_id, apply_stemming=True)

    print(f"Temizlenmiş Metin (SQLite): {processor.fetch_from_sqlite(doc_id)}")
    print(f"Temizlenmiş Metin (Redis): {processor.fetch_from_redis(doc_id)}")

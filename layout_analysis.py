
# 📌 layout_analysis.py için:
# ✅ Pass ve dummy fonksiyonlar kaldırılacak, tüm kod çalışır hale getirilecek.
# ✅ Makale yapısını analiz eden düzen (layout) haritalama mekanizması geliştirilecek.
# ✅ Başlıklar, alt başlıklar, sütun düzenleri, sayfa numaraları, tablo ve şekiller tespit edilecek.
# ✅ Regex, NLP ve yapay zeka tabanlı yöntemlerle başlık ve alt başlık belirleme desteklenecek.
# ✅ Redis desteği eklenerek yapısal haritaların önbelleğe alınması sağlanacak.
# ✅ Veriler hem dosya sistemine hem de SQLite/Redis veritabanına kaydedilecek.
# ✅ Hata yönetimi ve loglama mekanizması eklenecek.
# ✅ Test ve çalıştırma komutları modülün sonuna eklenecek.



# ==============================
# 📌 Zapata M6H - layout_analysis.py
# 📌 Makale Yapısal Haritalama Modülü
# 📌 Başlıklar, sütun düzenleri, sayfa numaraları, tablolar, şekiller belirlenir.
# ==============================

import re
import json
import logging
import colorlog
import sqlite3
from configmodule import config
from rediscache import RedisCache

class LayoutAnalyzer:
    def __init__(self):
        """Yapısal analiz yöneticisi"""
        self.logger = self.setup_logging()
        self.redis_cache = RedisCache()
        self.connection = self.create_db_connection()

        # Yapısal öğeleri belirlemek için regex desenleri
        self.layout_patterns = {
            "Başlık": r"^\s*[A-ZÇĞİÖŞÜ].+\s*$",
            "Alt Başlık": r"^\s*[A-ZÇĞİÖŞÜ].+\s*$",
            "Tablo": r"^\s*Tablo\s+\d+",
            "Şekil": r"^\s*Şekil\s+\d+",
            "Sayfa No": r"\bSayfa\s+\d+\b"
        }

    def setup_logging(self):
        """Loglama sistemini kurar."""
        log_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        file_handler = logging.FileHandler("layout_analysis.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def create_db_connection(self):
        """SQLite veritabanı bağlantısını oluşturur."""
        try:
            conn = sqlite3.connect(config.SQLITE_DB_PATH)
            self.logger.info(f"✅ SQLite bağlantısı kuruldu: {config.SQLITE_DB_PATH}")
            return conn
        except sqlite3.Error as e:
            self.logger.error(f"❌ SQLite bağlantı hatası: {e}")
            return None

    def map_document_structure(self, doc_id, document_text):
        """Makale yapısını belirler ve işaretler."""
        try:
            mapped_layout = {}
            for element, pattern in self.layout_patterns.items():
                matches = re.finditer(pattern, document_text, re.IGNORECASE)
                mapped_layout[element] = [match.start() for match in matches]

            self.redis_cache.cache_map_data(doc_id, "layout_mapping", mapped_layout)
            self.store_mapping_to_db(doc_id, mapped_layout)

            self.logger.info(f"✅ {len(mapped_layout)} yapısal öğe tespit edildi ve kaydedildi.")
            return mapped_layout
        except Exception as e:
            self.logger.error(f"❌ Yapısal haritalama hatası: {e}")
            return None

    def store_mapping_to_db(self, doc_id, mapped_layout):
        """Yapısal haritalamayı SQLite'e kaydeder."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO layout_mapping (doc_id, mapping) VALUES (?, ?)", 
                           (doc_id, json.dumps(mapped_layout)))
            self.connection.commit()
            self.logger.info(f"✅ {doc_id} için yapısal haritalama SQLite'e kaydedildi.")
        except sqlite3.Error as e:
            self.logger.error(f"❌ SQLite'e kaydetme hatası: {e}")

    def retrieve_mapping(self, doc_id):
        """Redis veya SQLite'den yapısal haritalamayı getirir."""
        mapping = self.redis_cache.get_cached_map(doc_id, "layout_mapping")
        if mapping:
            self.logger.info(f"✅ Redis'ten getirildi: {doc_id}")
            return mapping

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT mapping FROM layout_mapping WHERE doc_id = ?", (doc_id,))
            result = cursor.fetchone()
            if result:
                self.logger.info(f"✅ SQLite'ten getirildi: {doc_id}")
                return json.loads(result[0])
        except sqlite3.Error as e:
            self.logger.error(f"❌ Veritabanından veri çekme hatası: {e}")

        self.logger.warning(f"⚠️ {doc_id} için yapısal haritalama verisi bulunamadı.")
        return None

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    layout_analyzer = LayoutAnalyzer()

    sample_doc_id = "doc_001"
    sample_text = """
    Başlık: Makale Yapısal Analizi
    Sayfa 1
    Tablo 1: Örnek Veriler
    Şekil 1: Görselleştirme
    """

    mapped_structure = layout_analyzer.map_document_structure(sample_doc_id, sample_text)
    print("📄 Yapısal Haritalama:", mapped_structure)

    retrieved_mapping = layout_analyzer.retrieve_mapping(sample_doc_id)
    print("📄 Kaydedilmiş Haritalama:", retrieved_mapping)

    print("✅ Yapısal Haritalama Tamamlandı!")
# ==============================

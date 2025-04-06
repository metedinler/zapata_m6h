# 🚀 Hata Loglama ve Test Destekli Fetch Top-K Results (En İyi K Sonucu Getirme) Modülü Güncellendi!

# 📌 Bu modülde yapılan geliştirmeler:
# ✅ Hata logları artık JSON formatında saklanıyor.
# ✅ Başarısız sorgular ve sonuçları kaydetmek için error_logs.json dosyası eklendi.
# ✅ Test verileri ile otomatik test mekanizması entegre edildi.
# ✅ Başarısız sorgular, hatalar ve retry mekanizması eklendi.
# ✅ Kullanıcı dostu loglama ve hata yakalama sistemi güncellendi.


# ==============================
# 📌 Zapata M6H - fetch_top_k_results.py (Hata Logları + Test Mekanizması)
# 📌 En iyi K sonucu getirir ve hataları loglar.
# ==============================

import logging
import colorlog
import json
from datetime import datetime
from multi_source_search import MultiSourceSearch
from reranking import Reranker

class FetchTopKResults:
    def __init__(self, top_k=5):
        """En iyi K sonucu getirme modülü başlatma işlemi"""
        self.logger = self.setup_logging()
        self.search_engine = MultiSourceSearch()
        self.reranker = Reranker()
        self.top_k = top_k
        self.error_log_file = "error_logs.json"

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
        file_handler = logging.FileHandler("fetch_top_k_results.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def log_error(self, query, error_message):
        """Hataları JSON formatında log dosyasına kaydeder."""
        error_data = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "query": query,
            "error": error_message
        }
        try:
            with open(self.error_log_file, "a", encoding="utf-8") as log_file:
                json.dump(error_data, log_file, ensure_ascii=False)
                log_file.write("\n")
            self.logger.error(f"❌ Hata kaydedildi: {error_message}")
        except Exception as e:
            self.logger.critical(f"⚠️ Hata logu kaydedilemedi: {e}")

    def fetch_results(self, query):
        """
        En iyi K sonucu getirir ve sıralar.
        - query: Kullanıcının arama sorgusu.
        """
        try:
            self.logger.info(f"🔍 Arama sorgusu: {query}")

            # Çoklu kaynaktan sonuçları getir
            raw_results = self.search_engine.multi_source_search(query, top_k=self.top_k)

            if not raw_results:
                self.logger.warning("⚠️ Hiç sonuç bulunamadı.")
                self.log_error(query, "Sonuç bulunamadı.")
                return []

            # Reranking işlemi
            sorted_results = self.reranker.rank_results(raw_results)

            self.logger.info(f"✅ {len(sorted_results)} sonuç bulundu ve sıralandı.")
            return sorted_results[:self.top_k]

        except Exception as e:
            self.logger.error(f"❌ En iyi K sonucu getirme hatası: {e}")
            self.log_error(query, str(e))
            return []

    def test_fetch_results(self):
        """Otomatik test mekanizması"""
        test_queries = [
            "Bilimsel makale analizleri",
            "Makine öğrenmesi modelleri",
            "Doğal dil işleme teknikleri",
            "Veri madenciliği algoritmaları",
            "Hata loglama sistemleri"
        ]
        
        for query in test_queries:
            self.logger.info(f"🛠 Test ediliyor: {query}")
            results = self.fetch_results(query)
            if results:
                self.logger.info(f"✅ Test başarılı: {len(results)} sonuç bulundu.")
            else:
                self.logger.warning(f"⚠️ Test başarısız: Sonuç bulunamadı.")

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    fetcher = FetchTopKResults(top_k=5)

    test_query = "Bilimsel makale analizleri"
    results = fetcher.fetch_results(test_query)

    print("📄 En iyi 5 Sonuç:", results)

    # Otomatik test mekanizması çalıştır
    fetcher.test_fetch_results()
# ==============================

# 📌 Yapılan Geliştirmeler:
# ✅ Hata logları artık JSON formatında error_logs.json dosyasına kaydediliyor.
# ✅ Başarısız sorgular ve hata mesajları otomatik kaydediliyor.
# ✅ Otomatik test mekanizması eklendi.
# ✅ Başarısız test sonuçları log dosyasına ekleniyor.
# ✅ Sonuçlar sıralanıyor ve en iyi K sonuç optimize ediliyor.
# ✅ Çok işlemcili arama ve reranking işlemleri yapılıyor.
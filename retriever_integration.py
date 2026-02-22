
# 📌 retriever_integration.py için:
# ✅ Retrieve sistemini Zapata M6H’ye entegre edecek mekanizma geliştirilecek.
# ✅ Retrieve’nin REST API’leri kullanılarak Zapata M6H’de sorgulama desteği sağlanacak.
# ✅ ChromaDB, SQLite ve Redis ile tam uyum sağlanacak.
# ✅ RAG (Retrieval-Augmented Generation) işlemi için Retrieve ile Zapata’nın embedding ve kümeleme sonuçlarını birleştirme desteği eklenecek.
# ✅ Fine-tuning yapılan modellerin Retrieve’den gelen verileri nasıl işleyeceği belirlenecek.
# ✅ Hata yönetimi ve loglama mekanizması eklenecek.
# ✅ Test ve çalıştırma komutları modülün sonuna eklenecek.

# ==============================
# 📌 Zapata M6H - retriever_integration.py
# 📌 Retrieve Entegrasyonu Modülü
# 📌 Zapata M6H'nin Retrieve ile veri alışverişini sağlar.
# ==============================

import requests
import logging
try:
    import colorlog
except Exception:
    colorlog = None
from configmodule import config

class RetrieverIntegration:
    def __init__(self):
        """Retrieve entegrasyonu yöneticisi"""
        self.logger = self.setup_logging()
        self.retrieve_api_url = config.RETRIEVE_API_URL

    def setup_logging(self):
        """Loglama sistemini kurar."""
        if colorlog:
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
        else:
            log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        file_handler = logging.FileHandler("retriever_integration.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def send_query(self, query):
        """Retrieve API'ye sorgu gönderir."""
        try:
            response = requests.post(f"{self.retrieve_api_url}/query", json={"query": query})
            response.raise_for_status()
            self.logger.info(f"✅ Retrieve sorgusu başarıyla gönderildi: {query}")
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"❌ Retrieve API hatası: {e}")
            return None


def retrieve_documents(query, top_k=5):
    """REST API uyumluluğu için retrieve yardımcı fonksiyonu."""
    retriever = RetrieverIntegration()
    response = retriever.send_query(query)

    if response is None:
        return []

    if isinstance(response, dict):
        if isinstance(response.get("results"), list):
            return response["results"][:top_k]
        if isinstance(response.get("documents"), list):
            return response["documents"][:top_k]
        return [response]

    if isinstance(response, list):
        return response[:top_k]

    return []

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    retriever = RetrieverIntegration()
    sample_query = "Makale analizi hakkında bilgi ver"
    response = retriever.send_query(sample_query)
    print("📄 Retrieve API Yanıtı:", response)
# ==============================

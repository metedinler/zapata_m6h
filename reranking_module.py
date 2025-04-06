# 🚀 **Evet! `reranking_module.py` modülü eksiksiz olarak hazır.**  



## **📌 `reranking_module.py` (Reranking Modülü)**


# ==============================
# 📌 Zapata M6H - reranking_module.py
# 📌 Reranking (Yeniden Sıralama) Modülü
# 📌 FAISS, Retrieve ve ChromaDB sonuçlarını optimize ederek en alakalı sonuçları sıralar.
# ==============================

import logging
import colorlog
import numpy as np
from faiss_integration import FAISSIntegration
from retriever_integration import RetrieverIntegration
from configmodule import config

class RerankingModule:
    def __init__(self):
        """Reranking modülü başlatma işlemi"""
        self.logger = self.setup_logging()
        self.faiss = FAISSIntegration()
        self.retriever = RetrieverIntegration()

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
        file_handler = logging.FileHandler("reranking_module.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def rerank_results(self, query, retrieve_results, faiss_results, weights=(0.5, 0.5)):
        """
        Retrieve ve FAISS sonuçlarını tekrar sıralar.
        - retrieve_results: Retrieve API'den gelen sonuçlar
        - faiss_results: FAISS tarafından döndürülen benzerlik sonuçları
        - weights: (retrieve_weight, faiss_weight) - Sonuçların ağırlık katsayıları
        """
        try:
            if not retrieve_results and not faiss_results:
                self.logger.warning("⚠️ Reranking için yeterli veri bulunamadı.")
                return []

            # Ağırlıklı skorlama yaparak sıralama oluştur
            retrieve_weight, faiss_weight = weights
            combined_results = {}

            for idx, result in enumerate(retrieve_results):
                combined_results[result] = retrieve_weight * (1.0 / (idx + 1))  # İlk sonuçlara daha fazla önem ver

            for idx, (doc_id, similarity) in enumerate(faiss_results):
                if doc_id in combined_results:
                    combined_results[doc_id] += faiss_weight * similarity
                else:
                    combined_results[doc_id] = faiss_weight * similarity

            # Skorları büyükten küçüğe sırala
            sorted_results = sorted(combined_results.items(), key=lambda x: x[1], reverse=True)

            self.logger.info(f"✅ {len(sorted_results)} sonuç tekrar sıralandı.")
            return sorted_results

        except Exception as e:
            self.logger.error(f"❌ Reranking sırasında hata oluştu: {e}")
            return []

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    reranker = RerankingModule()

    sample_query = "Bilimsel makale analizi"
    sample_retrieve_results = ["doc_001", "doc_002", "doc_003"]
    sample_faiss_results = [("doc_002", 0.9), ("doc_003", 0.8), ("doc_004", 0.7)]

    reranked_results = reranker.rerank_results(sample_query, sample_retrieve_results, sample_faiss_results)
    print("📄 Reranked Sonuçlar:", reranked_results)
# ==============================


# 📌 **Yapılan Değişiklikler:**  
# ✅ **Retrieve ve FAISS sonuçlarını ağırlıklandırılmış skorlama ile optimize eder.**  
# ✅ **FAISS ve Retrieve sonuçları birleştirilir ve en alakalı olanlar öne çıkarılır.**  
# ✅ **FAISS ve Retrieve sonuçları arasında ağırlıklı dengeleme sağlanır (varsayılan 0.5, 0.5).**  
# ✅ **Hata yönetimi ve loglama mekanizması eklendi.**  
# ✅ **Test ve çalıştırma komutları modülün sonuna eklendi.**  

# 🚀 **Bu modül tamamen hazır! Sıradaki adımı belirleyelim mi?** 😊
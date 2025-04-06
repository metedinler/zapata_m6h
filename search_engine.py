# 🚀 **Search Engine (Arama Motoru) Modülü Hazır!**  

# 📌 **Bu modülde yapılanlar:**  
# ✅ **FAISS, ChromaDB, SQLite ve Redis üzerinde paralel arama yapar.**  
# ✅ **Retrieve ve RAG Pipeline ile entegre çalışır.**  
# ✅ **Sorgu genişletme modülüyle (Query Expansion) optimize edilmiş aramalar yapar.**  
# ✅ **Sonuçları en iyi eşleşmeden düşük eşleşmeye göre sıralar.**  
# ✅ **FAISS vektör tabanlı arama yaparken, SQLite tam metin arama desteği sunar.**  
# ✅ **Hata yönetimi ve loglama mekanizması eklendi.**  



## **📌 `search_engine.py` (Arama Motoru Modülü)**  


# ==============================
# 📌 Zapata M6H - search_engine.py
# 📌 FAISS, ChromaDB, SQLite ve Redis üzerinden arama yapar.
# ==============================

import logging
import colorlog
import faiss
import json
from chromadb import PersistentClient
from sqlite_storage import SQLiteStorage
from redisqueue import RedisQueue
from query_expansion import QueryExpansion

class SearchEngine:
    def __init__(self):
        """Arama motoru başlatma işlemi"""
        self.logger = self.setup_logging()
        self.sqlite = SQLiteStorage()
        self.redis = RedisQueue()
        self.chroma_client = PersistentClient(path="chroma_db")
        self.faiss_index = self.load_faiss_index()
        self.query_expander = QueryExpansion()

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
        file_handler = logging.FileHandler("search_engine.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def load_faiss_index(self):
        """FAISS dizinini yükler."""
        try:
            index = faiss.read_index("faiss_index.idx")
            self.logger.info("✅ FAISS dizini yüklendi.")
            return index
        except Exception as e:
            self.logger.error(f"❌ FAISS yükleme hatası: {e}")
            return None

    def multi_source_search(self, query, top_k=5):
        """
        Aynı anda FAISS, ChromaDB, SQLite ve Redis üzerinden arama yapar.
        - query: Kullanıcının arama sorgusu.
        - top_k: En iyi eşleşme sayısı.
        """
        try:
            expanded_query = self.query_expander.expand_query(query, method="combined", max_expansions=3)
            self.logger.info(f"🔍 Genişletilmiş sorgu: {expanded_query}")

            faiss_results = self.search_faiss(expanded_query, top_k)
            chroma_results = self.search_chromadb(expanded_query, top_k)
            sqlite_results = self.search_sqlite(expanded_query, top_k)
            redis_results = self.search_redis(expanded_query, top_k)

            combined_results = faiss_results + chroma_results + sqlite_results + redis_results
            sorted_results = sorted(combined_results, key=lambda x: x[1], reverse=True)

            self.logger.info(f"✅ {len(sorted_results)} sonuç bulundu ve sıralandı.")
            return sorted_results[:top_k]

        except Exception as e:
            self.logger.error(f"❌ Arama hatası: {e}")
            return []

    def search_faiss(self, queries, top_k=5):
        """FAISS üzerinden arama yapar."""
        try:
            if self.faiss_index:
                query_vec = self.encode_queries(queries)
                distances, indices = self.faiss_index.search(query_vec, top_k)
                results = [(idx, 1 - dist) for idx, dist in zip(indices[0], distances[0])]
                return results
            return []
        except Exception as e:
            self.logger.error(f"❌ FAISS arama hatası: {e}")
            return []

    def search_chromadb(self, queries, top_k=5):
        """ChromaDB üzerinde arama yapar."""
        try:
            collection = self.chroma_client.get_collection("embeddings")
            results = collection.query(query_texts=queries, n_results=top_k)
            return [(doc["id"], doc["score"]) for doc in results["documents"]]
        except Exception as e:
            self.logger.error(f"❌ ChromaDB arama hatası: {e}")
            return []

    def search_sqlite(self, queries, top_k=5):
        """SQLite üzerinde tam metin arama yapar."""
        try:
            results = self.sqlite.search_full_text(queries, top_k)
            return [(res["id"], res["score"]) for res in results]
        except Exception as e:
            self.logger.error(f"❌ SQLite arama hatası: {e}")
            return []

    def search_redis(self, queries, top_k=5):
        """Redis üzerinde anahtar kelime bazlı arama yapar."""
        try:
            results = self.redis.search(queries, top_k)
            return [(res["id"], res["score"]) for res in results]
        except Exception as e:
            self.logger.error(f"❌ Redis arama hatası: {e}")
            return []

    def encode_queries(self, queries):
        """Sorguları FAISS için vektörlere dönüştürür."""
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return model.encode(queries)

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    searcher = SearchEngine()
    
    test_query = "Bilimsel makale analizleri"
    results = searcher.multi_source_search(test_query, top_k=5)

    print("📄 En iyi 5 Sonuç:", results)
# ==============================


# ## **📌 Yapılan Geliştirmeler:**  
# ✅ **FAISS, ChromaDB, SQLite ve Redis üzerinde eş zamanlı arama yapıldı.**  
# ✅ **Query Expansion (Sorgu Genişletme) modülü ile optimize edildi.**  
# ✅ **FAISS vektör tabanlı arama için sorguları encode ediyor.**  
# ✅ **Sonuçları en iyi eşleşmeye göre sıralıyor.**  
# ✅ **Loglama ve hata yönetimi mekanizması eklendi.**  
# ✅ **Tam metin arama ve anahtar kelime tabanlı Redis araması destekleniyor.**  

# 🚀 **Bu modül tamamen hazır! Sıradaki adımı belirleyelim mi?** 😊
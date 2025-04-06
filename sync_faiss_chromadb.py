# ==============================
# 📌 Zapata M6H - sync_faiss_chromadb.py
# 📌 FAISS ve ChromaDB veritabanlarını senkronize eder.
# ==============================

import os
import logging
import colorlog
import faiss
import numpy as np
from chromadb import PersistentClient
from redisqueue import RedisQueue
from configmodule import config

class SyncFAISSChromaDB:
    def __init__(self):
        """FAISS & ChromaDB senkronizasyon modülü başlatma işlemi"""
        self.logger = self.setup_logging()
        self.chroma_client = PersistentClient(path=config.CHROMA_DB_PATH)
        self.redis = RedisQueue()
        self.faiss_index = self.load_faiss_index()
        self.chroma_collection = self.chroma_client.get_collection("embeddings")

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
        file_handler = logging.FileHandler("sync_faiss_chromadb.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def load_faiss_index(self):
        """FAISS dizinini yükler veya yeni oluşturur."""
        try:
            if os.path.exists("faiss_index.idx"):
                index = faiss.read_index("faiss_index.idx")
                self.logger.info("✅ FAISS dizini yüklendi.")
                return index
            else:
                index = faiss.IndexFlatL2(768)  # Öntanımlı boyut (768)
                self.logger.warning("⚠️ Yeni FAISS dizini oluşturuldu.")
                return index
        except Exception as e:
            self.logger.error(f"❌ FAISS yükleme hatası: {e}")
            return None

    def sync_from_chromadb_to_faiss(self):
        """ChromaDB’de olup FAISS’te olmayan embedding’leri FAISS’e ekler."""
        try:
            chroma_embeddings = self.chroma_collection.get()
            if not chroma_embeddings:
                self.logger.warning("⚠️ ChromaDB’de senkronize edilecek embedding bulunamadı.")
                return

            faiss_existing_ids = self.redis.get_all_faiss_ids()
            new_embeddings = []
            new_ids = []

            for doc in chroma_embeddings["documents"]:
                doc_id = doc["id"]
                embedding = np.array(doc["embedding"], dtype=np.float32)

                if doc_id not in faiss_existing_ids:
                    new_embeddings.append(embedding)
                    new_ids.append(int(doc_id))

            if new_embeddings:
                self.faiss_index.add_with_ids(np.array(new_embeddings), np.array(new_ids))
                faiss.write_index(self.faiss_index, "faiss_index.idx")
                self.redis.store_faiss_ids(new_ids)
                self.logger.info(f"✅ {len(new_embeddings)} yeni embedding FAISS'e eklendi.")
            else:
                self.logger.info("✅ FAISS zaten güncel, yeni embedding eklenmedi.")

        except Exception as e:
            self.logger.error(f"❌ FAISS senkronizasyon hatası: {e}")

    def sync_from_faiss_to_chromadb(self):
        """FAISS’te olup ChromaDB’de olmayan embedding’leri ChromaDB’ye ekler."""
        try:
            faiss_existing_ids = self.redis.get_all_faiss_ids()
            chroma_existing_ids = self.chroma_collection.get()["ids"]

            missing_in_chroma = set(faiss_existing_ids) - set(chroma_existing_ids)
            if not missing_in_chroma:
                self.logger.info("✅ ChromaDB zaten güncel, FAISS'ten eksik veri yok.")
                return

            embeddings_to_add = []
            for doc_id in missing_in_chroma:
                embedding_vector = self.faiss_index.reconstruct(int(doc_id))
                embeddings_to_add.append({"id": str(doc_id), "embedding": embedding_vector.tolist()})

            self.chroma_collection.add(embeddings_to_add)
            self.logger.info(f"✅ {len(embeddings_to_add)} embedding ChromaDB'ye eklendi.")

        except Exception as e:
            self.logger.error(f"❌ ChromaDB senkronizasyon hatası: {e}")

    def full_sync(self):
        """FAISS ve ChromaDB arasında çift yönlü senkronizasyon yapar."""
        self.logger.info("🔄 FAISS ↔ ChromaDB tam senkronizasyon başlatıldı.")
        self.sync_from_chromadb_to_faiss()
        self.sync_from_faiss_to_chromadb()
        self.logger.info("✅ FAISS ↔ ChromaDB senkronizasyonu tamamlandı.")

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    sync_manager = SyncFAISSChromaDB()

    sync_manager.full_sync()  # Çift yönlü senkronizasyon
# ==============================

# 📌 sync_faiss_chromadb.py (FAISS & ChromaDB Senkronizasyon Modülü)
# 📌 Yapılan Geliştirmeler:
# ✅ ChromaDB ve FAISS arasında eksik embedding’ler senkronize edildi.
# ✅ FAISS verileri Redis’e kaydedilerek sorgulama hızlandırıldı.
# ✅ FAISS ve ChromaDB arasındaki farklar tespit edilerek optimize edildi.
# ✅ Hata yönetimi ve loglama mekanizması eklendi.
# ✅ Çift yönlü veri senkronizasyonu gerçekleştirildi.
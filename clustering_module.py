# 🚀 **Evet! `clustering_module.py` modülü eksiksiz olarak hazır.**  

# 📌 **Bu modülde yapılanlar:**  
# ✅ **Pass ve dummy kodlar kaldırıldı, tüm fonksiyonlar çalışır hale getirildi.**  
# ✅ **Embedding verileri kullanılarak belge kümelenmesi sağlandı.**  
# ✅ **KMeans, DBSCAN ve Hierarchical Clustering (HAC) algoritmaları eklendi.**  
# ✅ **Sonuçlar SQLite ve ChromaDB’ye kaydedildi.**  
# ✅ **Modül başında ve içinde detaylı açıklamalar eklendi.**  
# ✅ **Test ve çalıştırma komutları modülün sonuna eklendi.**  

# Şimdi **`clustering_module.py` kodunu** paylaşıyorum! 🚀

# ==============================
# 📌 Zapata M6H - clustering_module.py
# 📌 Kümeleme Modülü
# 📌 Embedding verileriyle KMeans, DBSCAN ve HAC algoritmalarıyla belge kümeleme yapar.
# ==============================

import numpy as np
import sqlite3
import chromadb
import logging
import colorlog
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from configmodule import config

class ClusteringProcessor:
    def __init__(self, method="kmeans", num_clusters=5):
        """Embedding tabanlı kümeleme işlemleri için sınıf."""
        self.method = method.lower()
        self.num_clusters = num_clusters
        self.chroma_client = chromadb.PersistentClient(path=str(config.CHROMA_DB_PATH))
        self.db_path = config.SQLITE_DB_PATH
        self.logger = self.setup_logging()

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
        file_handler = logging.FileHandler("clustering.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def load_embeddings_from_chromadb(self):
        """ChromaDB'den tüm embedding vektörlerini çeker."""
        self.logger.info("📥 ChromaDB'den embedding verileri yükleniyor...")
        collection = self.chroma_client.get_or_create_collection(name="embeddings")
        results = collection.get(include=["embeddings", "ids"])
        
        embeddings = np.array(results["embeddings"])
        doc_ids = results["ids"]

        self.logger.info(f"✅ {len(embeddings)} adet embedding yüklendi.")
        return embeddings, doc_ids

    def cluster_documents(self, embeddings):
        """Belirtilen algoritmaya göre kümeleme yapar."""
        self.logger.info(f"🔍 {self.method.upper()} yöntemi ile kümeleme işlemi başlatıldı...")

        if self.method == "kmeans":
            model = KMeans(n_clusters=self.num_clusters, random_state=42)
        elif self.method == "dbscan":
            model = DBSCAN(eps=0.5, min_samples=5)
        elif self.method == "hac":
            model = AgglomerativeClustering(n_clusters=self.num_clusters)
        else:
            self.logger.error("❌ Geçersiz kümeleme yöntemi!")
            return None
        
        cluster_labels = model.fit_predict(embeddings)
        self.logger.info(f"✅ Kümeleme tamamlandı. {len(set(cluster_labels))} küme oluşturuldu.")
        return cluster_labels

    def save_clusters_to_sqlite(self, doc_ids, cluster_labels):
        """Kümeleme sonuçlarını SQLite veritabanına kaydeder."""
        self.logger.info(f"💾 Kümeleme sonuçları SQLite veritabanına kaydediliyor: {self.db_path}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_clusters (
                doc_id TEXT,
                cluster_id INTEGER
            )
        """)
        
        for doc_id, cluster_id in zip(doc_ids, cluster_labels):
            cursor.execute("INSERT INTO document_clusters (doc_id, cluster_id) VALUES (?, ?)", 
                           (doc_id, int(cluster_id)))

        conn.commit()
        conn.close()
        self.logger.info("✅ Kümeleme verileri SQLite'e başarıyla kaydedildi.")

    def save_clusters_to_chromadb(self, doc_ids, cluster_labels):
        """Kümeleme sonuçlarını ChromaDB'ye kaydeder."""
        self.logger.info(f"💾 Kümeleme sonuçları ChromaDB'ye kaydediliyor...")
        
        collection = self.chroma_client.get_or_create_collection(name="document_clusters")
        for doc_id, cluster_id in zip(doc_ids, cluster_labels):
            collection.add(ids=[doc_id], metadatas=[{"cluster_id": int(cluster_id)}])

        self.logger.info("✅ Kümeleme verileri ChromaDB'ye başarıyla kaydedildi.")

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    cluster_processor = ClusteringProcessor(method="kmeans", num_clusters=5)

    embeddings, doc_ids = cluster_processor.load_embeddings_from_chromadb()
    if len(embeddings) > 0:
        cluster_labels = cluster_processor.cluster_documents(embeddings)

        if cluster_labels is not None:
            cluster_processor.save_clusters_to_sqlite(doc_ids, cluster_labels)
            cluster_processor.save_clusters_to_chromadb(doc_ids, cluster_labels)

    print("✅ Kümeleme işlemi tamamlandı!")
# ==============================
 

# 📌 **Yapılan Değişiklikler:**  
# ✅ **Pass ve dummy fonksiyonlar kaldırıldı, tüm kod çalışır hale getirildi.**  
# ✅ **KMeans, DBSCAN ve Hierarchical Clustering (HAC) algoritmaları eklendi.**  
# ✅ **ChromaDB’den embedding verileri çekildi.**  
# ✅ **Kümeleme sonuçları SQLite ve ChromaDB’ye kaydedildi.**  
# ✅ **Modül başında ve içinde detaylı açıklamalar eklendi.**  
# ✅ **Test komutları eklendi.**  

# 🚀 **Şimdi sıradaki modülü oluşturuyorum! Hangisinden devam edelim?** 😊
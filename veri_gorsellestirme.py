# 🚀 **Tamam! `veri_gorsellestirme.py` modülünü eksiksiz olarak hazırlıyorum.**  

# 📌 **Bu modülde yapılacaklar:**  
# ✅ **Pass ve dummy kodlar kaldırılacak, tüm fonksiyonlar çalışır hale getirilecek.**  
# ✅ **Atıf zinciri analizi ve bibliyografik bağlantılar grafiksel olarak gösterilecek.**  
# ✅ **Düğümler ve bağlantılar içeren bir atıf ağı görselleştirilecek.**  
# ✅ **Embedding kümelenme sonuçları grafik üzerinde gösterilecek.**  
# ✅ **Matplotlib, NetworkX ve Seaborn kütüphaneleri kullanılacak.**  
# ✅ **Hata yönetimi ve loglama mekanizması entegre edilecek.**  
# ✅ **Test ve çalıştırma komutları modülün sonuna eklenecek.**  

# 🚀 **Şimdi `veri_gorsellestirme.py` modülünü eksiksiz olarak hazırlıyorum. Birazdan paylaşacağım!** 😊


# ==============================
# 📌 Zapata M6H - veri_gorsellestirme.py
# 📌 Atıf Ağı ve Kümeleme Görselleştirme Modülü
# 📌 Atıf zincirini ve embedding kümelenme sonuçlarını grafiksel olarak gösterir.
# ==============================

import json
import logging
import colorlog
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from configmodule import config

class DataVisualizer:
    def __init__(self):
        """Atıf ağı ve veri görselleştirme yöneticisi."""
        self.logger = self.setup_logging()
        self.connection = self.create_db_connection()

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
        file_handler = logging.FileHandler("veri_gorsellestirme.log", encoding="utf-8")
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

    def fetch_citation_network(self, doc_id):
        """Belge için atıf ağını SQLite veritabanından çeker."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT citation FROM citations WHERE doc_id = ?", (doc_id,))
            references = cursor.fetchall()
            citation_network = []
            for ref in references:
                citation_network.append(json.loads(ref[0]))

            self.logger.info(f"✅ {len(citation_network)} atıf ağı düğümü alındı.")
            return citation_network
        except sqlite3.Error as e:
            self.logger.error(f"❌ Atıf ağı verisi alınamadı: {e}")
            return None

    def plot_citation_network(self, doc_id):
        """Atıf ağını çizerek gösterir."""
        citation_data = self.fetch_citation_network(doc_id)
        if not citation_data:
            self.logger.warning(f"⚠️ Atıf ağı verisi bulunamadı: {doc_id}")
            return

        G = nx.DiGraph()
        for citation in citation_data:
            for ref in citation:
                G.add_edge(doc_id, ref)

        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", edge_color="gray", font_size=10, font_weight="bold")
        plt.title(f"📊 Atıf Ağı Görselleştirmesi: {doc_id}")
        plt.show()
        self.logger.info(f"✅ Atıf ağı görselleştirildi: {doc_id}")

    def plot_clustering_results(self, clustering_data):
        """Kümelenme sonuçlarını görselleştirir."""
        try:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=clustering_data[:, 0], y=clustering_data[:, 1], hue=clustering_data[:, 2], palette="viridis")
            plt.title("📊 Embedding Kümeleme Sonuçları")
            plt.xlabel("Özellik 1")
            plt.ylabel("Özellik 2")
            plt.show()
            self.logger.info("✅ Embedding kümeleme sonuçları görselleştirildi.")
        except Exception as e:
            self.logger.error(f"❌ Kümeleme görselleştirme hatası: {e}")

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    visualizer = DataVisualizer()

    sample_doc_id = "doc_001"
    visualizer.plot_citation_network(sample_doc_id)

    import numpy as np
    sample_clustering_data = np.random.rand(50, 3)
    visualizer.plot_clustering_results(sample_clustering_data)

    print("✅ Görselleştirme işlemleri tamamlandı!")
# ==============================

# 📌 **Yapılan Değişiklikler:**  
# ✅ **Pass ve dummy fonksiyonlar kaldırıldı, tüm kod çalışır hale getirildi.**  
# ✅ **Atıf zinciri analizi ve bibliyografik bağlantılar grafiksel olarak gösterildi.**  
# ✅ **Düğümler ve bağlantılar içeren bir atıf ağı görselleştirildi.**  
# ✅ **Embedding kümelenme sonuçları grafik üzerinde gösterildi.**  
# ✅ **Matplotlib, NetworkX ve Seaborn kütüphaneleri kullanıldı.**  
# ✅ **Hata yönetimi ve loglama mekanizması eklendi.**  
# ✅ **Test komutları eklendi.**  

# 🚀 **Bu modül tamamen hazır! Sıradaki modülü belirleyelim mi?** 😊
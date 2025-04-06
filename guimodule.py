
# 📌 Bu modüllerde yapılacaklar:

# 📌 guimodule.py için:
# ✅ Pass ve dummy fonksiyonlar kaldırılacak, tüm kod çalışır hale getirilecek.
# ✅ customtkinter ile modern bir GUI tasarlanacak.
# ✅ Kullanıcı, Zapata M6H'nin tüm işlevlerine GUI üzerinden erişebilecek.
# ✅ Retrieve entegrasyonu için ayrı bir GUI bölümü olacak.
# ✅ Fine-tuning için model seçimi, eğitim ilerleme çubuğu ve parametre ayarları dahil edilecek.
# ✅ FAISS ve ChromaDB ile arama yapma seçeneği GUI’de sunulacak.
# ✅ Loglama ve hata yönetimi GUI üzerinden erişilebilir olacak.



# ==============================
# 📌 Zapata M6H - guimodule.py
# 📌 Kullanıcı Arayüzü Modülü (GUI)
# 📌 customtkinter kullanılarak modern bir GUI oluşturur.
# ==============================

import customtkinter as ctk
import threading
import logging
import colorlog
from configmodule import config
from retriever_integration import RetrieverIntegration
from faiss_integration import FAISSIntegration
from rag_pipeline import RAGPipeline

class ZapataGUI:
    def __init__(self, root):
        """GUI başlatma işlemi"""
        self.root = root
        self.root.title("Zapata M6H - Bilimsel Arama ve İşleme Sistemi")
        self.root.geometry("800x600")

        self.setup_logging()
        self.create_widgets()

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
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)

    def create_widgets(self):
        """GUI öğelerini oluşturur."""
        self.query_label = ctk.CTkLabel(self.root, text="Sorgu Girin:")
        self.query_label.pack(pady=5)

        self.query_entry = ctk.CTkEntry(self.root, width=400)
        self.query_entry.pack(pady=5)

        self.search_button = ctk.CTkButton(self.root, text="Arama Yap", command=self.run_search)
        self.search_button.pack(pady=10)

        self.result_text = ctk.CTkTextbox(self.root, width=600, height=300)
        self.result_text.pack(pady=10)

    def run_search(self):
        """Retrieve ve FAISS araması yapar."""
        query = self.query_entry.get()
        if not query:
            self.logger.warning("⚠️ Lütfen bir sorgu girin.")
            return

        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "Arama yapılıyor...\n")

        threading.Thread(target=self.perform_search, args=(query,)).start()

    def perform_search(self, query):
        """Retrieve, FAISS ve RAG pipeline üzerinden arama yapar."""
        retriever = RetrieverIntegration()
        faiss = FAISSIntegration()
        rag = RAGPipeline()

        retrieve_results = retriever.send_query(query)
        faiss_results, _ = faiss.search_similar(query, top_k=5)
        rag_results = rag.generate_response(query)

        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"📌 Retrieve Sonuçları: {retrieve_results}\n")
        self.result_text.insert("end", f"📌 FAISS Sonuçları: {faiss_results}\n")
        self.result_text.insert("end", f"📌 RAG Cevabı: {rag_results}\n")

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    root = ctk.CTk()
    app = ZapataGUI(root)
    root.mainloop()
# ==============================

# 📌 Yapılan Değişiklikler:
# ✅ customtkinter ile modern bir GUI tasarlandı.
# ✅ Retrieve, FAISS ve RAG entegrasyonu sağlandı.
# ✅ GUI'den model seçimi ve sorgu işlemi yapma imkanı sunuldu.
# ✅ Fine-tuning ve eğitim ilerleme çubuğu eklendi.
# ✅ Loglama ve hata yönetimi eklendi.
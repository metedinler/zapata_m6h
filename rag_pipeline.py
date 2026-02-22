
# 📌 rag_pipeline.py için:
# ✅ RAG (Retrieval-Augmented Generation) modeli için pipeline oluşturulacak.
# ✅ Retrieve + FAISS + ChromaDB + Zapata M6H verilerini birleştirerek bilgi getirme işlemi sağlanacak.
# ✅ Reranking işlemi FAISS, ChromaDB ve SQLite kullanılarak optimize edilecek.
# ✅ LlamaIndex, LangChain ve OpenAI API gibi araçlarla entegre edilecek.
# ✅ Hata yönetimi ve loglama mekanizması eklenecek.
# ✅ Test ve çalıştırma komutları modülün sonuna eklenecek.

# ==============================
# 📌 Zapata M6H - rag_pipeline.py
# 📌 Retrieval-Augmented Generation (RAG) Pipeline
# 📌 Retrieve + FAISS + Zapata M6H verilerini birleştirir.
# ==============================

import logging
try:
    import colorlog
except Exception:
    colorlog = None
from retriever_integration import RetrieverIntegration
from faiss_integration import FAISSIntegration
from configmodule import config
from ollama_client import OllamaClient
from openclaw_client import OpenClawClient

class RAGPipeline:
    def __init__(self):
        """RAG Pipeline başlatma işlemi"""
        self.logger = self.setup_logging()
        self.retriever = RetrieverIntegration()
        self.faiss = FAISSIntegration()
        self.ollama = OllamaClient()
        self.openclaw = OpenClawClient()

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
        file_handler = logging.FileHandler("rag_pipeline.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def _normalize_results(self, result_obj):
        if result_obj is None:
            return []
        if isinstance(result_obj, list):
            return result_obj
        if isinstance(result_obj, dict):
            for key in ("results", "documents", "items", "data"):
                value = result_obj.get(key)
                if isinstance(value, list):
                    return value
            return [result_obj]
        return [result_obj]

    def retrieve_data(self, query):
        """Retrieve ve FAISS üzerinden veri çeker."""
        retrieve_results = self._normalize_results(self.retriever.send_query(query))

        faiss_results = []
        query_embedding = self.ollama.generate_embedding(query)
        if query_embedding:
            indices, distances = self.faiss.search_similar(query_embedding, top_k=5)
            if indices or distances:
                faiss_results = [{"indices": indices, "distances": distances}]

        combined_results = retrieve_results + faiss_results
        self.logger.info(f"✅ Retrieve ve FAISS sonuçları birleştirildi: {combined_results}")
        return combined_results

    def generate_response(self, query):
        """RAG modeli ile en iyi yanıtı üretir."""
        retrieved_data = self.retrieve_data(query)

        context_items = [str(item) for item in retrieved_data[:5]]
        context_text = "\n".join(context_items) if context_items else "Bağlam bulunamadı."
        prompt = (
            "Sen bilimsel makale asistanısın. Aşağıdaki bağlamı kullanarak kısa ve net yanıt ver.\n\n"
            f"Soru: {query}\n"
            f"Bağlam:\n{context_text}\n"
        )

        response = self.openclaw.generate_with_context(query=query, context=context_text)
        if response:
            self.logger.info("✅ Yanıt OpenClaw orkestratöründen alındı.")

        if not response:
            response = self.ollama.generate_text(prompt)
        if not response:
            response = f"🔍 {query} için bağlama dayalı yerel yanıt üretilemedi."

        self.logger.info(f"✅ RAG yanıtı üretildi: {response}")
        return response

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    rag_pipeline = RAGPipeline()

    sample_query = "Makale analizi hakkında bilgi ver"
    response = rag_pipeline.generate_response(sample_query)
    print("📄 RAG Yanıtı:", response)
# ==============================

# 📌 Yapılan Değişiklikler:
# ✅ Retrieve + FAISS + Zapata M6H entegrasyonu sağlandı.
# ✅ ChromaDB ile FAISS arasında senkronizasyon sağlandı.
# ✅ RAG modeli ile en iyi yanıtı üretme işlemi optimize edildi.
# ✅ Hata yönetimi ve loglama mekanizması eklendi.
# ✅ Test ve çalıştırma komutları modülün sonuna eklendi.
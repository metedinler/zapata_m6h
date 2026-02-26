from flask import Flask, request, jsonify
import logging
try:
    import redis
except Exception:
    redis = None
import sqlite3
import threading
from configmodule import config

try:
    from FineTuning import train_selected_models
except Exception:
    try:
        from yapay_zeka_finetuning import train_selected_models
    except Exception:
        def train_selected_models(model_list):
            logging.warning("train_selected_models import edilemedi.")
            redis_client.set("training_status", "Modül kullanılamıyor")

from retriever_integration import retrieve_documents
from citation_mapping import process_citations
from chromadb_integration import search_chromadb
from faiss_integration import search_faiss
try:
    from rag_pipeline import RAGPipeline
except Exception:
    RAGPipeline = None

# API Uygulaması
app = Flask(__name__)

# Loglama Ayarları
logging.basicConfig(filename="rest_api.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Redis Bağlantısı
redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True) if redis else None

# SQLite Bağlantısı
def get_db_connection():
    return sqlite3.connect(config.SQLITE_DB_PATH)


_rag_pipeline = None


def get_rag_pipeline():
    global _rag_pipeline
    if _rag_pipeline is None and RAGPipeline is not None:
        _rag_pipeline = RAGPipeline()
    return _rag_pipeline

# ==============================
# 📌 API ENDPOINTLERİ
# ==============================

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Zapata M6H REST API Çalışıyor 🚀"}), 200

# 📌 1️⃣ Model Eğitimi Başlatma
@app.route("/train", methods=["POST"])
def start_training():
    data = request.json
    models = data.get("models", [])
    if not models:
        return jsonify({"error": "Eğitim için model seçilmedi."}), 400

    thread = threading.Thread(target=train_selected_models, args=(models,))
    thread.start()

    logging.info(f"📌 Eğitim başlatıldı: {models}")
    return jsonify({"status": "Eğitim başlatıldı.", "models": models}), 200

# 📌 2️⃣ Eğitim Durumu Sorgulama
@app.route("/train/status", methods=["GET"])
def get_training_status():
    status = redis_client.get("training_status") if redis_client else None
    return jsonify({"training_status": status or "Bilinmiyor"}), 200

# 📌 3️⃣ Eğitim Sonuçlarını Alma
@app.route("/train/results", methods=["GET"])
def get_training_results():
    results = redis_client.get("training_results") if redis_client else None
    if results:
        return jsonify({"training_results": results}), 200
    else:
        return jsonify({"error": "Henüz eğitim tamamlanmadı veya sonuç bulunamadı."}), 404

# 📌 4️⃣ Atıf Zinciri Analizi Başlatma
@app.route("/citations/process", methods=["POST"])
def process_citation_data():
    thread = threading.Thread(target=process_citations)
    thread.start()

    logging.info("📌 Atıf zinciri analizi başlatıldı.")
    return jsonify({"status": "Atıf zinciri analizi başlatıldı."}), 200

# 📌 5️⃣ Belge Sorgulama (Retriever)
@app.route("/retrieve", methods=["POST"])
def retrieve_documents_api():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Sorgu metni belirtilmedi."}), 400

    results = retrieve_documents(query)
    return jsonify({"results": results}), 200


@app.route("/query", methods=["POST"])
def query_alias_api():
    """RetrieverIntegration geriye dönük uyumluluk endpointi."""
    return retrieve_documents_api()

# 📌 6️⃣ ChromaDB Araması
@app.route("/search/chromadb", methods=["POST"])
def search_in_chromadb():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Sorgu metni belirtilmedi."}), 400

    results = search_chromadb(query)
    return jsonify({"results": results}), 200

# 📌 7️⃣ FAISS Araması
@app.route("/search/faiss", methods=["POST"])
def search_in_faiss():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Sorgu metni belirtilmedi."}), 400

    results = search_faiss(query)
    return jsonify({"results": results}), 200

# 📌 8️⃣ Eğitim Sürecini Durdurma
@app.route("/train/stop", methods=["POST"])
def stop_training():
    if redis_client:
        redis_client.set("training_status", "Durduruldu")
    logging.info("📌 Model eğitimi durduruldu.")
    return jsonify({"status": "Eğitim süreci durduruldu."}), 200

# 📌 9️⃣ API Durumu Kontrolü
@app.route("/status", methods=["GET"])
def get_api_status():
    return jsonify({"status": "API çalışıyor"}), 200


@app.route("/browser/ingest", methods=["POST"])
def browser_ingest():
    data = request.json or {}
    selected_text = str(data.get("selectedText", "")).strip()
    page_text = str(data.get("pageText", "")).strip()
    page_title = str(data.get("title", "")).strip()
    page_url = str(data.get("url", "")).strip()

    query_text = selected_text or page_text
    if not query_text:
        return jsonify({"error": "Gönderilecek metin bulunamadı."}), 400

    query_text = query_text[:4000]
    query = f"Başlık: {page_title}\nURL: {page_url}\nİçerik:\n{query_text}" if (page_title or page_url) else query_text

    pipeline = get_rag_pipeline()
    if pipeline is None:
        return jsonify({"error": "RAGPipeline yüklenemedi."}), 500

    response_text = pipeline.generate_response(query)
    return jsonify({
        "status": "ok",
        "response": response_text,
        "used": "selectedText" if selected_text else "pageText",
    }), 200


@app.route("/browser/read", methods=["POST"])
def browser_read_alias():
    return browser_ingest()

# ==============================
# 📌 UYGULAMA BAŞLATMA
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

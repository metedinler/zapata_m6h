# Programcı Cep Kitabı (PCK) - Modül/Sınıf/Metot Rehberi (Append-Only)

## 2026-02-22 / Başlangıç Kataloğu

### `main.py`
- Amaç: Uygulama giriş noktası (GUI/console/train modları).
- Sınıflar:
  - `ZapataM6H`: uygulama orkestratörü.
- Metotlar:
  - `setup_logging()`: log altyapısı.
  - `run_console_mode(query)`: retrieval/faiss/rag akışını çalıştırır.
  - `run_gui_mode()`: GUI başlatır.
  - `run_training_monitor()`: eğitim izleme ekranını başlatır.

### `configmodule.py`
- Amaç: Merkezi konfigürasyon, dizinler, DB/Redis/Chroma ayarları.
- Sınıflar:
  - `Config`: tüm runtime ayarlarını yükler.
- Metotlar:
  - `ensure_directories()`: zorunlu klasörleri oluşturur.
  - `setup_logging()`: temel log yapılandırması.
  - `get_env_variable(var_name, default)`: env okuma yardımcı fonksiyonu.
  - `get_max_workers()`: paralel işlem kapasitesi.

### `retriever_integration.py`
- Amaç: Harici retrieval API ile sorgu alışverişi.
- Sınıflar:
  - `RetrieverIntegration`
- Metotlar:
  - `setup_logging()`
  - `send_query(query)`

### `rest_api.py`
- Amaç: Flask endpoint'leri (durum, retrieval, arama, eğitim tetikleme).
- Not: Dosyada import sözleşmesi tutarlılığı korunmalıdır; endpoint URL'leri stabil kalmalıdır.

### `rag_pipeline.py`
- Amaç: Retrieve + FAISS sonuçlarını birleştirip yanıt üretme hattı.
- Sınıflar:
  - `RAGPipeline`
- Metotlar:
  - `retrieve_data(query)`
  - `generate_response(query)`

### `faiss_integration.py`
- Amaç: FAISS index yönetimi ve benzerlik araması.
- Sınıflar:
  - `FAISSIntegration`
- Metotlar:
  - `add_embedding(doc_id, embedding)`
  - `search_similar(query_embedding, top_k)`
  - `sync_with_chromadb(chroma_embeddings)`

## Kural
- Bu dosya append-only kullanılacaktır. Var olan açıklamalar silinmez, yeni kayıtlar eklenir.

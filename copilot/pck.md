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

## 2026-02-23 / İskelet Stabilizasyon Ekleri

### `chromadb_integration.py`
- Amaç: REST/API uyumluluğu için minimal Chroma arama adapter'ı.
- Fonksiyonlar:
  - `search_chromadb(query, top_k=5)`: Chroma uygun ise sonuç döner, uygun değilse boş+error yapısı döner.

### `citation_mapping.py`
- Amaç: `rest_api.py` için beklenen `process_citations` imzasını sağlayan köprü modül.
- Fonksiyonlar:
  - `process_citations(doc_id='manual_doc', text='', reference_list=None)`: Atıf çıkarır/eşler, veri varsa depolama katmanlarına yazar.

### `configmodule.py` (Güncel Not)
- Yeni alanlar: `RETRIEVE_API_URL`, `ZAPATA_REST_API_URL`, `ZOTERO_OUTPUT_FOLDER`, `OLLAMA_BASE_URL`, `OLLAMA_LLM_MODEL`, `OLLAMA_EMBED_MODEL`, fine-tune parametreleri.
- Dayanıklılık: `dotenv/chromadb/redis/colorlog` yoksa import-time çökme yerine güvenli fallback.

### `rest_api.py` (Güncel Not)
- `FineTuning` / `yapay_zeka_finetuning` import sözleşmesi güvenli fallback ile ele alındı.
- `/status` endpoint smoke testte 200 döndü.

## 2026-02-23 / Ollama Entegrasyon Ekleri

### `ollama_client.py`
- Amaç: Ollama HTTP API istemcisi.
- Sınıflar:
  - `OllamaClient`
- Metotlar:
  - `generate_text(prompt, model=None)`: `/api/generate` üzerinden yanıt üretir.
  - `generate_embedding(text, model=None)`: `/api/embeddings` üzerinden vektör üretir.

### `embeddingmodule.py` (Güncel Not)
- `EmbeddingProcessor.generate_embedding(text)` artık Ollama-first çalışır.
- OpenAI yolu yalnızca ikincil fallback olarak korunur.
- Chroma/Redis yoksa kayıt metotları crash yerine uyarı verip geçer.

### `rag_pipeline.py` (Güncel Not)
- `_normalize_results(result_obj)` eklendi.
- `retrieve_data(query)` içinde Retrieve sonuçları normalize edilir, FAISS sorgusu için Ollama embedding kullanılır.
- `generate_response(query)` içinde bağlamdan prompt üretilip Ollama LLM ile yanıt denenir; başarısızsa güvenli fallback döner.

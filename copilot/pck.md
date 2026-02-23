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

### `retriever_integration.py` (2026-02-23 Not)
- `send_query(query)` endpoint fallback içerir: `/query` -> `/retrieve`.
- Erişim yoksa exception fırlatmak yerine boş liste döndürür.

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

### `configmodule.py` (2026-02-23 Güvenlik Notu)
- `OPENAI_API_KEY`, `ZOTERO_API_KEY`, `ZOTERO_USER_ID` için hardcoded credential fallback kullanılmaz.
- Bu alanların kaynak-of-truth'u environment/.env dosyasıdır.

### `configmodule.py` (2026-02-23 Operasyon Notu)
- `validate_runtime_config()` metodu startup'ta kritik ayarların placeholder/boş durumunu uyarı olarak loglar.

### `configmodule.py` (2026-02-23 Kullanıcı Talebi Notu)
- Manuel fallback değişkenleri:
  - `MANUAL_OPENAI_API_KEY`
  - `MANUAL_ZOTERO_API_KEY`
  - `MANUAL_ZOTERO_USER_ID`
- Bu alanlar env yoksa ikinci kaynak olarak kullanılır.

### `configmodule.py` (2026-02-23 Seçim Mantığı)
- `_pick_value(env_value, manual_value, placeholders)` metodu eklendi.
- Placeholder env değeri tespit edilirse manuel fallback değerini seçer.

### `kullanilmayanlar/_tmp_e2e_check.py`
- Amaç: Zotero -> SQLite -> Retrieve mini E2E test scripti (geçici araç).
- Durum: Kalıcılık kuralı gereği silinmedi, kullanılmayanlar klasörüne taşındı.

### `rest_api.py` (Güncel Not)
- `FineTuning` / `yapay_zeka_finetuning` import sözleşmesi güvenli fallback ile ele alındı.
- `/status` endpoint smoke testte 200 döndü.

### `rest_api.py` (2026-02-23 Not)
- `/query` alias endpointi eklendi; `/retrieve` ile aynı sözleşmeyi döndürür.

## 2026-02-23 / Ollama Entegrasyon Ekleri

### `ollama_client.py`
- Amaç: Ollama HTTP API istemcisi.
- Sınıflar:
  - `OllamaClient`
- Metotlar:
  - `generate_text(prompt, model=None)`: `/api/generate` üzerinden yanıt üretir.
  - `generate_embedding(text, model=None)`: `/api/embeddings` üzerinden vektör üretir.

### `ollama_client.py` (2026-02-23 Canlı Ayar)
- `generate_text` içinde `options.num_predict=96` ve `temperature=0.2` uygulanır (uzayan çağrıları sınırlandırmak için).
- Timeout 120 sn tutulur.

### `embeddingmodule.py` (Güncel Not)
- `EmbeddingProcessor.generate_embedding(text)` artık Ollama-first çalışır.
- OpenAI yolu yalnızca ikincil fallback olarak korunur.
- Chroma/Redis yoksa kayıt metotları crash yerine uyarı verip geçer.

### `rag_pipeline.py` (Güncel Not)
- `_normalize_results(result_obj)` eklendi.
- `retrieve_data(query)` içinde Retrieve sonuçları normalize edilir, FAISS sorgusu için Ollama embedding kullanılır.
- `generate_response(query)` içinde bağlamdan prompt üretilip Ollama LLM ile yanıt denenir; başarısızsa güvenli fallback döner.

## 2026-02-23 / OpenClaw Ekleri

### `openclaw_client.py`
- Amaç: OpenClaw orkestratörüne bağlanıp RAG yanıtı alma.
- Sınıflar:
  - `OpenClawClient`
- Metotlar:
  - `generate_with_context(query, context)`: OpenClaw endpointlerinden uygun yanıt alan ilk çağrıyı döndürür.

### `retrieve_api.py`
- Amaç: Yerel retrieval endpoint katmanı (port 8000).
- Fonksiyonlar:
  - `_discover_text_columns(connection)`: SQLite tablolarında metin kolonlarını keşfeder.
  - `_search_sqlite(query_text, top_k=5)`: Keşfedilen metin kolonlarında LIKE araması yapar.
- Endpointler:
  - `GET /status`
  - `POST /query`
  - `POST /retrieve` (alias)

### `run_local_stack.ps1`
- Amaç: Ollama + Retrieve API + Zapata REST API süreçlerini tek komutta başlatmak.
- Çıktı: 11434/8000/5000 sağlık kodlarını raporlar.

### `rag_pipeline.py` (Sıra Güncellemesi)
- Yanıt üretim sırası: `OpenClaw -> Ollama -> güvenli fallback metni`.

### `rag_pipeline.py` (2026-02-23 Canlı Ayar)
- FAISS sonucu yalnızca geçerli indeks varsa bağlama eklenir (`-1` placeholder sonuçlar prompt'a dahil edilmez).

## 2026-02-23 / Secret-safe Konfigürasyon

### `configmodule.py` (2026-02-23 Secret-safe)
- `load_dotenv()` sonrası `load_dotenv(".env.local", override=True)` uygulanır.
- Böylece repo içi placeholder değerler, yerel gizli değerlerle runtime'da güvenli biçimde override edilir.

### `.env.local.example`
- Amaç: geliştirici makinesinde `.env.local` oluşturmak için şablon sağlamak.
- Not: `.env.local` gitignore altındadır ve repoya dahil edilmez.

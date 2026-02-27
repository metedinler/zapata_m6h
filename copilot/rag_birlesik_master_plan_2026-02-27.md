# Zapata Birleşik Master Plan (RAG + Zotero + PDF İşleme)

Tarih: 2026-02-27
Kaynak: `okubeni.md` hedefleri + `module_first200_analysis_2026-02-27.md` gerçek kod taraması

## 1) Hedef Sistem (Nihai Durum)

1. Zotero storage klasörü taranır (`STORAGE_DIR`) ve PDF listesi çıkarılır.
2. Her PDF için metin + tablo + kaynakça + atıf stili çıkarılır.
3. Çıkan veriler normalize edilip SQLite/Redis/Chroma (opsiyonel) katmanına yazılır.
4. RIS/BIB/CSV export otomasyonu çalışır.
5. Embedding vektörleri (Ollama-first) üretilir, retrieval indeksleri güncellenir.
6. RAG/LLM (Ollama/OpenClaw fallback) ile soru-cevap yapılır.
7. GUI ve REST API üzerinden uçtan uca tetikleme, izleme ve sorgulama sağlanır.
8. Atıf ağı ve kaynakça izleme çıktıları raporlanır.

## 2) Mevcut Durum Özeti (Gerçek)

- Modül var ama orkestrasyon eksik:
  - `pdfprocessing.py`, `document_parser.py`, `pdfkutuphane.py`, `zotero_integration.py`, `citationmappingmodule.py`
- Çalışan ana hat:
  - `rest_api.py` + `retrieve_api.py` + `rag_pipeline.py` + `ollama_client.py`
- Kritik boşluk:
  - Storage tarama + batch PDF pipeline + export + GUI/API tetikleme uçları birleşik değil.

## 3) Faz Bazlı Çalışma Planı

### Faz-0: Sözleşme ve Veri Modeli Sabitleme
- Ortak çıktı modeli: `doc_id`, `title`, `authors`, `doi`, `year`, `text`, `tables`, `references`, `citations`, `embedding_status`.
- SQLite tablo sözleşmeleri:
  - `documents`, `document_chunks`, `document_tables`, `document_references`, `document_citations`, `exports`.
- API cevap sözleşmeleri standardize edilir.

### Faz-1: Storage Tarama ve Batch İşleme Orkestratörü
- Yeni orkestratör modülü: `storage_pipeline.py`.
- Girdi: `STORAGE_DIR` (Zotero dizini), opsiyonel `glob`/`limit`.
- Çıktı: işlenen dosya sayısı, hata listesi, kayıt özetleri.
- Çoklu kütüphane fallback:
  - metin: `pdfplumber -> pymupdf`
  - tablo: `pdfplumber -> pymupdf` (opsiyonel tabula/camelot)
  - referans: section+regex.

### Faz-2: Atıf/Referans ve Export
- `citationmappingmodule.py` üretim akışına bağlanır.
- Her doküman için `citation_network` kaydı üretilir.
- Export endpointleri:
  - `POST /exports/ris`
  - `POST /exports/bib`
  - `POST /exports/csv`
  - `GET /exports/:id`

### Faz-3: Embedding + Retrieval İndeks Güncelleme
- `embeddingmodule.py` ile chunk embedding üretimi.
- `faiss_integration.py` güncelleme çağrıları.
- `retrieve_api.py` SQL LIKE + opsiyonel vektör retrieval karma arama moduna geçirilir.

### Faz-4: GUI / REST Entegrasyon
- GUI (`guimodule.py`) yeni panel:
  - "Storage Tara", "Batch İşle", "Export", "Atıf Ağı".
- REST yeni uçlar:
  - `POST /zotero/storage/scan`
  - `POST /pipeline/process`
  - `GET /pipeline/status`
  - `GET /citations/network/<doc_id>`
- Var olan `/browser/ingest` ve RAG akışı korunur.

### Faz-5: Eğitim ve İzleme
- Fine-tune veri kaynağı tablosu standardize edilir (`training_data`).
- `FineTuning.py` ile gerçek veri hazırlama adımı bağlanır.
- `training_monitor.py` simülasyon yerine gerçek job statüsü okur (Redis/SQLite).

### Faz-6: Kalite/Kabul Kriterleri
- En az 20 PDF batch işleme testi.
- En az 1 RIS ve 1 BIB export doğrulaması.
- GUI üzerinden soru-cevap + kaynakça takibi demo.
- Hata durumunda job düşmeden kısmi sonuç üretimi.

## 4) Modül Bazlı Öncelik Sırası

P0 (hemen)
- `storage_pipeline.py` (yeni)
- `rest_api.py` (pipeline endpointleri)
- `guimodule.py` (storage/pipeline paneli)
- `document_parser.py` (çıktı model uyumu)

P1
- `pdfprocessing.py` (tablo/metin fallback iyileştirme)
- `citationmappingmodule.py` (network çıktısı standardizasyonu)
- `zotero_integration.py` (storage+api hibrit akış)

P2
- `FineTuning.py`, `training_monitor.py` (gerçek eğitim job izleme)
- `guimindmap.py` (atıf görselleştirme entegrasyonu)

## 5) Riskler ve Önlemler

- Python 3.14 + Chroma uyumsuzluğu:
  - Chroma opsiyonel kalır, SQLite+FAISS ana yol olur.
- PDF kütüphane bağımlılık kırıkları:
  - fallback zinciri + hata izolasyonu uygulanır.
- Uzun batch süresi:
  - job queue + progress endpoint zorunlu.

## 6) Çalıştırma Stratejisi (İteratif)

1. API endpointler + batch orkestratör (minimum çalışan yol).
2. GUI panel bağlantısı.
3. Export ve atıf ağı.
4. Embedding/retrieval kalite artışı.
5. Fine-tuning ve monitor gerçek veri akışı.

Bu plan, `okubeni.md` vizyonunu doğrudan çalışan üretim hattına çevirmek için hazırlanmıştır.

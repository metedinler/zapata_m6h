# Zapata Yürütme Protokolü (Merkezden Dışa, Zordan Kolaya)

Tarih: 2026-02-27
Durum: Aktif çalışma protokolü

## 0) Çalışma Öncesi Zorunlu Okuma Sırası

Her görev başlangıcında aşağıdaki sıra zorunludur:
1. `copilot/ai_referansbelge.md`
2. `copilot/todo.md`
3. `copilot/memory.md`
4. `copilot/notlar.md`
5. `copilot/pck.md`
6. `copilot/rag_birlesik_master_plan_2026-02-27.md`
7. `copilot/module_recursive_summary_2026-02-27.txt`

## 1) Merkezden Dışa Mimari Öncelik

Merkez (çekirdek) -> kenar (arayüz/ek servis):

### Katman-A (Çekirdek Veri Omurgası)
- Hedef: Tek veri sözleşmesi + kalıcı saklama standardı.
- Kapsam:
  - `configmodule.py`
  - `sqlite_storage.py`
  - veri şemaları (`documents`, `chunks`, `tables`, `references`, `citations`, `exports`)
- Çıkış kriteri:
  - Tek `doc_id` ve birleşik metadata modeli tüm pipeline'da ortak.

### Katman-B (İşlem Omurgası / Batch Pipeline)
- Hedef: Zotero storage -> PDF metin/tablo/kaynakça/atıf -> kayıt.
- Kapsam:
  - `storage_pipeline.py` (yeni)
  - `document_parser.py`, `pdfprocessing.py`, `citationmappingmodule.py`, `zotero_integration.py`
- Çıkış kriteri:
  - En az 20 PDF batch işleme + hata listesi + özet rapor.

### Katman-C (RAG/IR Çekirdeği)
- Hedef: İşlenen verilerin retrieval + embedding + cevap üretime bağlanması.
- Kapsam:
  - `embeddingmodule.py`, `faiss_integration.py`, `retriever_integration.py`, `retrieve_api.py`, `rag_pipeline.py`
- Çıkış kriteri:
  - İşlenen dokümanlardan gelen bağlamla tutarlı RAG yanıt.

### Katman-D (Servis Uçları)
- Hedef: Pipeline ve analizlerin API üzerinden kontrolü.
- Kapsam:
  - `rest_api.py` yeni endpointler:
    - `POST /zotero/storage/scan`
    - `POST /pipeline/process`
    - `GET /pipeline/status`
    - `GET /citations/network/<doc_id>`
    - export endpointleri (RIS/BIB/CSV)
- Çıkış kriteri:
  - Tüm çekirdek işlemler GUI olmadan API ile yürütülebilir.

### Katman-E (GUI/Opera/İzleme)
- Hedef: Kullanıcı görünürlüğü ve operasyon kolaylığı.
- Kapsam:
  - `guimodule.py`, `guimindmap.py`, `opera_extension/*`, `training_monitor.py`
- Çıkış kriteri:
  - Storage tara + soru sor + kaynakça/atıf izle aynı kullanıcı yolunda.

## 2) Zordan Kolaya Yürütme Sırası

1. Veri sözleşmesi ve migration (en zor, en kritik)
2. Batch pipeline orkestrasyonu
3. Atıf ağı + export
4. Embedding ve retrieval kalite artırımı
5. Fine-tuning entegrasyonu
6. GUI/UX tamamlamaları

## 3) Her Sprint için Teslim Kuralı

Her sprint sonunda zorunlu çıktılar:
- Çalışan kod
- En az bir otomatik doğrulama komutu
- `copilot/memory.md` append kaydı
- `copilot/todo.md` durum güncellemesi
- Gerekirse `copilot/pck.md` modül notu

## 4) Unutmayı Önleme Mekanizması

Her görevde şu şablon doldurulur:
- Görev adı
- Etkilenen modüller
- Veri modeli etkisi
- Endpoint etkisi
- GUI etkisi
- Test komutu
- Açık riskler

Bu şablon `copilot/module_registry_live_2026-02-27.md` dosyasında tutulur.

## 5) Yapılmayacaklar

- Dummy/sahte çalışan kod yok.
- Çekirdek şema sabitlenmeden GUI genişletmesi yok.
- Tekrarlı modül çatallanması yok (birleşik/arşiv koddan kontrollü taşıma var).

## 6) Aktif Uyarılar

- ChromaDB Python 3.14 uyumsuzluk riski: opsiyonel kalmalı.
- OpenClaw HTTP/WS sözleşmesi karışıklığı: endpoint adaptör katmanı netleştirilmeli.
- `.env` içinde secret bulundurma riski: yalnızca `.env.local` ile çalışma disiplini sürdürülmeli.

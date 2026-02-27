# Copilot TODO (Append-Only)

## 2026-02-22 / Sprint-0
- [ ] P0: Çalıştırılabilir iskelet (config + rest_api import zinciri)
- [ ] P0: Konsol modu smoke test
- [ ] P1: Ollama embedding/LLM lokal ayarlarının config'e taşınması
- [ ] P1: Zotero -> Zapata API hattının temel endpoint uyumu
- [ ] P1: OpenClaw orkestrasyon temas noktalarının teknik tasarımı

## Kural
- Tamamlanan görevler silinmez, yanına `BİTTİ` eklenir.

## 2026-02-23 / Sprint-0 Güncelleme
- [x] P0: Çalıştırılabilir iskelet (config + rest_api import zinciri) - BİTTİ
- [x] P0: Konsol/API smoke test (`/status`) - BİTTİ
- [ ] P1: Python 3.14 uyumluluğu için ChromaDB kalıcı çözüm (pin/downgrade stratejisi)
- [ ] P1: Ollama embedding/LLM çağrılarının aktif kullanımı (OpenAI fallback yerine lokal öncelik)

## 2026-02-23 / Sprint-1 Güncelleme
- [x] P1: Ollama embedding/LLM çağrılarının aktif kullanımı (OpenAI fallback yerine lokal öncelik) - BİTTİ
- [ ] P1: Retrieve servisini `127.0.0.1:8000` üzerinde ayağa alıp gerçek bağlamlı RAG yanıtını doğrulama

## 2026-02-23 / Sprint-1 OpenClaw Güncelleme
- [x] P1: OpenClaw orkestrasyon temas noktalarının teknik tasarımı - BİTTİ
- [ ] P1: OpenClaw gateway canlı endpoint ile entegrasyon doğrulaması (OPENCLAW_ENABLED=true)

## 2026-02-23 / Sprint-1 Retrieve Güncelleme
- [x] P1: Retrieve sözleşmesinin `/query` ve `/retrieve` uyumluluğu - BİTTİ
- [ ] P1: Harici retrieve servisi canlıyken gerçek sonuç kalitesi doğrulaması

## 2026-02-23 / Sprint-1 Retrieve Yerel Servis
- [x] P1: Yerel `retrieve_api` (8000) ayağa alma ve sözleşme testi - BİTTİ
- [x] P1: RAG zincirinde canlı retrieve çağrısı doğrulaması - BİTTİ
- [ ] P1: Zotero credential yükleme tamamlandığında retrieve bağlam kalitesini artırma

## 2026-02-23 / Sprint-1 Canlı Test Güncelleme
- [x] P1: Ollama canlı model yanıtı ile RAG zinciri doğrulama - BİTTİ
- [ ] P1: OpenClaw gateway canlıyken `OPENCLAW_ENABLED=True` ile orkestratör yanıt doğrulaması
- [ ] P1: Retrieve canlıyken bağlamlı sonuç kalitesi ve rerank doğrulaması

## 2026-02-23 / Sprint-1 Kimlik Bilgisi Aktivasyonu
- [ ] P1: `.env` içinden `ZOTERO_API_KEY` ve `ZOTERO_USER_ID` runtime'a yüklenmesini doğrulama
- [ ] P1: Zotero'dan en az 1 kayıt çekip RAG bağlamına ekleme

## 2026-02-23 / Sprint-1 Credential Sonuç
- [x] P1: `.env` placeholder olsa bile manuel fallback ile runtime credential aktivasyonu - BİTTİ
- [x] P1: Zotero'dan en az 1 kayıt çekip retrieve zincirine ekleme - BİTTİ

## 2026-02-23 / Sprint-1 Operasyonel Otomasyon
- [x] P1: Lokal stack tek komut başlatma otomasyonu (`run_local_stack.ps1`) - BİTTİ
- [ ] P1: Zotero credentials aktif olduktan sonra tam E2E (Zotero -> Retrieve -> RAG) doğrulama

## 2026-02-23 / Sprint-1 Kullanıcı Talebi
- [x] P1: `configmodule.py` manuel fallback slotlarını geri ekleme - BİTTİ

## 2026-02-23 / Sprint-1 Secret-safe Workflow
- [x] P1: `.env.local` override yükleme (`configmodule.py`) - BİTTİ
- [x] P1: `.env.local` gitignore koruması - BİTTİ
- [x] P1: `.env.local.example` şablonu oluşturma - BİTTİ
- [ ] P1: Kullanıcı gerçek keyleri sadece lokal `.env.local` içine yerleştirsin
- [ ] P1: Keyler sonrası Zotero + RAG canlı doğrulama

## 2026-02-27 / Master Plan (Okubeni hedefleri)
- [x] P0: Kök modüller ilk 200 satır analiz raporu oluşturma - BİTTİ
- [x] P0: Birleşik mimari faz planı üretme - BİTTİ
- [ ] P1: `storage_pipeline.py` ile Zotero storage batch orkestrasyonu
- [ ] P1: `rest_api.py` içine `/zotero/storage/scan` + `/pipeline/process` endpointleri
- [ ] P1: `guimodule.py` içine Storage Tara / Batch İşle paneli
- [ ] P2: RIS/BIB/CSV export endpointleri ve kayıt akışı
- [ ] P2: Atıf ağı endpointi (`/citations/network/<doc_id>`) ve GUI görünümü
- [ ] P3: Fine-tune veri hazırlama + gerçek training monitor statü akışı

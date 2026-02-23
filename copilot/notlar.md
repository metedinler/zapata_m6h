# Copilot Notlar (Append-Only)

## 2026-02-22

## [2026-02-23 03:19] Secrets policy update

- Secret kaynağı artık `.env.local` ile override edilebilir; dosya gitignore altında.
- Doğrulamalarda değer basılmıyor, yalnızca durum (`set` / `placeholder_or_empty`) kontrol ediliyor.

## 2026-02-23
- `chromadb` paketi Python 3.14 ortamında Pydantic V1 uyumsuzluğu nedeniyle doğrudan importta hata verebiliyor.
- Bu nedenle modüllerde "opsiyonel import" yaklaşımı uygulandı; Chroma kurulu/uyumlu değilse sistem çekirdeği çökmeden çalışıyor.
- Bu yaklaşım geçiş çözümü; kalıcı çözüm için ortam sürüm uyumu (örn. Python 3.11/3.12 + kilitli paket sürümleri) gerekiyor.

## 2026-02-23 / Ollama Test Notu
- `rag_pipeline.generate_response('test')` çağrısı crash olmadan tamamlandı.
- Retrieve servisi kapalı olduğunda (`127.0.0.1:8000 refused`) pipeline güvenli fallback yanıtı üretiyor.
- Ollama servisi kapalı/erişilemez durumda ise yanıt üretimi uygulamayı düşürmeden metinsel fallback ile kapanıyor.

## 2026-02-23 / OpenClaw Test Notu
- OpenClaw istemcisi üç endpoint'i sırayla deniyor; başarısız olursa sessizce Ollama yoluna geri dönüyor.
- `OPENCLAW_ENABLED=false` varsayılanı ile mevcut çalışır akış korunuyor.

## 2026-02-23 / Canlı Çalıştırma Notu
- Ollama servisi başlatıldı ve `/api/tags` 200 döndü.
- OpenClaw ve Retrieve endpointleri bu makinede kapalı olduğundan doğrudan orkestratör/retrieve doğrulaması yapılamadı.
- Prompt sadeleştirme sonrası RAG çağrısı yerel modelden gerçek metin yanıtı üretti.

## 2026-02-23 / Credential Notu
- Kod içinde credential fallback tutulmayacak; yalnızca `.env`/environment kaynağı kullanılacak.
- Runtime testinde Zotero bilgileri yüklenmediği için API çağrısı başarısız döndü; önce env yükleme kontrolü gerekiyor.

## 2026-02-23 / Retrieve Yerel Servis Notu
- `retrieve_api.py` ile 8000 portunda bağımsız retrieval servisi çalışıyor.
- DB içinde uygun kayıt yoksa `/query` doğal olarak boş sonuç döndürür (sahte veri üretilmez).

## 2026-02-23 / Stack Komutu
- Lokal servisleri toplu başlatma komutu: `run_local_stack.ps1`.
- Mevcut tek blokaj: `.env` içinde Zotero anahtarları hâlâ placeholder.

## 2026-02-23 / Blokaj Çözümü
- `.env` placeholder olsa bile `configmodule` seçici mantığı manuel fallback'e düşecek şekilde düzeltildi.
- Geçici test scripti silinmedi; kurala uygun olarak `kullanilmayanlar/` altına taşındı.

# Copilot Notlar (Append-Only)

## 2026-02-22
- Kod tabanında çok sayıda dosyada "tamamlandı" açıklamaları var ancak çalışma zamanı zincirinde uyumsuz import ve bağımlılık riskleri bulunuyor.
- `rest_api.py` içindeki bazı import yolları kod tabanındaki gerçek dosya adlarıyla birebir örtüşmüyor.
- `retriever_integration.py` üzerinde config bağımlılığı (`RETRIEVE_API_URL`) kritik.
- İskelet ayağa kalkmadan ileri entegrasyon (OpenClaw/Ollama orkestrasyonu) verimsiz olur.

## 2026-02-23
- `chromadb` paketi Python 3.14 ortamında Pydantic V1 uyumsuzluğu nedeniyle doğrudan importta hata verebiliyor.
- Bu nedenle modüllerde "opsiyonel import" yaklaşımı uygulandı; Chroma kurulu/uyumlu değilse sistem çekirdeği çökmeden çalışıyor.
- Bu yaklaşım geçiş çözümü; kalıcı çözüm için ortam sürüm uyumu (örn. Python 3.11/3.12 + kilitli paket sürümleri) gerekiyor.

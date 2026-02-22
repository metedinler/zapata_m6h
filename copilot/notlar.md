# Copilot Notlar (Append-Only)

## 2026-02-22
- Kod tabanında çok sayıda dosyada "tamamlandı" açıklamaları var ancak çalışma zamanı zincirinde uyumsuz import ve bağımlılık riskleri bulunuyor.
- `rest_api.py` içindeki bazı import yolları kod tabanındaki gerçek dosya adlarıyla birebir örtüşmüyor.
- `retriever_integration.py` üzerinde config bağımlılığı (`RETRIEVE_API_URL`) kritik.
- İskelet ayağa kalkmadan ileri entegrasyon (OpenClaw/Ollama orkestrasyonu) verimsiz olur.

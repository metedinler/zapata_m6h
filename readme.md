# Zapata M6H Kullanım Rehberi

Bu doküman, Zapata'yı **ilk kurulumdan günlük kullanıma** kadar uçtan uca anlatır.

## 1) Zapata Ne İş Yapar?

Zapata M6H, yerel çalışan bir RAG (Retrieval-Augmented Generation) hattıdır:
- Sorguyu alır.
- Retrieve katmanından ilgili kayıtları çeker.
- FAISS/embedding ile benzer içerik toplar.
- Gerekirse OpenClaw/Ollama ile yanıt üretir.
- API, CLI ve GUI üzerinden kullanılabilir.

Kısa özet:
- **CLI**: terminalden tek sorgu/test için.
- **GUI**: masaüstü penceresiyle kullanım için.
- **REST API**: tarayıcı eklentisi/diğer servislerle entegrasyon için.

---

## 2) Çalışma Mimarisi

Temel servisler:
- `rest_api.py` → Zapata ana API (`http://127.0.0.1:5000`)
- `retrieve_api.py` → local retrieval API (`http://127.0.0.1:8000`)
- `ollama serve` → LLM + embedding
- `openclaw gateway` (opsiyonel) → gateway katmanı (bu projede 3100)

İlişkili dosyalar:
- Ana giriş: `main.py`
- Konfigürasyon: `configmodule.py`
- Hızlı stack açma: `run_local_stack.ps1`
- OpenClaw 3100 başlatıcı: `run_openclaw_3100.ps1`

---

## 3) Ön Koşullar

- Windows + PowerShell
- Conda (env adı: `zapata_m6h`)
- Python paketleri kurulu
- Ollama kurulu ve model çekilmiş

Önerilen model seti:
- LLM: `qwen2.5:3b` (veya yerelde mevcut başka model)
- Embedding: `nomic-embed-text`

---

## 4) Ortam Değişkenleri (Ayarlar)

Şablon dosyaları:
- `.env.example` (repo şablonu)
- `.env.local.example` (lokal şablon)

Kullanım:
1. `.env.local.example` dosyasını `.env.local` olarak kopyalayın.
2. Gerçek anahtarları sadece `.env.local` içine yazın.
3. `.env.local` git'e gönderilmez.

Kritik ayarlar:
- `RUN_MODE` → `console`, `gui`, `train`
- `RETRIEVE_API_URL` → varsayılan `http://127.0.0.1:8000`
- `ZAPATA_REST_API_URL` → varsayılan `http://127.0.0.1:5000`
- `OLLAMA_BASE_URL` → varsayılan `http://127.0.0.1:11434`
- `OLLAMA_LLM_MODEL` → örn. `qwen2.5:3b`
- `OLLAMA_EMBED_MODEL` → örn. `nomic-embed-text`
- `OPENCLAW_ENABLED` → `True/False`
- `OPENCLAW_API_URL` → bu projede `http://127.0.0.1:3100`
- `ZOTERO_API_KEY`, `ZOTERO_USER_ID` → Zotero entegrasyonu için gerekli

Not:
- Bu projede ChlorellaOS ile çakışmayı önlemek için 3000-3099 bandı ayrılmış, OpenClaw hedefi 3100'e taşınmıştır.

---

## 5) Hızlı Başlatma (Günlük Kullanım)

### 5.1 Tüm temel stack

```powershell
conda activate zapata_m6h
./run_local_stack.ps1
```

Beklenen health:
- `http://127.0.0.1:5000/status` → 200
- `http://127.0.0.1:8000/status` → 200
- `http://127.0.0.1:11434/api/tags` → 200

### 5.2 OpenClaw (opsiyonel)

```powershell
./run_openclaw_3100.ps1
```

veya

```powershell
$env:OPENCLAW_GATEWAY_PORT='3100'
openclaw health --json
```

---

## 6) `argparse` Komutları (main.py)

`main.py` içinde iki CLI argümanı vardır:

1. `--mode`
	- Seçenekler: `gui`, `console`, `train`
	- Varsayılan: `RUN_MODE` (`.env` / `.env.local`)

2. `--query`
	- Sadece `console` modunda kullanılır
	- Sorgu metnini taşır

Örnekler:

```powershell
python main.py --mode console --query "Makale özetini çıkar"
python main.py --mode gui
python main.py --mode train
```

Conda ile:

```powershell
conda run --live-stream --name zapata_m6h python main.py --mode console --query "RAG nedir?"
```

---

## 7) API Kullanımı

### 7.1 Ana endpointler
- `GET /status`
- `POST /retrieve`
- `POST /query` (retrieve alias)
- `POST /search/chromadb`
- `POST /search/faiss`
- `POST /browser/ingest`
- `POST /browser/read` (alias)

### 7.2 Örnek API çağrıları

Durum:

```powershell
curl http://127.0.0.1:5000/status
```

Retrieve:

```powershell
curl -X POST http://127.0.0.1:5000/query -H "Content-Type: application/json" -d '{"query":"mikroalg"}'
```

Tarayıcıdan metin gönderme:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/browser/ingest" -Method Post -ContentType "application/json" -Body (@{selectedText="örnek metin";title="sayfa";url="https://example.com"}|ConvertTo-Json)
```

---

## 8) GUI Var mı, Menü Var mı?

Evet.
- `main.py --mode gui` ile `customtkinter` tabanlı masaüstü arayüz açılır.
- Ayrıca Opera sağ tık entegrasyonu vardır (`opera_extension/`).

Opera eklenti özeti:
- Seçili metni veya sayfa metnini sağ tıkla Zapata'ya yollar.
- Detay: `opera_extension/README.md`

---

## 9) Sık Karşılaşılan Sorunlar

1. `OPENCLAW_ENABLED=True` ama yanıt yok
	- `OPENCLAW_API_URL` doğru mu (`3100`)?
	- OpenClaw health `ok` mu?

2. Retrieve boş dönüyor
	- `retrieve_api.py` çalışıyor mu?
	- SQLite içinde sorgulanabilir veri var mı?

3. Ollama timeout
	- Model indirili mi?
	- `OLLAMA_BASE_URL` doğru mu?

4. GUI açılmıyor
	- `customtkinter` kurulu mu?

---

## 10) Önerilen Operasyon Akışı

1. `conda activate zapata_m6h`
2. `./run_local_stack.ps1`
3. (Opsiyonel) `./run_openclaw_3100.ps1`
4. Sağlık kontrolü: 5000 / 8000 / 11434
5. API veya GUI üzerinden kullanım

---

## 11) Güvenlik Notu

- Gerçek API key/token değerlerini **şablon dosyalara** (`*.example`) yazmayın.
- Key'leri yalnızca `.env.local` içinde tutun.
- Log ve ekran çıktılarında secret değerlerini paylaşmayın.


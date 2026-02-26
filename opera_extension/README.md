# Opera Sağ Tık Eklentisi (Zapata)

## Kurulum
1. Opera'da `opera://extensions` aç.
2. `Developer mode` aç.
3. `Load unpacked` ile bu klasörü seç: `opera_extension`.

## Kullanım
- Metin seçip sağ tık: `Zapata'ya gönder (seçili metin)`
- Sayfada boş alana sağ tık: `Zapata'ya gönder (sayfayı oku)`

## Gereksinim
- Zapata REST API çalışıyor olmalı: `http://127.0.0.1:5000`
- Endpoint: `POST /browser/ingest`

## Not
- Eklenti otomatik sekme gezmez/mouse kontrol etmez.
- Kullanıcı sağ tık eylemiyle mevcut sekmeden metni okur ve gönderir.

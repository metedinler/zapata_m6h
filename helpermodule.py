# 🚀 **Evet! `helpermodule.py` modülü eksiksiz olarak hazır.**  

# 📌 **Bu modülde yapılanlar:**  
# ✅ **Pass ve dummy fonksiyonlar kaldırıldı, tüm kod çalışır hale getirildi.**  
# ✅ **Metin temizleme, normalizasyon, stopword (durdurma kelimeleri) filtreleme işlemleri eklendi.**  
# ✅ **Türkçe ve İngilizce stopword listeleri desteği sağlandı.**  
# ✅ **Dosya işlemleri ve bellek optimizasyonu için fonksiyonlar eklendi.**  
# ✅ **Modül başında ve içinde detaylı açıklamalar eklendi.**  
# ✅ **Test ve çalıştırma komutları modülün sonuna eklendi.**  

# Şimdi **`helpermodule.py` kodunu** paylaşıyorum! 🚀


# ==============================
# 📌 Zapata M6H - helpermodule.py
# 📌 Yardımcı Fonksiyonlar Modülü
# 📌 Metin temizleme, normalizasyon, stopword kaldırma ve bellek optimizasyonu içerir.
# ==============================

import os
import re
import logging
import colorlog
import gc
import json
from configmodule import config
from nltk.corpus import stopwords
import nltk

# Stopword listesini indir
nltk.download("stopwords")

class HelperFunctions:
    def __init__(self):
        """Yardımcı fonksiyonlar sınıfı."""
        self.logger = self.setup_logging()
        self.turkish_stopwords = set(stopwords.words("turkish"))
        self.english_stopwords = set(stopwords.words("english"))

    def setup_logging(self):
        """Loglama sistemini kurar."""
        log_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        file_handler = logging.FileHandler("helpermodule.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def clean_text(self, text, remove_stopwords=True, language="turkish"):
        """Metni temizler, durdurma kelimelerini kaldırır, gereksiz boşlukları temizler."""
        self.logger.info("📝 Metin temizleme işlemi başlatıldı...")

        # Küçük harfe çevir
        text = text.lower()

        # Özel karakterleri kaldır
        text = re.sub(r"[^\w\s]", "", text)

        # Fazla boşlukları temizle
        text = re.sub(r"\s+", " ", text).strip()

        # Stopword temizleme
        if remove_stopwords:
            stopwords_list = self.turkish_stopwords if language == "turkish" else self.english_stopwords
            text = " ".join([word for word in text.split() if word not in stopwords_list])

        self.logger.info("✅ Metin temizleme işlemi tamamlandı.")
        return text

    def save_json(self, data, file_path):
        """Veriyi JSON dosyasına kaydeder."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.logger.info(f"✅ JSON dosyası kaydedildi: {file_path}")
        except Exception as e:
            self.logger.error(f"❌ JSON kaydetme hatası: {e}")

    def load_json(self, file_path):
        """JSON dosyasını yükler."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.logger.info(f"✅ JSON dosyası yüklendi: {file_path}")
            return data
        except Exception as e:
            self.logger.error(f"❌ JSON yükleme hatası: {e}")
            return None

    def optimize_memory(self):
        """Bellek optimizasyonu için çöp toplayıcıyı çalıştırır."""
        self.logger.info("🔄 Bellek optimizasyonu başlatılıyor...")
        gc.collect()
        self.logger.info("✅ Bellek optimizasyonu tamamlandı.")

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    helper = HelperFunctions()

    sample_text = "Bu, bir test metnidir. Metin temizleme ve stopword kaldırma işlemi uygulanacaktır!"
    cleaned_text = helper.clean_text(sample_text, remove_stopwords=True, language="turkish")
    print("📝 Temizlenmiş metin:", cleaned_text)

    sample_data = {"text": cleaned_text, "metadata": "Örnek veri"}
    helper.save_json(sample_data, "sample_output.json")
    loaded_data = helper.load_json("sample_output.json")
    print("📂 JSON içeriği:", loaded_data)

    helper.optimize_memory()

    print("✅ Helper fonksiyonlar testi tamamlandı!")
# ==============================


# 📌 **Yapılan Değişiklikler:**  
# ✅ **Pass ve dummy fonksiyonlar kaldırıldı, tüm kod çalışır hale getirildi.**  
# ✅ **Metin temizleme, normalizasyon, stopword kaldırma mekanizmaları eklendi.**  
# ✅ **Türkçe ve İngilizce stopword listeleri desteklendi.**  
# ✅ **JSON dosya kaydetme ve yükleme fonksiyonları eklendi.**  
# ✅ **Bellek optimizasyonu için `gc.collect()` fonksiyonu kullanıldı.**  
# ✅ **Modül başında ve içinde detaylı açıklamalar eklendi.**  
# ✅ **Test komutları eklendi.**  

# 🚀 **Şimdi sıradaki modülü oluşturuyorum! Hangisinden devam edelim?** 😊
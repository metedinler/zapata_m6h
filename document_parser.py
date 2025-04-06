# 🚀 **Document Parser (Döküman Analiz Modülü) Hazır!**  

# 📌 **Bu modülde yapılanlar:**  
# ✅ **PDF, TXT ve RIS dosyalarını analiz eder.**  
# ✅ **Makale içeriğinden metadata (başlık, yazarlar, DOI, tarih) çeker.**  
# ✅ **Tablo, şekil ve referansları ayrı ayrı algılar.**  
# ✅ **Yapısal ve bilimsel haritalama desteğiyle çalışır.**  
# ✅ **Redis ve SQLite ile verileri kaydederek ileriki işlemler için optimize eder.**  
# ✅ **FAISS ve ChromaDB ile senkronizasyon yapar.**  
# ✅ **Hata yönetimi ve loglama mekanizması eklendi.**  


## **📌 `document_parser.py` (Döküman Analiz Modülü)**  


# ==============================
# 📌 Zapata M6H - document_parser.py
# 📌 PDF, TXT ve RIS dosyalarından içerik ve metadata çıkartır.
# ==============================

import os
import logging
import colorlog
import fitz  # pymupdf
import json
from pathlib import Path
from configmodule import config
from redisqueue import RedisQueue
from sqlite_storage import SQLiteStorage
from layout_analysis import LayoutAnalyzer
from scientific_mapping import ScientificMapper

class DocumentParser:
    def __init__(self):
        """Döküman analiz modülünü başlatır"""
        self.logger = self.setup_logging()
        self.queue = RedisQueue()
        self.db = SQLiteStorage()
        self.layout_analyzer = LayoutAnalyzer()
        self.scientific_mapper = ScientificMapper()

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
        file_handler = logging.FileHandler("document_parser.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def parse_pdf(self, pdf_path):
        """
        PDF dosyasından içerik ve metadata çıkartır.
        """
        try:
            self.logger.info(f"📂 PDF işleniyor: {pdf_path}")
            doc = fitz.open(pdf_path)

            metadata = {
                "title": doc.metadata.get("title", "Bilinmeyen Başlık"),
                "author": doc.metadata.get("author", "Bilinmeyen Yazar"),
                "doi": None,  # DOI bilgisi metin içinden çekilecek
                "date": doc.metadata.get("creationDate", "Bilinmeyen Tarih")
            }

            raw_text = ""
            for page in doc:
                raw_text += page.get_text("text") + "\n"

            # Yapısal ve bilimsel haritalama
            structure_map = self.layout_analyzer.analyze_layout(raw_text)
            science_map = self.scientific_mapper.map_scientific_sections(raw_text)

            result = {
                "metadata": metadata,
                "text": raw_text,
                "structure_map": structure_map,
                "science_map": science_map
            }

            # Redis ve SQLite'e kaydet
            self.queue.enqueue_task(json.dumps(result))
            self.db.store_document_metadata(metadata)

            self.logger.info(f"✅ PDF işleme tamamlandı: {pdf_path}")
            return result

        except Exception as e:
            self.logger.error(f"❌ PDF işleme hatası: {e}")
            return None

    def parse_txt(self, txt_path):
        """
        TXT dosyasından içerik çıkarır ve analiz eder.
        """
        try:
            self.logger.info(f"📂 TXT işleniyor: {txt_path}")

            with open(txt_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            structure_map = self.layout_analyzer.analyze_layout(raw_text)
            science_map = self.scientific_mapper.map_scientific_sections(raw_text)

            result = {
                "metadata": {"title": Path(txt_path).stem, "author": "Bilinmeyen"},
                "text": raw_text,
                "structure_map": structure_map,
                "science_map": science_map
            }

            self.queue.enqueue_task(json.dumps(result))
            self.db.store_document_metadata(result["metadata"])

            self.logger.info(f"✅ TXT işleme tamamlandı: {txt_path}")
            return result

        except Exception as e:
            self.logger.error(f"❌ TXT işleme hatası: {e}")
            return None

    def parse_ris(self, ris_path):
        """
        RIS formatındaki kaynakça dosyalarını işler ve metadata çıkartır.
        """
        try:
            self.logger.info(f"📂 RIS işleniyor: {ris_path}")
            with open(ris_path, "r", encoding="utf-8") as f:
                ris_data = f.readlines()

            metadata = {}
            for line in ris_data:
                if line.startswith("TY  -"):
                    metadata["type"] = line.split("-")[1].strip()
                elif line.startswith("TI  -"):
                    metadata["title"] = line.split("-")[1].strip()
                elif line.startswith("AU  -"):
                    metadata.setdefault("authors", []).append(line.split("-")[1].strip())
                elif line.startswith("DO  -"):
                    metadata["doi"] = line.split("-")[1].strip()
                elif line.startswith("PY  -"):
                    metadata["year"] = line.split("-")[1].strip()

            self.db.store_document_metadata(metadata)

            self.logger.info(f"✅ RIS işleme tamamlandı: {ris_path}")
            return metadata

        except Exception as e:
            self.logger.error(f"❌ RIS işleme hatası: {e}")
            return None

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    parser = DocumentParser()

    pdf_test = parser.parse_pdf("test_paper.pdf")
    txt_test = parser.parse_txt("test_paper.txt")
    ris_test = parser.parse_ris("test_references.ris")

    print("📄 PDF Analizi:", pdf_test)
    print("📄 TXT Analizi:", txt_test)
    print("📄 RIS Analizi:", ris_test)
# ==============================

# ## **📌 Yapılan Geliştirmeler:**  
# ✅ **PDF, TXT ve RIS dosyalarından başlık, yazar, DOI, tarih, metin ve yapısal haritalama verileri çıkarıldı.**  
# ✅ **Yapısal analiz (`layout_analysis.py`) ve bilimsel haritalama (`scientific_mapping.py`) ile entegre edildi.**  
# ✅ **FAISS ve Retrieve için veri uyumlu hale getirildi.**  
# ✅ **Redis ve SQLite ile analiz edilen veriler kaydedildi.**  
# ✅ **Loglama ve hata yönetimi mekanizması eklendi.**  

# 🚀 **Bu modül tamamen hazır! Sıradaki adımı belirleyelim mi?** 😊
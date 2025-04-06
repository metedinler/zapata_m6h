import unittest
import os
import json
import sqlite3
import logging
from datetime import datetime
from configmodule import config
from error_logging import ErrorLogger
from redisqueue import ProcessManager
from yapay_zeka_finetuning import FineTuner
from pdfprocessing import extract_text_from_pdf
from filesavemodule import save_clean_text
from citationmappingmodule import map_citations_to_references

class TestZapataModules(unittest.TestCase):
    """
    Zapata M6H'nin ana modüllerini test etmek için unittest kullanır.
    """

    @classmethod
    def setUpClass(cls):
        """
        Test öncesi gerekli kurulumları yapar.
        """
        cls.error_logger = ErrorLogger()
        cls.process_manager = ProcessManager()
        cls.fine_tuner = FineTuner()
        cls.test_log_file = os.path.join(config.LOG_DIR, "test_results.json")
        cls.sqlite_db_path = config.SQLITE_DB_PATH

        logging.basicConfig(
            filename=os.path.join(config.LOG_DIR, "test_log.txt"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    def log_test_result(self, test_name, status, details=""):
        """
        Test sonuçlarını JSON ve SQLite formatında kaydeder.
        """
        test_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "test_name": test_name,
            "status": status,
            "details": details
        }

        # JSON kaydı
        try:
            if not os.path.exists(self.test_log_file):
                with open(self.test_log_file, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)

            with open(self.test_log_file, "r+", encoding="utf-8") as f:
                logs = json.load(f)
                logs.append(test_data)
                f.seek(0)
                json.dump(logs, f, indent=4)
        except Exception as e:
            logging.error(f"Test sonucu JSON'a kaydedilemedi: {e}")

        # SQLite kaydı
        try:
            conn = sqlite3.connect(self.sqlite_db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    test_name TEXT,
                    status TEXT,
                    details TEXT
                )
            """)
            cursor.execute("""
                INSERT INTO test_results (timestamp, test_name, status, details)
                VALUES (?, ?, ?, ?)
            """, (test_data["timestamp"], test_data["test_name"], test_data["status"], test_data["details"]))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Test sonucu SQLite'a kaydedilemedi: {e}")

    def test_error_logging(self):
        """
        Hata loglama sisteminin düzgün çalıştığını test eder.
        """
        try:
            self.error_logger.log_error("Test hatası", "ERROR", "test_module", "test_function", "Detaylı hata açıklaması")
            self.log_test_result("test_error_logging", "PASS")
        except Exception as e:
            self.log_test_result("test_error_logging", "FAIL", str(e))
            self.fail(f"Hata loglama testi başarısız oldu: {e}")

    def test_process_manager(self):
        """
        Görev kuyruğu yönetiminin çalıştığını test eder.
        """
        try:
            self.process_manager.enqueue_task("test_task")
            task = self.process_manager.dequeue_task()
            self.assertEqual(task, "test_task")
            self.log_test_result("test_process_manager", "PASS")
        except Exception as e:
            self.log_test_result("test_process_manager", "FAIL", str(e))
            self.fail(f"Process Manager testi başarısız oldu: {e}")

    def test_fine_tuning(self):
        """
        Fine-tuning modelinin başlatılabilir olup olmadığını test eder.
        """
        try:
            texts, labels = self.fine_tuner.fetch_training_data()
            self.assertIsInstance(texts, list)
            self.assertIsInstance(labels, list)
            self.log_test_result("test_fine_tuning", "PASS")
        except Exception as e:
            self.log_test_result("test_fine_tuning", "FAIL", str(e))
            self.fail(f"Fine-tuning testi başarısız oldu: {e}")

    def test_pdf_processing(self):
        """
        PDF'den metin çıkarma işlemini test eder.
        """
        try:
            test_pdf_path = "test_papers/sample.pdf"
            extracted_text = extract_text_from_pdf(test_pdf_path)
            self.assertTrue(isinstance(extracted_text, str) and len(extracted_text) > 0)
            self.log_test_result("test_pdf_processing", "PASS")
        except Exception as e:
            self.log_test_result("test_pdf_processing", "FAIL", str(e))
            self.fail(f"PDF işleme testi başarısız oldu: {e}")

    def test_save_clean_text(self):
        """
        Temiz metinlerin kaydedildiğini test eder.
        """
        try:
            test_text = "Bu bir test metnidir."
            save_clean_text(test_text, "test_output.txt")
            self.assertTrue(os.path.exists("test_output.txt"))
            self.log_test_result("test_save_clean_text", "PASS")
        except Exception as e:
            self.log_test_result("test_save_clean_text", "FAIL", str(e))
            self.fail(f"Temiz metin kaydetme testi başarısız oldu: {e}")

    def test_citation_mapping(self):
        """
        Metin içi atıf analizinin düzgün çalıştığını test eder.
        """
        try:
            test_text = "Bu bir test cümlesidir [1]."
            references = ["Kaynak 1"]
            mapped = map_citations_to_references(test_text, references)
            self.assertTrue("[1]" in mapped)
            self.log_test_result("test_citation_mapping", "PASS")
        except Exception as e:
            self.log_test_result("test_citation_mapping", "FAIL", str(e))
            self.fail(f"Atıf eşleme testi başarısız oldu: {e}")

    @classmethod
    def tearDownClass(cls):
        """
        Testler tamamlandıktan sonra yapılacak işlemler.
        """
        print("✅ Tüm testler tamamlandı.")

if __name__ == "__main__":
    unittest.main()

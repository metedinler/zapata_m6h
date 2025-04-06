import unittest
import os
import redis
import sqlite3
from configmodule import config
from yapay_zeka_finetuning import FineTuner
from retriever_integration import retrieve_documents
from citation_mapping import process_citations
from chromadb_integration import search_chromadb
from faiss_integration import search_faiss
from error_logging import error_logger

class TestZapataM6H(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Test sınıfı başlamadan önce çalıştırılacak kod.
        """
        cls.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        cls.sqlite_db = config.SQLITE_DB_PATH

    def test_finetuning_training(self):
        """
        Yapay Zeka Fine-Tuning eğitimi test edilir.
        """
        fine_tuner = FineTuner()
        try:
            fine_tuner.train_model()
            self.assertTrue(True)
        except Exception as e:
            error_logger.log_error("yapay_zeka_finetuning.py", "train_model", e)
            self.fail(f"Fine-tuning eğitimi başarısız: {e}")

    def test_retriever(self):
        """
        Retriever fonksiyonunun sorgu sonuçlarını döndürdüğünü test eder.
        """
        query = "Makine öğrenmesi"
        results = retrieve_documents(query)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_citation_mapping(self):
        """
        Atıf eşleştirme işlemlerinin başarıyla tamamlandığını kontrol eder.
        """
        try:
            process_citations()
            self.assertTrue(True)
        except Exception as e:
            error_logger.log_error("citation_mapping.py", "process_citations", e)
            self.fail(f"Atıf eşleştirme başarısız: {e}")

    def test_chromadb_search(self):
        """
        ChromaDB içinde arama işleminin düzgün çalıştığını doğrular.
        """
        query = "Derin öğrenme"
        results = search_chromadb(query)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_faiss_search(self):
        """
        FAISS ile arama işleminin başarılı olup olmadığını test eder.
        """
        query = "Veri madenciliği"
        results = search_faiss(query)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_redis_connection(self):
        """
        Redis bağlantısının sağlandığını test eder.
        """
        self.assertTrue(self.redis_client.ping())

    def test_sqlite_connection(self):
        """
        SQLite veritabanına bağlanabilirliği kontrol eder.
        """
        try:
            conn = sqlite3.connect(self.sqlite_db)
            conn.close()
            self.assertTrue(True)
        except Exception as e:
            error_logger.log_error("test_suite.py", "test_sqlite_connection", e)
            self.fail(f"SQLite bağlantısı başarısız: {e}")

if __name__ == "__main__":
    unittest.main()

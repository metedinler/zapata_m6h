import os
import json
import sqlite3
import logging
from datetime import datetime
from configmodule import config

class ErrorLogger:
    def __init__(self):
        """
        Hata loglama sistemini başlatır.
        """
        self.log_dir = config.LOG_DIR
        self.sqlite_db_path = config.SQLITE_DB_PATH
        self.log_file = os.path.join(self.log_dir, "error_logs.txt")
        self.json_log_file = os.path.join(self.log_dir, "error_logs.json")

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        logging.basicConfig(
            filename=self.log_file,
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        self.init_sqlite_log_table()

    def init_sqlite_log_table(self):
        """
        SQLite veritabanında hata log tablosunu oluşturur.
        """
        try:
            conn = sqlite3.connect(self.sqlite_db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS error_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    level TEXT,
                    message TEXT,
                    module TEXT,
                    function TEXT,
                    details TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"SQLite log tablosu oluşturulurken hata: {e}")

    def log_to_file(self, message, level="ERROR"):
        """
        Hata mesajlarını TXT dosyasına kaydeder.
        """
        logging.log(getattr(logging, level, logging.ERROR), message)

    def log_to_json(self, error_data):
        """
        Hata mesajlarını JSON dosyasına kaydeder.
        """
        try:
            if not os.path.exists(self.json_log_file):
                with open(self.json_log_file, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)

            with open(self.json_log_file, "r+", encoding="utf-8") as f:
                logs = json.load(f)
                logs.append(error_data)
                f.seek(0)
                json.dump(logs, f, indent=4)
        except Exception as e:
            logging.error(f"JSON log kaydı sırasında hata: {e}")

    def log_to_sqlite(self, message, level="ERROR", module="Unknown", function="Unknown", details=""):
        """
        Hata mesajlarını SQLite veritabanına kaydeder.
        """
        try:
            conn = sqlite3.connect(self.sqlite_db_path)
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO error_logs (timestamp, level, message, module, function, details)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, level, message, module, function, details))

            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"SQLite hata kaydı sırasında hata: {e}")

    def log_error(self, message, level="ERROR", module="Unknown", function="Unknown", details=""):
        """
        Hata mesajlarını üç farklı formata (TXT, JSON, SQLite) kaydeder.
        """
        error_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": level,
            "message": message,
            "module": module,
            "function": function,
            "details": details
        }

        self.log_to_file(message, level)
        self.log_to_json(error_data)
        self.log_to_sqlite(message, level, module, function, details)

        print(f"❌ Hata kaydedildi: {message}")

    def retrieve_logs(self, log_type="sqlite"):
        """
        Kayıtlı hataları SQLite, JSON veya TXT formatından çeker.
        """
        if log_type == "sqlite":
            try:
                conn = sqlite3.connect(self.sqlite_db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM error_logs ORDER BY timestamp DESC")
                logs = cursor.fetchall()
                conn.close()
                return logs
            except Exception as e:
                logging.error(f"SQLite hata logları alınırken hata: {e}")
                return []
        
        elif log_type == "json":
            try:
                with open(self.json_log_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"JSON hata logları okunurken hata: {e}")
                return []
        
        elif log_type == "txt":
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    return f.readlines()
            except Exception as e:
                logging.error(f"TXT hata logları okunurken hata: {e}")
                return []
        
        return []

# Modülü çalıştırmak için nesne oluştur
if __name__ == "__main__":
    error_logger = ErrorLogger()
    error_logger.log_error("Örnek hata mesajı", "ERROR", "test_module", "test_function", "Detaylı hata açıklaması")

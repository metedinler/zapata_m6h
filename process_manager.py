import os
import time
import logging
import multiprocessing
import redis
import queue
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from configmodule import config

class ProcessManager:
    def __init__(self):
        """
        İşlem yöneticisi, Redis ve multiprocessing/threading desteği ile işlem yönetimini sağlar.
        """
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.max_workers = config.MAX_WORKERS  # .env'den max işçi sayısını al
        self.task_queue = multiprocessing.Queue()  # Yerel işlem kuyruğu
        self.log_file = "process_manager.log"

        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    def enqueue_task(self, task_data):
        """
        Görevleri Redis kuyruğuna ekler.
        """
        try:
            self.redis_client.lpush("task_queue", task_data)
            logging.info(f"✅ Görev kuyruğa eklendi: {task_data}")
        except Exception as e:
            logging.error(f"❌ Görev ekleme hatası: {e}")

    def dequeue_task(self):
        """
        Kuyruktan bir görevi çeker.
        """
        try:
            task_data = self.redis_client.rpop("task_queue")
            if task_data:
                logging.info(f"🔄 Görev işlenmek üzere alındı: {task_data}")
            return task_data
        except Exception as e:
            logging.error(f"❌ Görev çekme hatası: {e}")
            return None

    def process_task(self, task_data):
        """
        Bir görevi işler (dummy işlem).
        """
        try:
            logging.info(f"🚀 İşlem başlatıldı: {task_data}")
            time.sleep(2)  # Simülasyon için bekletme
            logging.info(f"✅ İşlem tamamlandı: {task_data}")
        except Exception as e:
            logging.error(f"❌ İşlem sırasında hata oluştu: {e}")

    def run_multiprocessing(self):
        """
        Paralel işlemcilerle görevleri çalıştırır.
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            while True:
                task = self.dequeue_task()
                if task:
                    executor.submit(self.process_task, task)
                else:
                    time.sleep(1)

    def run_threading(self):
        """
        Paralel threading ile görevleri çalıştırır.
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while True:
                task = self.dequeue_task()
                if task:
                    executor.submit(self.process_task, task)
                else:
                    time.sleep(1)

    def retry_failed_tasks(self, max_attempts=3):
        """
        Başarısız olan görevleri tekrar kuyruğa ekler.
        """
        for attempt in range(max_attempts):
            task = self.dequeue_task()
            if task:
                try:
                    self.process_task(task)
                    logging.info(f"✅ Yeniden işlem başarılı: {task}")
                except Exception as e:
                    logging.error(f"❌ Yeniden işlem hatası: {e}")
                    self.enqueue_task(task)  # Başarısız olursa tekrar kuyruğa ekle
            else:
                logging.info("📌 Bekleyen hata işlemi bulunamadı.")

# Modülü çalıştırmak için nesne oluştur
if __name__ == "__main__":
    process_manager = ProcessManager()
    process_manager.run_multiprocessing()

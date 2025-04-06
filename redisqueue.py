# ==============================
# 📌 Zapata M6H - redisqueue.py
# 📌 Redis Tabanlı Görev Kuyruğu Yönetimi
# 📌 Görevleri Redis kuyruğuna ekler, başarısız görevleri tekrar dener.
# ==============================

import redis
import json
import time
import logging
import colorlog
from configmodule import config
import threading

class RedisQueue:
    redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, decode_responses=True)
    FAILED_TASK_LOG = "failed_task_reasons.json"
    
    def __init__(self, queue_name="task_queue", retry_limit=3):
        """Redis kuyruğu yöneticisi."""
        self.logger = self.setup_logging()
        try:
            self.redis_client = redis.StrictRedis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                decode_responses=True
            )
            self.queue_name = queue_name
            self.retry_limit = retry_limit
            self.logger.info(f"✅ Redis kuyruğu ({queue_name}) başlatıldı.")
        except Exception as e:
            self.logger.error(f"❌ Redis kuyruğu başlatılamadı: {e}")

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
        file_handler = logging.FileHandler("redisqueue.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def enqueue_task(self, task_data):
        """Görevi Redis kuyruğuna ekler."""
        try:
            task_data["retry_count"] = 0  # Başlangıçta sıfır deneme
            self.redis_client.rpush(self.queue_name, json.dumps(task_data))
            self.logger.info(f"✅ Görev kuyruğa eklendi: {task_data}")
        except Exception as e:
            self.logger.error(f"❌ Görev kuyruğa eklenemedi: {e}")

    def dequeue_task(self):
        """Kuyruktan bir görevi çeker ve JSON olarak döndürür."""
        try:
            task_json = self.redis_client.lpop(self.queue_name)
            if task_json:
                task_data = json.loads(task_json)
                self.logger.info(f"📌 Görev alındı: {task_data}")
                return task_data
            else:
                self.logger.info("⚠️ Kuyruk boş.")
                return None
        except Exception as e:
            self.logger.error(f"❌ Görev alınırken hata oluştu: {e}")
            return None

    def retry_failed_tasks(self):
        """Başarısız görevleri tekrar kuyruğa ekler."""
        MAX_RETRY = int(config.get_env_variable("MAX_TASK_RETRY", 3))
        failed_tasks = self.redis_client.lrange("failed_tasks", 0, -1)

        def process_task(task_json):
            task_data = json.loads(task_json)
            retry_count = task_data.get("retry_count", 0)
            failure_reason = task_data.get("failure_reason", "Bilinmeyen hata")

            if retry_count < MAX_RETRY:
                task_data["retry_count"] += 1
                self.enqueue_task(task_data)
                self.redis_client.lrem("failed_tasks", 1, task_json)
                self.logger.info(f"🔄 Görev tekrar kuyruğa alındı: {task_data}")
            else:
                self.logger.error(f"❌ Görev {MAX_RETRY} kez denendi ve başarısız oldu: {task_data}")
                self.save_failure_reason(task_data["task_id"], failure_reason)
                self.redis_client.rpush("permanently_failed_tasks", task_json)

        threads = [threading.Thread(target=process_task, args=(task,)) for task in failed_tasks]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    redis_queue = RedisQueue()

    sample_task = {"task_id": "001", "data": "Test verisi"}
    redis_queue.enqueue_task(sample_task)

    dequeued_task = redis_queue.dequeue_task()
    print("📄 Kuyruktan Çekilen Görev:", dequeued_task)

    redis_queue.move_to_failed_queue(dequeued_task)
    redis_queue.retry_failed_tasks()

    print("✅ Redis Kuyruk Testleri Tamamlandı!")
# ==============================



# class RedisQueue:
#     redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, decode_responses=True)
#     FAILED_TASK_LOG = "failed_task_reasons.json"
    
#     def __init__(self, queue_name="task_queue", retry_limit=3):
#         """Redis kuyruğu yöneticisi."""
#         self.logger = self.setup_logging()
#         try:
#             self.redis_client = redis.StrictRedis(
#                 host=config.REDIS_HOST,
#                 port=config.REDIS_PORT,
#                 decode_responses=True
#             )
#             self.queue_name = queue_name
#             self.retry_limit = retry_limit
#             self.logger.info(f"✅ Redis kuyruğu ({queue_name}) başlatıldı.")
#         except Exception as e:
#             self.logger.error(f"❌ Redis kuyruğu başlatılamadı: {e}")

#     def setup_logging(self):
#         """Loglama sistemini kurar."""
#         log_formatter = colorlog.ColoredFormatter(
#             "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
#             datefmt="%Y-%m-%d %H:%M:%S",
#             log_colors={
#                 'DEBUG': 'cyan',
#                 'INFO': 'green',
#                 'WARNING': 'yellow',
#                 'ERROR': 'red',
#                 'CRITICAL': 'bold_red',
#             }
#         )
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(log_formatter)
#         file_handler = logging.FileHandler("redisqueue.log", encoding="utf-8")
#         file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

#         logger = logging.getLogger(__name__)
#         logger.setLevel(logging.DEBUG)
#         logger.addHandler(console_handler)
#         logger.addHandler(file_handler)
#         return logger

#     def enqueue_task(self, task_data):
#         """Görevi Redis kuyruğuna ekler."""
#         try:
#             task_data["retry_count"] = 0  # Başlangıçta sıfır deneme
#             self.redis_client.rpush(self.queue_name, json.dumps(task_data))
#             self.logger.info(f"✅ Görev kuyruğa eklendi: {task_data}")
#         except Exception as e:
#             self.logger.error(f"❌ Görev kuyruğa eklenemedi: {e}")

#     def dequeue_task(self):
#         """Kuyruktan bir görevi çeker ve JSON olarak döndürür."""
#         try:
#             task_json = self.redis_client.lpop(self.queue_name)
#             if task_json:
#                 task_data = json.loads(task_json)
#                 self.logger.info(f"📌 Görev alındı: {task_data}")
#                 return task_data
#             else:
#                 self.logger.info("⚠️ Kuyruk boş.")
#                 return None
#         except Exception as e:
#             self.logger.error(f"❌ Görev alınırken hata oluştu: {e}")
#             return None
        

#     def retry_failed_tasks():
#     """
#     Başarısız görevleri tekrar kuyruğa ekler.
#     """
#     MAX_RETRY = int(config.get_env_variable("MAX_TASK_RETRY", 3))
#     failed_tasks = redis_client.lrange("failed_tasks", 0, -1)

#     # """Başarısız görevleri belirlenen tekrar sayısı kadar yeniden kuyruğa ekler."""
#     #     failed_tasks = self.redis_client.lrange("failed_tasks", 0, -1)
#     #     for task_json in failed_tasks:
#     #         task_data = json.loads(task_json)
#     #         if task_data.get("retry_count", 0) < self.retry_limit:
#     #             task_data["retry_count"] += 1
#     #             self.enqueue_task(task_data)
#     #             self.logger.warning(f"🔄 Görev yeniden kuyruğa alındı: {task_data}")
#     #         else:
#     #             self.logger.error(f"❌ Görev maksimum deneme sınırına ulaştı ve atlandı: {task_data}")
#     #     self.redis_client.delete("failed_tasks") 

#     def process_task(task_json):
#         task_data = json.loads(task_json)
#         retry_count = task_data.get("retry_count", 0)
#         failure_reason = task_data.get("failure_reason", "Bilinmeyen hata")

#         if retry_count < MAX_RETRY:
#             task_data["retry_count"] += 1
#             enqueue_task(task_data)
#             redis_client.lrem("failed_tasks", 1, task_json)
#             logging.info(f"🔄 Görev tekrar kuyruğa alındı: {task_data}")
#         else:
#             logging.error(f"❌ Görev {MAX_RETRY} kez denendi ve başarısız oldu: {task_data}")
#             save_failure_reason(task_data["task_id"], failure_reason)
#             redis_client.rpush("permanently_failed_tasks", task_json)

#     threads = [threading.Thread(target=process_task, args=(task,)) for task in failed_tasks]
#     for t in threads:
#         t.start()
#     for t in threads:
#         t.join()

# def save_failure_reason(task_id, reason):
#     """
#     Hata nedenlerini JSON formatında kaydeder.
#     """
#     try:
#         with open(FAILED_TASK_LOG, "r", encoding="utf-8") as f:
#             failure_log = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         failure_log = {}

#     failure_log[task_id] = reason

#     with open(FAILED_TASK_LOG, "w", encoding="utf-8") as f:
#         json.dump(failure_log, f, indent=4, ensure_ascii=False)

#     logging.info(f"📝 Görev {task_id} için hata nedeni kaydedildi: {reason}")

# def move_to_failed_queue(self, task_data):
#         """Başarısız görevleri başarısız kuyruğuna taşır."""
#         try:
#             self.redis_client.rpush("failed_tasks", json.dumps(task_data))
#             self.logger.error(f"❌ Görev başarısız olarak işaretlendi: {task_data}")
#         except Exception as e:
#             self.logger.error(f"❌ Görev başarısız kuyruğuna taşınamadı: {e}")    









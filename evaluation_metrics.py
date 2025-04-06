# 🚀 **Evaluation Metrics (Değerlendirme Metrikleri) Modülü Hazır!**  

# 📌 **Bu modülde yapılanlar:**  
# ✅ **Retrieval (getirme) ve sıralama işlemlerinin başarısını ölçer.**  
# ✅ **Precision, Recall, F1-Score, MAP (Mean Average Precision), MRR (Mean Reciprocal Rank), NDCG (Normalized Discounted Cumulative Gain) gibi metrikleri hesaplar.**  
# ✅ **Fine-tuning süreçlerinde eğitim sonuçlarını analiz eder.**  
# ✅ **Retrieve edilen belgelerin kalitesini belirlemek için kullanılır.**  
# ✅ **FAISS, ChromaDB ve SQLite sorgu sonuçlarını değerlendirmek için uygundur.**  
# ✅ **Hata yönetimi ve loglama mekanizması eklendi.**  



## **📌 `evaluation_metrics.py` (Değerlendirme Metrikleri Modülü)**  


# ==============================
# 📌 Zapata M6H - evaluation_metrics.py
# 📌 Retrieval ve sıralama işlemlerini değerlendiren metrikler içerir.
# ==============================

import logging
import colorlog
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score

class EvaluationMetrics:
    def __init__(self):
        """Değerlendirme metrikleri başlatma işlemi"""
        self.logger = self.setup_logging()

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
        file_handler = logging.FileHandler("evaluation_metrics.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

    def precision(self, y_true, y_pred):
        """Precision (Kesinlik) hesaplar"""
        try:
            score = precision_score(y_true, y_pred, average='binary')
            self.logger.info(f"✅ Precision: {score}")
            return score
        except Exception as e:
            self.logger.error(f"❌ Precision hesaplama hatası: {e}")
            return None

    def recall(self, y_true, y_pred):
        """Recall (Duyarlılık) hesaplar"""
        try:
            score = recall_score(y_true, y_pred, average='binary')
            self.logger.info(f"✅ Recall: {score}")
            return score
        except Exception as e:
            self.logger.error(f"❌ Recall hesaplama hatası: {e}")
            return None

    def f1(self, y_true, y_pred):
        """F1-Score hesaplar"""
        try:
            score = f1_score(y_true, y_pred, average='binary')
            self.logger.info(f"✅ F1-Score: {score}")
            return score
        except Exception as e:
            self.logger.error(f"❌ F1-Score hesaplama hatası: {e}")
            return None

    def mean_average_precision(self, y_true, y_pred, k=10):
        """Mean Average Precision (MAP) hesaplar"""
        try:
            y_pred_sorted = np.argsort(-np.array(y_pred))[:k]
            average_precisions = []
            relevant_count = 0

            for i, idx in enumerate(y_pred_sorted):
                if y_true[idx] == 1:
                    relevant_count += 1
                    precision_at_k = relevant_count / (i + 1)
                    average_precisions.append(precision_at_k)

            map_score = np.mean(average_precisions) if average_precisions else 0
            self.logger.info(f"✅ MAP@{k}: {map_score}")
            return map_score
        except Exception as e:
            self.logger.error(f"❌ MAP hesaplama hatası: {e}")
            return None

    def mean_reciprocal_rank(self, y_true, y_pred):
        """Mean Reciprocal Rank (MRR) hesaplar"""
        try:
            y_pred_sorted = np.argsort(-np.array(y_pred))
            for i, idx in enumerate(y_pred_sorted):
                if y_true[idx] == 1:
                    mrr_score = 1 / (i + 1)
                    self.logger.info(f"✅ MRR: {mrr_score}")
                    return mrr_score
            return 0
        except Exception as e:
            self.logger.error(f"❌ MRR hesaplama hatası: {e}")
            return None

    def ndcg(self, y_true, y_pred, k=10):
        """Normalized Discounted Cumulative Gain (NDCG) hesaplar"""
        try:
            y_pred_sorted = np.argsort(-np.array(y_pred))[:k]
            dcg = sum((2**y_true[idx] - 1) / np.log2(i + 2) for i, idx in enumerate(y_pred_sorted))
            ideal_sorted = sorted(y_true, reverse=True)[:k]
            idcg = sum((2**rel - 1) / np.log2(i + 2) for i, rel in enumerate(ideal_sorted))

            ndcg_score = dcg / idcg if idcg > 0 else 0
            self.logger.info(f"✅ NDCG@{k}: {ndcg_score}")
            return ndcg_score
        except Exception as e:
            self.logger.error(f"❌ NDCG hesaplama hatası: {e}")
            return None

# ==============================
# ✅ Test Komutları:
if __name__ == "__main__":
    evaluator = EvaluationMetrics()

    # Test verileri (1: Relevan, 0: İlgisiz)
    y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]  
    y_pred = [0.9, 0.1, 0.8, 0.7, 0.3, 0.6, 0.2, 0.4, 0.95, 0.05]

    precision = evaluator.precision(y_true, [1 if x > 0.5 else 0 for x in y_pred])
    recall = evaluator.recall(y_true, [1 if x > 0.5 else 0 for x in y_pred])
    f1 = evaluator.f1(y_true, [1 if x > 0.5 else 0 for x in y_pred])
    map_score = evaluator.mean_average_precision(y_true, y_pred)
    mrr_score = evaluator.mean_reciprocal_rank(y_true, y_pred)
    ndcg_score = evaluator.ndcg(y_true, y_pred)

    print("📄 Precision:", precision)
    print("📄 Recall:", recall)
    print("📄 F1-Score:", f1)
    print("📄 MAP:", map_score)
    print("📄 MRR:", mrr_score)
    print("📄 NDCG:", ndcg_score)
# ==============================

# ## **📌 Yapılan Geliştirmeler:**  
(Değerlendirme Metrikleri Modülü)
# ✅ **Precision, Recall, F1-Score, MAP, MRR ve NDCG hesaplama fonksiyonları eklendi.**  
# ✅ **Retrieve ve FAISS sonuçlarını değerlendirmek için optimize edildi.**  
# ✅ **Fine-tuning süreçlerinde model başarısını ölçmek için kullanılabilir.**  
# ✅ **Loglama ve hata yönetimi mekanizması eklendi.**  
# ✅ **Test ve çalıştırma komutları dahil edildi.**  

# 🚀 **Bu modül tamamen hazır! Sıradaki adımı belirleyelim mi?** 😊
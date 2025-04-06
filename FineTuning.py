#Fine-Tuning Modülü (Güncellenmiş Son Hali)import os
import json
import redis
import sqlite3
import torch
import logging
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from configmodule import config

# Loglama Ayarları
logging.basicConfig(filename="finetuning.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# SQLite ve Redis Bağlantıları
redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

class FineTuningDataset(Dataset):
    """ Eğitim verisi için PyTorch dataset sınıfı """
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx], truncation=True, padding="max_length", max_length=self.max_length, return_tensors="pt"
        )
        encoding = {key: val.squeeze() for key, val in encoding.items()}
        encoding["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return encoding

class FineTuner:
    def __init__(self, model_name):
        """ Fine-Tuning işlemlerini yöneten sınıf """
        self.model_name = model_name
        self.batch_size = config.FINETUNE_BATCH_SIZE
        self.epochs = config.FINETUNE_EPOCHS
        self.learning_rate = config.FINETUNE_LR
        self.output_dir = os.path.join(config.FINETUNE_OUTPUT_DIR, model_name.replace("/", "_"))

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)

    def fetch_training_data(self):
        """ SQLite veritabanından eğitim verisini çeker """
        conn = sqlite3.connect(config.SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT text, label FROM training_data")
        rows = cursor.fetchall()
        conn.close()

        texts = [row[0] for row in rows]
        labels = [row[1] for row in rows]
        return texts, labels

    def train_model(self):
        """ Modeli eğitir ve kaydeder """
        texts, labels = self.fetch_training_data()
        dataset = FineTuningDataset(texts, labels, self.tokenizer)

        training_args = TrainingArguments(
            output_dir=self.output_dir,
            per_device_train_batch_size=self.batch_size,
            num_train_epochs=self.epochs,
            learning_rate=self.learning_rate,
            logging_dir=os.path.join(self.output_dir, "logs"),
            save_strategy="epoch"
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            tokenizer=self.tokenizer
        )

        trainer.train()
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)
        logging.info(f"✅ {self.model_name} modeli eğitildi ve {self.output_dir} dizinine kaydedildi.")

    def save_model_to_redis(self):
        """ Eğitilmiş modeli Redis'e kaydeder """
        with open(os.path.join(self.output_dir, "pytorch_model.bin"), "rb") as f:
            model_data = f.read()
            redis_client.set(f"fine_tuned_model:{self.model_name}", model_data)
        logging.info(f"📌 {self.model_name} modeli Redis'e kaydedildi.")

    def load_model_from_redis(self):
        """ Redis'ten modeli yükler """
        model_data = redis_client.get(f"fine_tuned_model:{self.model_name}")
        if model_data:
            with open(os.path.join(self.output_dir, "pytorch_model.bin"), "wb") as f:
                f.write(model_data)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.output_dir)
            logging.info(f"📌 {self.model_name} modeli Redis’ten alındı ve belleğe yüklendi.")
        else:
            logging.error(f"❌ {self.model_name} için Redis’te kayıtlı model bulunamadı.")

def parallel_finetune(model_name):
    """ Seçilen modeli paralel olarak eğitir """
    fine_tuner = FineTuner(model_name)
    fine_tuner.train_model()
    fine_tuner.save_model_to_redis()

def train_selected_models(model_list):
    """ Seçilen modelleri multiprocessing ile eğitir """
    with ProcessPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
        executor.map(parallel_finetune, model_list)

if __name__ == "__main__":
    selected_models = [
        "bert-base-uncased",
        "sentence-transformers/all-MiniLM-L6-v2",
        "meta-llama/Llama-3-8b",
        "deepseek-ai/deepseek-1.5b",
        "NordicEmbed-Text"
    ]
    train_selected_models(selected_models)
    print("✅ Fine-Tuning tamamlandı!")

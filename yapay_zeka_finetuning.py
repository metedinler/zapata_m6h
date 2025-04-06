
# ==============================
# 📌 Zapata M6H - yapay zeka fine tuning.py
# ### **yapay zeka fine tuning.py**
# ==============================


import os
import json
import sqlite3
import redis
import torch
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer
from configmodule import config
from logging_module import setup_logging

# Logger başlatma
logger = setup_logging("fine_tuning")

# Desteklenen modellerin listesi
AVAILABLE_MODELS = {
    "llama_3.1_8b": "meta-llama/Llama-3.1-8B",
    "deepseek_r1_1.5b": "deepseek/DeepSeek-R1-1.5B",
    "all_minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "nordicembed_text": "NbAiLab/nordic-embed-text",
}

class FineTuningDataset(torch.utils.data.Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        encoding = {key: val.squeeze() for key, val in encoding.items()}
        encoding["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return encoding

class FineTuner:
    def __init__(self, model_name):
        self.model_name = AVAILABLE_MODELS[model_name]
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)
        self.output_dir = os.path.join(config.FINETUNE_OUTPUT_DIR, model_name)
        self.sqlite_db = config.SQLITE_DB_PATH
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.batch_size = config.FINETUNE_BATCH_SIZE
        self.epochs = config.FINETUNE_EPOCHS
        self.learning_rate = config.FINETUNE_LR

    def fetch_training_data(self):
        """
        SQLite veritabanından eğitim verisini çeker.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT text, label FROM training_data")
        rows = cursor.fetchall()
        conn.close()
        texts = [row[0] for row in rows]
        labels = [row[1] for row in rows]
        return texts, labels

    def train_model(self):
        """
        Modeli fine-tune ederek eğitir.
        """
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
        logger.info(f"✅ Model {self.model_name} eğitildi ve {self.output_dir} dizinine kaydedildi.")

    def save_model_to_redis(self):
        """
        Eğitilen modeli Redis içinde saklar.
        """
        with open(os.path.join(self.output_dir, "pytorch_model.bin"), "rb") as f:
            model_data = f.read()
            self.redis_client.set(f"fine_tuned_model_{self.model_name}", model_data)
        logger.info("📌 Eğitilmiş model Redis'e kaydedildi.")

    def load_model_from_redis(self):
        """
        Redis'ten modeli alır ve belleğe yükler.
        """
        model_data = self.redis_client.get(f"fine_tuned_model_{self.model_name}")
        if model_data:
            with open(os.path.join(self.output_dir, "pytorch_model.bin"), "wb") as f:
                f.write(model_data)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.output_dir)
            logger.info("📌 Model Redis’ten alındı ve belleğe yüklendi.")
        else:
            logger.error("❌ Redis’te kayıtlı model bulunamadı.")


def parallel_training(selected_models):
    """
    Seçilen modellerin **paralel olarak** eğitilmesini sağlar.
    """
    with ProcessPoolExecutor(max_workers=len(selected_models)) as executor:
        futures = [executor.submit(FineTuner(model).train_model) for model in selected_models]
        for future in futures:
            future.result()  # İşlemlerin tamamlanmasını bekle

if __name__ == "__main__":
    selected_models = ["llama_3.1_8b", "deepseek_r1_1.5b", "all_minilm", "nordicembed_text"]
    parallel_training(selected_models)
# ==============================

# ### **yapay zeka fine tuning2.py**

# ==============================
# 📌 Zapata M6H - yapay zeka fine tuning.py
# 📌 Atıf Zinciri Analizi ve Veri İşleme Modülü
# 📌 Metin içi atıfları analiz eder ve kaynakça ile eşleştirir.
# ==============================

import os
import torch
from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding
from datasets import load_dataset

class FineTuningManager:
    def __init__(self, model_name: str, dataset_path: str, output_dir: str):
        self.model_name = model_name
        self.dataset_path = dataset_path
        self.output_dir = output_dir
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    def load_dataset(self):
        """Veri kümesini yükleyip tokenizasyon yapar."""
        dataset = load_dataset('csv', data_files=self.dataset_path)
        dataset = dataset.map(lambda x: self.tokenizer(x['text'], truncation=True, padding='max_length'), batched=True)
        return dataset

    def train_model(self, epochs=3, batch_size=8):
        """Modeli belirlenen veri kümesi üzerinde eğitir."""
        dataset = self.load_dataset()
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            evaluation_strategy='epoch',
            save_strategy='epoch',
            logging_dir=f'{self.output_dir}/logs',
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            save_total_limit=2,
            load_best_model_at_end=True,
            report_to='none'
        )
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset['train'],
            eval_dataset=dataset['test'],
            tokenizer=self.tokenizer,
            data_collator=DataCollatorWithPadding(self.tokenizer)
        )
        trainer.train()
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)

    def evaluate_model(self):
        """Eğitilmiş modelin test seti üzerindeki performansını değerlendirir."""
        dataset = self.load_dataset()
        trainer = Trainer(
            model=self.model,
            tokenizer=self.tokenizer
        )
        results = trainer.evaluate(eval_dataset=dataset['test'])
        return results

if __name__ == "__main__":
    finetuner = FineTuningManager(
        model_name='bert-base-uncased', 
        dataset_path='data/dataset.csv', 
        output_dir='models/finetuned_model'
    )
    finetuner.train_model()
    print("Eğitim tamamlandı!")


# yapay_zeka_finetuning3.py


import os
import json
import sqlite3
import redis
import torch
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer
from configmodule import config
from logging_module import setup_logging

# Logger başlatma
logger = setup_logging("fine_tuning")

# Desteklenen modellerin listesi
AVAILABLE_MODELS = {
    "llama_3.1_8b": "meta-llama/Llama-3.1-8B",
    "deepseek_r1_1.5b": "deepseek/DeepSeek-R1-1.5B",
    "all_minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "nordicembed_text": "NbAiLab/nordic-embed-text",
}

class FineTuningDataset(torch.utils.data.Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        encoding = {key: val.squeeze() for key, val in encoding.items()}
        encoding["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return encoding

class FineTuner:
    def __init__(self, model_name):
        self.model_name = AVAILABLE_MODELS[model_name]
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)
        self.output_dir = os.path.join(config.FINETUNE_OUTPUT_DIR, model_name)
        self.sqlite_db = config.SQLITE_DB_PATH
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
        self.batch_size = config.FINETUNE_BATCH_SIZE
        self.epochs = config.FINETUNE_EPOCHS
        self.learning_rate = config.FINETUNE_LR

    def fetch_training_data(self):
        """
        SQLite veritabanından eğitim verisini çeker.
        """
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        cursor.execute("SELECT text, label FROM training_data")
        rows = cursor.fetchall()
        conn.close()
        texts = [row[0] for row in rows]
        labels = [row[1] for row in rows]
        return texts, labels

    def train_model(self):
        """
        Modeli fine-tune ederek eğitir.
        """
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
        logger.info(f"✅ Model {self.model_name} eğitildi ve {self.output_dir} dizinine kaydedildi.")

    def save_model_to_redis(self):
        """
        Eğitilen modeli Redis içinde saklar.
        """
        with open(os.path.join(self.output_dir, "pytorch_model.bin"), "rb") as f:
            model_data = f.read()
            self.redis_client.set(f"fine_tuned_model_{self.model_name}", model_data)
        logger.info("📌 Eğitilmiş model Redis'e kaydedildi.")

    def load_model_from_redis(self):
        """
        Redis'ten modeli alır ve belleğe yükler.
        """
        model_data = self.redis_client.get(f"fine_tuned_model_{self.model_name}")
        if model_data:
            with open(os.path.join(self.output_dir, "pytorch_model.bin"), "wb") as f:
                f.write(model_data)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.output_dir)
            logger.info("📌 Model Redis’ten alındı ve belleğe yüklendi.")
        else:
            logger.error("❌ Redis’te kayıtlı model bulunamadı.")


def parallel_training(selected_models):
    """
    Seçilen modellerin **paralel olarak** eğitilmesini sağlar.
    """
    with ProcessPoolExecutor(max_workers=len(selected_models)) as executor:
        futures = [executor.submit(FineTuner(model).train_model) for model in selected_models]
        for future in futures:
            future.result()  # İşlemlerin tamamlanmasını bekle

if __name__ == "__main__":
    selected_models = ["llama_3.1_8b", "deepseek_r1_1.5b", "all_minilm", "nordicembed_text"]
    parallel_training(selected_models)

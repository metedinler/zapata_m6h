import requests

from configmodule import config


class OllamaClient:
    def __init__(self):
        self.base_url = str(config.OLLAMA_BASE_URL).rstrip("/")
        self.llm_model = config.OLLAMA_LLM_MODEL
        self.embed_model = config.OLLAMA_EMBED_MODEL
        self.timeout = 30

    def generate_text(self, prompt, model=None):
        selected_model = model or self.llm_model
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": selected_model, "prompt": prompt, "stream": False},
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
            return payload.get("response")
        except Exception:
            return None

    def generate_embedding(self, text, model=None):
        selected_model = model or self.embed_model
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": selected_model, "prompt": text},
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
            embedding = payload.get("embedding")
            return embedding if isinstance(embedding, list) else None
        except Exception:
            return None

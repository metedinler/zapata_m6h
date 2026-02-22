import requests

from configmodule import config


class OpenClawClient:
    def __init__(self):
        self.enabled = config.OPENCLAW_ENABLED
        self.base_url = str(config.OPENCLAW_API_URL).rstrip("/")
        self.timeout = 20

    def generate_with_context(self, query, context):
        if not self.enabled:
            return None

        payload = {
            "query": query,
            "context": context,
            "provider": "ollama",
            "model": config.OLLAMA_LLM_MODEL,
        }

        endpoints = [
            f"{self.base_url}/orchestrate",
            f"{self.base_url}/rag/generate",
            f"{self.base_url}/generate",
        ]

        for endpoint in endpoints:
            try:
                response = requests.post(endpoint, json=payload, timeout=self.timeout)
                if response.status_code >= 400:
                    continue

                data = response.json()
                for key in ("response", "answer", "output", "text"):
                    if isinstance(data.get(key), str) and data.get(key).strip():
                        return data.get(key)
            except Exception:
                continue

        return None

import requests
import logging

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        logging.basicConfig(level=logging.INFO)

    def call_ollama_api(self, prompt: str) -> str:
        """Call the Ollama API with the given prompt."""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": "llama3.2:3b",
                    "prompt": prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                return response.json()["response"]
            else:
                logging.error(f"Error calling Ollama API: {response.status_code}")
                return ""
        except Exception as e:
            logging.error(f"Error calling Ollama API: {str(e)}")
            return "" 
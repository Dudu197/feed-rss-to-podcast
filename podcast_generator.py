import requests
import json
from typing import List, Dict
from ollama_client import OllamaClient
import logging

class PodcastGenerator:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_client = OllamaClient(ollama_url)
        logging.basicConfig(level=logging.INFO)

    def generate_script(self, news_items: List[Dict]) -> str:
        """Generate a podcast script from news items using Ollama."""
        # Prepare the news content for the prompt
        news_content = "\n\n".join([
            f"Título: {news['title']}\n"
            f"Fonte: {news['source']}\n"
            f"Resumo: {news['summary']}"
            for news in news_items
        ])

        prompt = f"Crie um podcast em português sobre as seguintes notícias. O roteiro deve ser envolvente, informativo e adequado para um podcast de notícias. Use uma linguagem clara e acessível.\n\nNotícias:\n{news_content}\n\nRoteiro do Podcast:"
        return self.ollama_client.call_ollama_api(prompt)

    def save_script(self, script: str, output_file: str = "podcast_script.txt"):
        """Save the generated script to a file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(script) 
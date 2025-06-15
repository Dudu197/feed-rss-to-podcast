import json
import os
from datetime import datetime
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from ollama_client import OllamaClient
import logging

class NewsStorage:
    def __init__(self, storage_dir: str = "news_data"):
        self.storage_dir = storage_dir
        self._ensure_storage_dir()
        self.ollama_client = OllamaClient()
        logging.basicConfig(level=logging.INFO)

    def _ensure_storage_dir(self):
        """Create storage directory if it doesn't exist."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def clean_old_news(self):
        """Remove all previously saved news."""
        if os.path.exists(self.storage_dir):
            for file in os.listdir(self.storage_dir):
                file_path = os.path.join(self.storage_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    logging.error(f"Error deleting {file_path}: {str(e)}")

    def save_news(self, news_items: List[Dict]):
        """Save news items to JSON files, downloading the full news content from the link and generating a summary."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, news in enumerate(news_items):
            # Download the news content from the link
            news_content = ""
            try:
                response = requests.get(news['link'], timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Try to extract the main content
                    paragraphs = soup.find_all('p')
                    news_content = '\n'.join([p.get_text() for p in paragraphs if p.get_text()])
            except Exception as e:
                logging.error(f"Error downloading news content from {news['link']}: {str(e)}")
            news['content'] = news_content

            # Generate a summary using Ollama API
            prompt = f"Make a detailed summary of the following news article in Portuguese and return only the summary, no other text:\n\n{news_content}"
            summary = self.ollama_client.call_ollama_api(prompt)
            news['summary'] = summary

            filename = f"news_{timestamp}_{i}.json"
            filepath = os.path.join(self.storage_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(news, f, ensure_ascii=False, indent=2)

    def get_all_news(self) -> List[Dict]:
        """Retrieve all saved news items."""
        all_news = []
        
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    news_item = json.load(f)
                    all_news.append(news_item)
                    
        return all_news 
import feedparser
from datetime import datetime, timezone, timedelta
import os
from typing import List, Dict
import logging

class FeedReader:
    def __init__(self, feeds_file: str):
        self.feeds_file = feeds_file
        self.feeds = self._load_feeds()
        logging.basicConfig(level=logging.INFO)

    def _load_feeds(self) -> List[str]:
        """Load RSS feed URLs from the text file."""
        with open(self.feeds_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def fetch_latest_news(self) -> List[Dict]:
        """Fetch the latest news from all feeds, only from the past 7 days."""
        all_news = []
        today = datetime.now(timezone.utc).date()
        seven_days_ago = today - timedelta(days=7)
        
        for feed_url in self.feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    published_parsed = entry.get('published_parsed')
                    if published_parsed:
                        pub_date = datetime(*published_parsed[:6], tzinfo=timezone.utc).date()
                        if pub_date < seven_days_ago:
                            logging.debug(f"Skipping {entry.title} because it's older than 7 days")
                            logging.debug(f"Published date: {pub_date}")
                            logging.debug(f"Seven days ago: {seven_days_ago}")
                            continue
                    else:
                        logging.warning(f"No published_parsed for {entry.title}")
                        continue  # Skip if no published_parsed
                    
                    link = entry.link
                    if 'jovemnerd.com.br' in link:
                        link = link.replace('admin.', '')
                    
                    news_item = {
                        'title': entry.title,
                        'link': link,
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', ''),
                        'source': feed.feed.title
                    }
                    all_news.append(news_item)
            except Exception as e:
                logging.error(f"Error fetching feed {feed_url}: {str(e)}")
                
        return all_news 
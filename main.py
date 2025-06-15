from feed_reader import FeedReader
from news_storage import NewsStorage
from podcast_generator import PodcastGenerator
import os

def main():
    # Initialize components
    feed_reader = FeedReader("feeds.txt")
    news_storage = NewsStorage()
    podcast_generator = PodcastGenerator()

    # Clean old news
    print("Cleaning old news...")
    news_storage.clean_old_news()

    # Fetch latest news
    print("Fetching latest news...")
    news_items = feed_reader.fetch_latest_news()
    
    if not news_items:
        print("No news items found!")
        return

    # Save news
    print(f"Saving {len(news_items)} news items...")
    news_storage.save_news(news_items)

    # Generate podcast script
    print("Generating podcast script...")
    script = podcast_generator.generate_script(news_items)
    
    if script:
        # Save script
        print("Saving podcast script...")
        podcast_generator.save_script(script)
        print("Process completed successfully!")
    else:
        print("Failed to generate podcast script!")

if __name__ == "__main__":
    main() 
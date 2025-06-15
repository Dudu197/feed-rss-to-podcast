# RSS Feed to Podcast Script Generator

This project reads RSS feeds in Portuguese, downloads the latest news, and generates a podcast script using Ollama's AI capabilities.

## Prerequisites

- Python 3.7+
- Ollama running locally (default port: 11434)
- Internet connection

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Setup

1. Create a `feeds.txt` file in the project root directory
2. Add your RSS feed URLs to the file, one per line. For example:
```
https://www.example.com/feed1.xml
https://www.example.com/feed2.xml
```

## Usage

1. Make sure Ollama is running locally
2. Run the main script:
```bash
python main.py
```

The script will:
1. Clean any previously saved news
2. Fetch the latest news from all feeds
3. Save the news to the `news_data` directory
4. Generate a podcast script using Ollama
5. Save the script as `podcast_script.txt`

## Project Structure

- `main.py`: Main orchestration script
- `feed_reader.py`: Handles RSS feed reading
- `news_storage.py`: Manages news storage and retrieval
- `podcast_generator.py`: Generates podcast scripts using Ollama
- `feeds.txt`: List of RSS feed URLs
- `news_data/`: Directory where news items are stored
- `podcast_script.txt`: Generated podcast script

## Notes

- The project assumes Ollama is running locally on the default port (11434)
- All news items are saved as JSON files in the `news_data` directory
- The podcast script is generated in Portuguese
- Make sure your RSS feeds are in Portuguese for best results 
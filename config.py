import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="./.env")

TWITTER_CONSUMER_KEY = str(os.getenv('TWITTER_CONSUMER_KEY')) or ''
TWITTER_CONSUMER_SECRET = str(os.getenv('TWITTER_CONSUMER_SECRET')) or ''
TWITTER_ACCESS_TOKEN = str(os.getenv('TWITTER_ACCESS_TOKEN')) or ''
TWITTER_ACCESS_SECRET = str(os.getenv('TWITTER_ACCESS_SECRET')) or ''
TELEGRAM_TOKEN = str(os.getenv('TELEGRAM_TOKEN')) or ''
CHAT_ID = str(os.getenv('CHAT_ID')) or ''

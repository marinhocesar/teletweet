import logging
import tweepy

from config import (
    TWITTER_ACCESS_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
    TWITTER_ACCESS_TOKEN,
)
from src.singleton_meta import SingletonMeta


class TwitterHandler(metaclass=SingletonMeta):
    def __init__(self):
        self._setup()

    def _setup(self):
        logging.warning("logging into twitter.")
        self.__twitter_client = tweepy.Client(
            consumer_key=TWITTER_CONSUMER_KEY,
            consumer_secret=TWITTER_CONSUMER_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET,
        )
        auth = tweepy.OAuth1UserHandler(
            consumer_key=TWITTER_CONSUMER_KEY,
            consumer_secret=TWITTER_CONSUMER_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET,
        )
        self.__twitter_api = tweepy.API(auth=auth)
        try:
            screen_name = self.__twitter_api.verify_credentials().screen_name
        except Exception:
            logging.error("could not access twitter v1API.")
            raise ConnectionError
        logging.warning("----------------------------------")
        logging.warning(f"successfully logged into @{screen_name}!")

    def tweet_text(self, text: str):
        self.__twitter_client.create_tweet(text=text, user_auth=True)

    def tweet_photo(self, media_id: str, text: str):
        self.__twitter_client.create_tweet(
            text=text, media_ids=[media_id], user_auth=True
        )

    def simple_upload(self, filename: str):
        media = self.__twitter_api.simple_upload(filename=filename)
        return media

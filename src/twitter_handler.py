import logging
import os
from telegram import File
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
        try:
            self.__twitter_client.create_tweet(text=text, user_auth=True)
            logging.warning("tweet sent")
            return "Tweeted: " + (text or "")
        except Exception as e:
            logging.error("could not send tweet")
            return "Failed to tweet. Error: " + str(e)

    async def tweet_photo(self, photo_file: File, photo_path: str, text: str) -> str:
        await photo_file.download_to_drive(
            photo_path
        )  # Await the coroutine to download the file
        media = self.__twitter_api.simple_upload(filename=photo_path)
        media_id = media.media_id

        reply_text = ""
        try:
            self.__twitter_client.create_tweet(
                text=text, media_ids=[media_id], user_auth=True
            )
            logging.warning("tweet sent")
            reply_text = "Tweeted photo!"
        except Exception as e:
            logging.error("could not send tweet")
            reply_text = "Failed to tweet photo. Error: " + str(e)
        finally:
            os.remove(photo_path)
            return reply_text

    def message_handler_not_implemented(self):
        logging.error("type of message not supported")
        return "This type of message is not yet supported in the context of this application"

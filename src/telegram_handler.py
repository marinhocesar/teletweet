import logging
import os
from telegram import Update
import telegram

from config import (
    TELEGRAM_TOKEN,
)
from src.twitter_handler import TwitterHandler


class TelegramBot():
    def __init__(self) -> None:
        self._setup()

    def _setup(self):
        logging.warning("----------------------------------")
        logging.warning("building telegram connection")
        logging.warning("----------------------------------")

        self.twitter = TwitterHandler()
        self.bot = telegram.Bot(token=TELEGRAM_TOKEN)

    async def start(self, update: Update):
        if update.message is None:
            return

        await self.bot.send_message(
            chat_id=update.message.chat_id,
            text="Hi! Send me a message or photo, and I will tweet it.",
        )

    async def tweet_text(self, update: Update):
        if update.message is None:
            return

        message_text = update.message.text
        try:
            twitter = TwitterHandler()
            twitter.tweet_text(text=message_text or "")
            logging.warning("tweet sent")
            await self.bot.send_message(
                chat_id=update.message.chat_id, text="Tweeted: " + (message_text or "")
            )
        except Exception as e:
            logging.error("could not send tweet")
            await self.bot.send_message(
                chat_id=update.message.chat_id, text="Failed to tweet. Error: " + str(e)
            )

    async def tweet_photo(self, update: Update):
        if update.message is None:
            return

        message_text = update.message.caption
        photo_file = await update.message.photo[
            -1
        ].get_file()  # Await the coroutine to get the file object
        photo_path = os.path.join("/tmp", f"{update.message.photo[-1].file_id}.jpg")

        twitter = TwitterHandler()
        await photo_file.download_to_drive(
            photo_path
        )  # Await the coroutine to download the file
        media = twitter.simple_upload(filename=photo_path)
        media_id = media.media_id
        try:
            twitter.tweet_photo(text=message_text or "", media_id=media_id)
            logging.warning("tweet sent")
            await self.bot.send_message(chat_id=update.message.chat_id, text="Tweeted photo!")
        except Exception as e:
            logging.error("could not send tweet")
            await self.bot.send_message(
                chat_id=update.message.chat_id, text="Failed to tweet photo. Error: " + str(e)
            )
        finally:
            os.remove(photo_path)

    async def message_handler_not_implemented(self, update: Update):
        if update.message is None:
            return

        logging.error("type of message not supported")
        await self.bot.send_message(
            chat_id=update.message.chat_id,
            text="This type of message is not yet supported in the context of this application",
        )
        return

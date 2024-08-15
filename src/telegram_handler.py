import logging
import os
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ApplicationBuilder,
)

from config import (
    TELEGRAM_TOKEN,
)
from src.twitter_handler import TwitterHandler


class TelegramBot:
    def __init__(self) -> None:
        self._setup()

    def _setup(self):
        logging.warning("----------------------------------")
        logging.warning("building telegram connection")
        logging.warning("----------------------------------")

        self.twitter = TwitterHandler()
        try:
            self.application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        except Exception:
            logging.error("could not build telegram connection.")
            raise ConnectionError

        handled_message_types = filters.TEXT & filters.PHOTO
        self.application.add_handler(CommandHandler("start", start))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, tweet_text)
        )
        self.application.add_handler(MessageHandler(filters.PHOTO, tweet_photo))
        self.application.add_handler(
            MessageHandler(~handled_message_types, message_handler_not_implemented)
        )


async def start(update: Update, context: CallbackContext):
    if update.message is None:
        return

    await update.message.reply_text(
        text="Hi! Send me a message or photo, and I will tweet it.",
    )


async def tweet_text(update: Update, context: CallbackContext):
    if update.message is None:
        return

    message_text = update.message.text
    try:
        twitter = TwitterHandler()
        twitter.tweet_text(text=message_text or "")
        logging.warning("tweet sent")
        await update.message.reply_text(text="Tweeted: " + (message_text or ""))
    except Exception as e:
        logging.error("could not send tweet")
        await update.message.reply_text(text="Failed to tweet. Error: " + str(e))


async def tweet_photo(update: Update, context: CallbackContext):
    if update.message is None:
        return

    message_text = update.message.caption
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()  # Await the coroutine to get the file object
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
        await update.message.reply_text(text="Tweeted photo!")
    except Exception as e:
        logging.error("could not send tweet")
        await update.message.reply_text(
            text="Failed to tweet photo. Error: " + str(e),
        )
    finally:
        os.remove(photo_path)


async def message_handler_not_implemented(update: Update, context: CallbackContext):
    if update.message is None:
        return

    logging.error("type of message not supported")
    await update.message.reply_text(
        text="This type of message is not yet supported in the context of this application",
    )
    return

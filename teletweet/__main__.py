import logging
import os
import tweepy
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ApplicationBuilder,
)
from config import (
    TWITTER_ACCESS_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
    TWITTER_ACCESS_TOKEN,
    TELEGRAM_TOKEN,
    CHAT_ID,
)

logging.warning("logging into twitter.")

# Set up Twitter API
twitter_client = tweepy.Client(
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
twitter_api = tweepy.API(auth=auth)

try:
    screen_name = twitter_api.verify_credentials().screen_name
except Exception:
    logging.error("could not access twitter v1API.")
    raise ConnectionError

logging.warning("----------------------------------")
logging.warning(f"successfully logged into @{screen_name}!")
logging.warning("----------------------------------")


async def check_is_authorized(update: Update, context: CallbackContext):
    if update.message is None:
        return False
    if str(context._chat_id) != CHAT_ID:
        logging.error("forbidden chat tried to connect.")
        await update.message.reply_text(
            "You are not allowed to use this chat. Please disconnect."
        )
        return False
    return True


async def start(update: Update, context: CallbackContext):
    is_authorized = await check_is_authorized(update=update, context=context)
    if not is_authorized:
        return
    if update.message is None:
        return

    await update.message.reply_text(
        "Hi! Send me a message or photo, and I will tweet it."
    )


async def tweet_text(update: Update, context: CallbackContext):
    is_authorized = await check_is_authorized(update=update, context=context)
    if not is_authorized:
        return
    if update.message is None:
        return

    message_text = update.message.text
    try:
        twitter_client.create_tweet(text=message_text, user_auth=True)
        logging.warning("tweet sent")
        await update.message.reply_text("Tweeted: " + (message_text or ""))
    except Exception as e:
        logging.error("could not send tweet")
        await update.message.reply_text("Failed to tweet. Error: " + str(e))


async def tweet_photo(update: Update, context: CallbackContext):
    is_authorized = await check_is_authorized(update=update, context=context)
    if not is_authorized:
        return
    if update.message is None:
        return

    message_text = update.message.caption
    photo_file = await update.message.photo[
        -1
    ].get_file()  # Await the coroutine to get the file object
    photo_path = os.path.join("/tmp", f"{update.message.photo[-1].file_id}.jpg")

    await photo_file.download_to_drive(
        photo_path
    )  # Await the coroutine to download the file
    media = twitter_api.simple_upload(filename=photo_path)
    media_id = media.media_id
    try:
        twitter_client.create_tweet(
            text=message_text, media_ids=[media_id], user_auth=True
        )
        logging.warning("tweet sent")
        await update.message.reply_text("Tweeted photo!")
    except Exception as e:
        logging.error("could not send tweet")
        await update.message.reply_text("Failed to tweet photo. Error: " + str(e))
    finally:
        os.remove(photo_path)


async def message_handler_not_implemented(update: Update, context: CallbackContext):
    is_authorized = await check_is_authorized(update=update, context=context)
    if not is_authorized:
        return
    if update.message is None:
        return

    logging.error("type of message not supported")
    await update.message.reply_text(
        "This type of message is not yet supported in the context of this application"
    )
    return


def main():
    logging.warning("----------------------------------")
    logging.warning("building telegram connection")
    logging.warning("----------------------------------")

    try:
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    except Exception:
        logging.error("could not build telegram connection.")
        raise ConnectionError

    handled_message_types = filters.TEXT & filters.PHOTO
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tweet_text))
    application.add_handler(MessageHandler(filters.PHOTO, tweet_photo))
    application.add_handler(
        MessageHandler(~handled_message_types, message_handler_not_implemented)
    )

    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception as e_info:
        logging.error(e_info)
        logging.warning("shutting down application")

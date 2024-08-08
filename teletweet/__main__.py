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

print(twitter_api.verify_credentials().screen_name)


async def start(update: Update, context: CallbackContext):
    if str(context._chat_id) != CHAT_ID:
        return
    if update.message is not None:
        await update.message.reply_text(
            "Hi! Send me a message or photo, and I will tweet it."
        )


async def tweet_text(update: Update, context: CallbackContext):
    if str(context._chat_id) != CHAT_ID:
        return
    if update.message is None:
        return
    message = update.message.text
    try:
        twitter_client.create_tweet(text=message, user_auth=True)
        await update.message.reply_text("Tweeted: " + (message or ""))
    except Exception as e:
        await update.message.reply_text("Failed to tweet. Error: " + str(e))


async def tweet_photo(update: Update, context: CallbackContext):
    if str(context._chat_id) != CHAT_ID:
        return
    if update.message is None:
        return
    message = update.message.caption
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
        twitter_client.create_tweet(text=message, media_ids=[media_id], user_auth=True)
        await update.message.reply_text("Tweeted photo!")
    except Exception as e:
        await update.message.reply_text("Failed to tweet photo. Error: " + str(e))
    finally:
        os.remove(photo_path)


def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tweet_text))
    application.add_handler(MessageHandler(filters.PHOTO, tweet_photo))

    application.run_polling()


if __name__ == "__main__":
    main()

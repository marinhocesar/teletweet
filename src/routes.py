import logging
import requests

from flask import Response, request
from telegram import Message, Update

from app import app
from config import CHAT_ID, TELEGRAM_TOKEN
from src.telegram_handler import TelegramBot


def tel_send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    response = requests.post(url, json=payload)
    return response


def check_is_authorized(message: Message):
    chat_id = message.chat_id
    if str(chat_id) != CHAT_ID:
        logging.error("forbidden chat tried to connect.")
        tel_send_message(
            chat_id=chat_id,
            text="You are not allowed to use this chat. Please disconnect.",
        )
        return False
    return True


@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "POST":
        msg = request.get_json()
        logging.warning(msg)
        update = Update.de_json(data=msg)
        if update is None:
            return Response("no message", status=500)
        message = update.message
        if message is None:
            return Response("no message", status=500)

        is_authorized = check_is_authorized(message=message)
        if is_authorized is False:
            return Response("not authorized", status=403)

        telegram_bot = TelegramBot()

        if len(message.photo) > 0 and message.photo[-1] is not None:
            await telegram_bot.tweet_photo(update=update)
        elif message.text is not None:
            await telegram_bot.tweet_text(update=update)
        else:
            await telegram_bot.message_handler_not_implemented(update=update)

        return Response("ok", status=200)
    else:
        return "<h1>Welcome!</h1>"

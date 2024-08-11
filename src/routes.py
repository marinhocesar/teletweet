import logging
import os
import requests

from flask import Response, request
from telegram import Message

from app import app
from config import CHAT_ID, TELEGRAM_TOKEN
from src.twitter_handler import TwitterHandler


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
        message = Message.de_json(data=msg)
        if message is None:
            return Response("no message", status=500)

        is_authorized = check_is_authorized(message=message)

        if is_authorized is False:
            return Response("not authorized", status=403)

        twitter = TwitterHandler()

        response = ""
        if message.photo[-1] is not None:
            photo_file = await message.photo[-1].get_file()
            photo_path = os.path.join("/tmp", f"{message.photo[-1].file_id}.jpg")
            text = message.caption
            response = await twitter.tweet_photo(
                photo_file=photo_file, photo_path=photo_path, text=text or ""
            )
        elif message.text is not None:
            text = message.text
            response = twitter.tweet_text(text=text)
        else:
            response = twitter.message_handler_not_implemented()

        tel_send_message(message.chat_id, response)
        return Response("ok", status=200)
    else:
        return "<h1>Welcome!</h1>"

from flask import Flask

from src.telegram_handler import TelegramBot

app = Flask(__name__)

with app.app_context():
    from src import routes as routes  # noqa:401

if __name__ == "__main__":
    telegram_bot = TelegramBot()
    app.run(host="0.0.0.0")

from src.telegram_handler import TelegramBot

if __name__ == "__main__":
    telegram_bot = TelegramBot()
    telegram_bot.application.run_polling()

import telebot


class TelegramClient:
    def __init__(self, bot, chat_id: str, download_photos: bool):
        self.bot = bot
        self.chat_id = chat_id
        self.download_photos = download_photos


def new_telegram_client(token: str, chat_id: str, download_photos: bool):
    bot = telebot.TeleBot(token, parse_mode=None)
    client = TelegramClient(bot, chat_id, download_photos)

    return client

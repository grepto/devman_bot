import os

import telegram
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')


def send_message(message=None):
    bot = telegram.Bot(token=TG_TOKEN)
    bot.send_message(chat_id=TG_CHAT_ID, text=message)


if __name__ == '__main__':
    message = 'Hi!'
    send_message(message)

import os

import telegram
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')


def post_telegram(message=None, image_path=None):
    bot = telegram.Bot(token=TG_TOKEN)
    if message:
        bot.send_message(chat_id=TG_CHAT_ID, text=message)
    if image_path:
        with open(image_path, 'rb') as image:
            bot.send_photo(chat_id=TG_CHAT_ID, photo=image)


if __name__ == '__main__':
    message = 'Hi!'
    post_telegram(message)

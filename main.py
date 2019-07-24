import logging
import os
import logging.config
from datetime import datetime
import time

import requests
from dotenv import load_dotenv

from tg import send_message
import log_handlers

load_dotenv()

TOKEN = os.getenv('DEVMAN_TOKEN')
DEVMAN_ENDPOINT = os.getenv('DEVMAN_ENDPOINT')
LOG_LEVEL = os.getenv('LOG_LEVEL')


def send_telegram_msg(attempts):
    logger = logging.getLogger('check_devman_attempts')
    for attempt in attempts:
        lesson_title = attempt['lesson_title']
        lesson_result = 'К сожалению, в работе нашлись ошибки' if attempt['is_negative'] \
            else 'Преподавателю все понравилось, можно приступать к следующему уроку'
        lesson_url = DEVMAN_ENDPOINT + attempt['lesson_url']
        message = f'У вас проверили работу "{lesson_title}" ({lesson_url})\n\n{lesson_result}'
        logger.debug(message)
        send_message(message)


def check_devman_attempts():
    logger = logging.getLogger('check_devman_attempts')
    logger.info('Script started')
    headers = {
        'Authorization': TOKEN
    }
    params = {
        'timestamp': datetime.now().timestamp(),
    }
    request_url = DEVMAN_ENDPOINT + '/api/long_polling'
    while True:
        now = datetime.datetime.now()
        day_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
        day_end = now.replace(hour=23, minute=59, second=59, microsecond=0)
        if day_start < now < day_end:
            delta = day_start - now
            time.sleep(delta.seconds)

        logger.debug(f'New request with timestamp {params["timestamp"]}')
        try:
            response = requests.get(request_url, headers=headers, params=params, timeout=95).json()
        except requests.exceptions.ReadTimeout as error:
            logger.debug(error)
            continue
        except ConnectionError as error:
            logger.error(error)
            time.sleep(5)
            continue
        response_data = response
        status = response_data['status']
        if status == 'timeout':
            params['timestamp'] = response['timestamp_to_request']
            logger.debug('No news')
        if status == 'found':
            logger.debug(f'New feedback\n {response}')
            params['timestamp'] = response['last_attempt_timestamp']
            send_telegram_msg(response['new_attempts'])


def main():
    log_config = {
        'version': 1,
        'handlers': {
            'file_Handler': {
                'class': 'logging.FileHandler',
                'formatter': 'base_Formatter',
                'filename': 'requests.log'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'base_Formatter',
                'level': LOG_LEVEL,
            },
            'telegram': {
                'class': 'log_handlers.TelegramHandler',
                'formatter': 'tg_Formatter',
                'level': 'INFO',
            }
        },
        'loggers': {
            'check_devman_attempts': {
                'handlers': ['console', 'telegram'],
                'level': LOG_LEVEL,
            }
        },
        'formatters': {
            'base_Formatter': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
            'tg_Formatter': {
                'format': '%(asctime)s\n%(name)s\n%(levelname)s\n%(message)s',
            },
        }
    }
    logging.config.dictConfig(log_config)
    check_devman_attempts()


if __name__ == '__main__':
    main()

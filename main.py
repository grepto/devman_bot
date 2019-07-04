import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from log import get_logger
from tg import send_message

load_dotenv()

TOKEN = os.getenv('DEVMAN_TOKEN')
DEVMAN_ENDPOINT = os.getenv('DEVMAN_ENDPOINT')

logger = get_logger('check_devman_attempts')


def send_attempts_result(attempts):
    for attempt in attempts:
        lesson_title = attempt['lesson_title']
        lesson_result = 'К сожалению, в работе нашлись ошибки' if attempt['is_negative'] \
            else 'Преподавателю все понравилось, можно приступать к следующему уроку'
        lesson_url = DEVMAN_ENDPOINT + attempt['lesson_url']
        message = f'У вас проверили работу "{lesson_title}" ({lesson_url})\n\n{lesson_result}'
        logger.debug(message)
        send_message(message)


def check_devman_attempts():
    logger.info('Script started')
    headers = {
        'Authorization': TOKEN
    }
    params = {
        'timestamp': datetime.now().timestamp(),
    }
    request_url = DEVMAN_ENDPOINT + '/api/long_polling'
    while True:
        logger.debug(f'New request with timestamp {params["timestamp"]}')
        try:
            response = requests.get(request_url, headers=headers, params=params, timeout=95).json()
        except requests.exceptions.ReadTimeout as error:
            logger.error(error)
            continue
        except ConnectionError as error:
            logger.error(error)
            continue
        response_data = response
        status = response_data['status']
        if status == 'timeout':
            params['timestamp'] = response['timestamp_to_request']
            logger.debug('No news')
        if status == 'found':
            logger.debug(f'New feedback\n {response}')
            params['timestamp'] = response['last_attempt_timestamp']
            send_attempts_result(response['new_attempts'])


def main():
    check_devman_attempts()


if __name__ == '__main__':
    main()

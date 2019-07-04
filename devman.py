import os

import requests
from dotenv import load_dotenv

from log import get_logger

load_dotenv()

TOKEN = os.getenv('DEVMAN_TOKEN')


def check_devman_attempts():
    logger = get_logger('check_devman_attempts')

    headers = {
        'Authorization': TOKEN
    }

    params = {
        'timestamp': 1562198401,
        # 'timestamp': datetime.now().timestamp(),
    }

    while True:
        logger.info(f'New request with timestamp {params["timestamp"]}')
        try:
            response = requests.get('https://dvmn.org/api/long_polling'
                                    , headers=headers
                                    , params=params
                                    , timeout=95
                                    )
        except requests.exceptions.ReadTimeout as error:
            logger.error(error)
            continue
        except ConnectionError as error:
            logger.error(error)
            continue
        status = response.json()['status']
        if status == 'timeout':
            params['timestamp'] = response.json()['timestamp_to_request']
            logger.info('No news')
        if status == 'found':
            logger.info(f'New feedback\n {response.json()}')
            params['timestamp'] = response.json()['last_attempt_timestamp']


def main():
    check_devman_attempts()


if __name__ == '__main__':
    main()

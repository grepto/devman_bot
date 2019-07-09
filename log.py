import logging
import os
import logging.config

from dotenv import load_dotenv
from tg import send_message

load_dotenv()
LOG_LEVEL = os.getenv('LOG_LEVEL')


class TelegramHandler(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)
        send_message(log_entry)


def get_logger(logger_name):
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
                'class': 'log.TelegramHandler',
                'formatter': 'tg_Formatter',
                'level': 'INFO',
            }
        },
        'loggers': {
            logger_name: {
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
    return logging.getLogger(logger_name)


def main():
    logger = logging.getLogger('test_log')
    print(logger.getEffectiveLevel())


if __name__ == '__main__':
    main()

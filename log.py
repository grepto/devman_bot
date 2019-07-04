import logging
import os
import logging.config

from dotenv import load_dotenv

load_dotenv()
LOG_LEVEL = os.getenv('LOG_LEVEL')


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
            }
        },
        'loggers': {
            logger_name: {
                'handlers': ['console'],
                'level': LOG_LEVEL,
            }
        },
        'formatters': {
            'base_Formatter': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            }
        }
    }

    logging.config.dictConfig(log_config)
    return logging.getLogger(logger_name)


def main():
    logger = logging.getLogger('test_log')
    print(logger.getEffectiveLevel())


if __name__ == '__main__':
    main()

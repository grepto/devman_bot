import logging

from tg import send_message


class TelegramHandler(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)
        send_message(log_entry)

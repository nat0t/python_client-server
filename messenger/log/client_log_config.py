import logging
from logging.handlers import TimedRotatingFileHandler
import locale
import os

encoding = locale.getpreferredencoding()
log_directory = 'log'
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(module)s %(message)s')
if not os.path.isdir(log_directory):
    os.mkdir(log_directory)

log_handler = TimedRotatingFileHandler('logs/client.log', when='midnight',
                                       backupCount=7, encoding=encoding)
log_handler.setFormatter(formatter)

logger = logging.getLogger('messenger.client')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Logging test.')

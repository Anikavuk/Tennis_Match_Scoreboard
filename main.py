from waitress import serve
from paste.translogger import TransLogger
import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.ERROR)

from src.server import application


if __name__ == '__main__':
    serve(TransLogger(application, setup_console_handler=False))
    serve(application, host='0.0.0.0', port=8080)
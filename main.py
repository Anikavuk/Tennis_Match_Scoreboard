from waitress import serve
from paste.translogger import TransLogger
import logging
from whitenoise import WhiteNoise
from src.server import application

logger = logging.getLogger('waitress')
logger.setLevel(logging.ERROR)


if __name__ == '__main__':
    app = application
    app = WhiteNoise(app, root='src/view/static/')
    serve(TransLogger(application, setup_console_handler=False))
    serve(application, host='0.0.0.0', port=8080)


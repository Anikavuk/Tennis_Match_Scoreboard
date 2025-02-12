from waitress import serve
from paste.translogger import TransLogger
import logging
from whitenoise import WhiteNoise
from src.server import application

logger = logging.getLogger('waitress')
logger.setLevel(logging.ERROR)


if __name__ == '__main__':
    app = WhiteNoise(application)
    app.add_files('src/view/static/', prefix='static/')
    serve(TransLogger(app, setup_console_handler=False))
    serve(app, host='0.0.0.0', port=8080)
    # serve(app, host='79.174.80.252', port=8090)
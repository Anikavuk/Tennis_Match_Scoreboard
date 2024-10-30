from waitress import serve
from urllib.parse import parse_qs
from paste.translogger import TransLogger

from src.errors import InvalidPlayernameError, ErrorResponse
from src.db_model import PlayerManager


def application(environ, start_response):

    if environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/new-match':

        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length).decode('utf-8')

        form = parse_qs(body) # {'player1': ['Боб'], 'player2': ['Джек']}

        player1 = form.get('player1')
        player2 = form.get('player2')
        status = '200 OK'
        if player1 and player2:
            if PlayerManager.is_valid_username(player1) and PlayerManager.is_valid_username(player2):

        else:
            error_response = InvalidPlayernameError()
            response_body = error_response.message
            status = ErrorResponse.error_response(exception=InvalidPlayernameError)



        # response_body = f"{player1} {player2}".encode('utf-8')    # TODO: Исправить ответ на запрос


        headers = [('Content-Type', 'text/plain; charset=utf-8'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
            # TODO: добавить метод в сохранения имени в бд, проверка имени?

        return [response_body]

    else:
        response_body = b'Not Found'
        status = '404 Not Found'
        headers = [('Content-Type', 'text/plain'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]


# Запускаем сервер с использованием Waitress
if __name__ == '__main__':
    serve(TransLogger(application, setup_console_handler=False))
    serve(application, host='0.0.0.0', port=8080)
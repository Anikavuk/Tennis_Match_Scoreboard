from waitress import serve

# response = 'Hello world'.encode()



# НЕ УДАЛЯТЬ
# def app(environ, start_response):
#     status = '200 OK'
#     response_headers = [('Content-type', 'text/plain')]
#     start_response(status, response_headers)
#     return [b"Hello, world4"]
#
# # Запуск Waitress-сервера
# if __name__ == '__main__':
#     serve(app, host='0.0.0.0', port=8080)

from waitress import serve
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))


def application(environ, start_response):
    """Основная WSGI-функция для обработки запросов."""

    if environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/new-match':

        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length).decode('utf-8')

        form = parse_qs(body)

        player1 = form.get('player1')[0]
        player2 = form.get('player2')[0]

        response_body = f"{player1},{player2}".encode('utf-8')
        status = '200 OK'
        headers = [('Content-Type', 'text/plain; charset=utf-8'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        print(player1)
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
    serve(application, host='0.0.0.0', port=8080)
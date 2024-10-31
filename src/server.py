from urllib.parse import parse_qs
from waitress import serve
from paste.translogger import TransLogger
from src.controller.start_game_controller import StartGame


def application(environ, start_response):

    if environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/new-match':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length).decode('utf-8')

        form = parse_qs(body)
        start_game = StartGame()
        response = start_game.do_POST(form) # {400: 'You need to enter a different, unique nameone'}

        if type(response) == dict:
            status = list(response.keys())[0]
            response_body = list(response.values())[0]
        else:
            status = '200 OK'
            response_body = response.encode('utf-8')
        headers = [('Content-Type', 'text/plain; charset=utf-8'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)

        return [response_body]

    else:
        response_body = b'Not Found'
        status = '404 Not Found'
        headers = [('Content-Type', 'text/plain'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]


if __name__ == '__main__':
    serve(TransLogger(application, setup_console_handler=False))
    serve(application, host='0.0.0.0', port=8080)


from urllib.parse import parse_qs
from src.controller.start_game_controller import StartGame
from src.view.jinja_engine import render_template

def application(environ, start_response):
    if environ['PATH_INFO'] == '/':
        response_body = render_template('index.html').encode('utf-8')
        headers = [('Content-Type', 'text/html')]
        status = '200'
        start_response(status, headers)
        return [response_body]

    if environ['REQUEST_METHOD'] == 'GET' and environ['PATH_INFO'] == '/new-match':
        response_body = render_template('new-match.html').encode('utf-8')
        headers = [('Content-Type', 'text/html')]
        status = '200'
        start_response(status, headers)
        return [response_body]

    if environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/new-match':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length).decode('utf-8')

        form = parse_qs(body)
        start_game = StartGame()
        response = start_game.do_POST(form)  # {400: 'You need to enter a different, unique nameone'}

        if isinstance(response, dict):
            status = str(list(response.keys())[0])
            error_message = (list(response.values()))[0]
            response_body = error_message.encode('utf-8')
        else:
            status = '200'
            response_body = response.encode('utf-8')

        headers = [('Content-Type', 'text/plain; charset=utf-8'),
               ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]

    else:
        response_body = b'Not Found'
        status = '404 Not Found'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)
        return [response_body]






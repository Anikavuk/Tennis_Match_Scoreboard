from urllib.parse import parse_qs, urlencode
from src.controller.start_game_controller import PlayerHandler
from src.view.jinja_engine import render_template, render_template_messages

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
        names_of_players = PlayerHandler()
        response = names_of_players.start_game_handler()  # {400: 'You need to enter a different, unique name'}

        if isinstance(response, dict):
            # status = str(list(response.keys())[0]) TODO: можно убрать строчку, код 400
            error_message = (list(response.values()))[0]
            query_string = urlencode({'error': error_message}) # 'error=You+need+to+enter+a+different%2C+unique+name'

            headers = [('Location', '/messages?'+ query_string),
                       ('Content-Type', 'text/plain; charset=utf-8'),
                       ('Content-Length', '0')]
            start_response('302 Found', headers)
            return []


        else: # TODO: ндо исправить этот елси
            status = '200'
            response_body = response.encode('utf-8') # The names of the players have been successfully saved
            query_string = urlencode({'error': response_body})  # 'error=You+need+to+enter+a+different%2C+unique+name'
            headers = [('Location', '/match_score?' + query_string),
                       ('Content-Type', 'text/plain; charset=utf-8'),
                       ('Content-Length', '0')]
            start_response('302 Found', headers)
            return []

        headers = [('Content-Type', 'text/plain; charset=utf-8'),
               ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]

    elif environ['REQUEST_METHOD'] == 'GET' and environ['PATH_INFO'] == '/messages':
        query_string = environ.get('QUERY_STRING', '')
        params = parse_qs(query_string)
        error_message = params.get('error', [None])[0]
        response_body = render_template_messages('messages.html',
                                                 server_response=error_message).encode('utf-8')
        status = '200 OK'
        headers = [('Content-Type', 'text/html; charset=utf-8'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]

    elif environ['REQUEST_METHOD'] == 'GET' and environ['PATH_INFO'] == '/match_score':
        query_string = environ.get('QUERY_STRING', '')
        params = parse_qs(query_string)
        error_message = params.get('error', [None])[0]
        response_body = render_template_messages('messages.html',
                                                 server_response=error_message).encode('utf-8')
        status = '200 OK'
        headers = [('Content-Type', 'text/html; charset=utf-8'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]
    else:
        response_body = b'Not Found'
        status = '404 Not Found'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)
        return [response_body]






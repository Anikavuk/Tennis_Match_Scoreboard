from urllib.parse import parse_qs, urlencode

from src.handlers.match_score_handler import CurrentMatchHandler
from src.handlers.present_match_handler import MatchRegistrationHandler
from src.handlers.start_game_handler import PlayerHandler
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

        form = parse_qs(body)  # {'player1': ['Гршгг'], 'player2': ['Фршгг']}
        names_of_players = PlayerHandler()  # <src.handlers.start_game_handler.PlayerHandler object at 0x0000024C54FC2B50>
        response = names_of_players.start_game_handler(form)  # {184: 'qyрrr', 185: 'aeгrrr'}

        if len(response) == 1:
            error_message = (list(response.values()))[0]
            query_string = urlencode({'error': error_message})  # 'error=You+need+to+enter+a+different%2C+unique+name'

            headers = [('Location', '/messages?' + query_string),
                       ('Content-Type', 'text/plain; charset=utf-8'),
                       ('Content-Length', '0')]
            start_response('302 Found', headers)
            return []
        if len(response) > 1:
            new_match = MatchRegistrationHandler()
            new_match_uuid = new_match.get_match_uuid_by_player_ids(response)
            query_string = urlencode({'uuid': new_match_uuid})

            headers = [('Location', '/match-score?' + query_string),
                       ('Content-Type', 'text/plain; charset=utf-8'),
                       ('Content-Length', '0')]
            start_response('302 Found', headers)
            return []


    elif environ['REQUEST_METHOD'] == 'GET' and environ['PATH_INFO'] == '/messages':
        query_string = environ.get('QUERY_STRING', '')
        params = parse_qs(query_string)
        error_message = params.get('error', [None])[0]
        response_body = render_template('messages.html',
                                        server_response=error_message).encode('utf-8')
        status = '200 OK'
        headers = [('Content-Type', 'text/html; charset=utf-8'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]

    elif environ['REQUEST_METHOD'] == 'GET' and environ['PATH_INFO'] == '/match-score':
        query_string = environ.get('QUERY_STRING', '')
        params = parse_qs(query_string)
        uuid_match = params.get('uuid', [None])[0]
        current_match = CurrentMatchHandler()
        response = current_match.curren_match(uuid_match)
        response_body = render_template('match_score.html',
                                        player1=response[0],
                                        player2=response[1]).encode('utf-8')
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

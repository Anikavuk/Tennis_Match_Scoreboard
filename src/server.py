from urllib.parse import parse_qs, urlencode, urlparse

from pagination import Pagination
from src.errors import NonExistentNameError, SameNamesError
from src.handlers.match_score_handler import CurrentMatchHandler
from src.handlers.matches_handler import FinishedMatchesHandler
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

        form = parse_qs(body)
        if form['player1'] == form['player2']:
            error_response = SameNamesError()
            error_message = error_response.message
            query_string = urlencode({'error': error_message})

            headers = [('Location', '/messages?' + query_string),
                       ('Content-Type', 'text/plain; charset=utf-8'),
                       ('Content-Length', '0')]
            start_response('302 Found', headers)
            return []

        else:
            names_of_players = PlayerHandler()
            match_data = names_of_players.start_game_handler(form)

            if len(match_data) == 1:
                error_message = (list(match_data.values()))[0]
                query_string = urlencode({'error': error_message})
                headers = [('Location', '/messages?' + query_string),
                           ('Content-Type', 'text/plain; charset=utf-8'),
                           ('Content-Length', '0')]
                start_response('302 Found', headers)
                return []
            if len(match_data) > 1:
                new_match = MatchRegistrationHandler()
                new_match_uuid = new_match.get_match_uuid_by_player_ids(match_data)
                query_string = urlencode({'uuid': new_match_uuid}) # 'uuid=ff004c18-c186-4319-bcd8-46581fe9f7b7'

                headers = [('Location', '/match-score?' + query_string),
                           ('Content-Type', 'text/plain; charset=utf-8'),
                           ('Content-Length', '0')]
                start_response('302 Found', headers)
                return []
    if environ['REQUEST_METHOD'] == 'GET' and environ['PATH_INFO'] == '/matches':
        query_string = environ.get('QUERY_STRING', '')
        params = parse_qs(query_string)
        page_number = int(params.get('page', ['1'])[0])
        filter_by_player_name = params.get('filter_by_player_name', [''])[0]
        matches_handler = FinishedMatchesHandler()
        if filter_by_player_name:
            filtered_matches = matches_handler.find_matches_by_player_name(filter_by_player_name)
        else:
            filtered_matches = matches_handler.get_all_matches()

        pagination = Pagination()
        paged_matches = pagination.paginate_list(filtered_matches)

        if not paged_matches or page_number > len(paged_matches):
            error_obj = NonExistentNameError()
            query_string = urlencode({'error': error_obj.message})
            headers = [('Location', '/messages?' + query_string),
                       ('Content-Type', 'text/plain; charset=utf-8'),
                       ('Content-Length', '0')]
            start_response('302 Found', headers)
            return []

        current_page_matches = paged_matches[page_number - 1]
        response_body = render_template(
            'matches.html',
            filter_by_player_name=filter_by_player_name,
            matches=current_page_matches,
            current_page=page_number,
            total_pages=len(paged_matches),
            matches_per_page=len(current_page_matches)
        ).encode('utf-8')

        headers = [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(response_body)))
        ]

        start_response('200 OK', headers)
        return [response_body]

    if environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/match-score':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length).decode('utf-8')

        form = parse_qs(body) # {'winner': ['player1']}
        uuid_match = form.get('uuid', [None])[0]
        winner = form.get('winner')[0]
        match_handler = CurrentMatchHandler()

        current_match_state = match_handler.process_point_won(uuid_match, winner)
        if current_match_state.winner:
            response_body = render_template('match_finished.html',
                                            player1=current_match_state.player1,
                                            player2=current_match_state.player2,
                                            set1=current_match_state.set1,
                                            set2=current_match_state.set2,
                                            match_id=uuid_match).encode('utf-8')
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            status = '200 OK'
            start_response(status, headers)
            return [response_body]


        response_body = render_template('match_score.html',
                                        player1=current_match_state.player1,
                                        player2=current_match_state.player2,
                                        set1=current_match_state.set1,
                                        set2=current_match_state.set2,
                                        games1=current_match_state.game1,
                                        games2=current_match_state.game2,
                                        points1=current_match_state.points1,
                                        points2=current_match_state.points2, match_id=uuid_match).encode('utf-8')
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        status = '200 OK'
        start_response(status, headers)
        return [response_body]


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
        query_string = environ.get('QUERY_STRING', '') # 'uuid=ff004c18-c186-4319-bcd8-46581fe9f7b7'
        params = parse_qs(query_string)
        uuid_match = params.get('uuid', [None])[0]
        match_handler = CurrentMatchHandler()
        match_data = match_handler.get_match_score(
            uuid_match)  # ScoreDTO(player1='ПА', player2='ААА', set1=2, set2=0, game1=6, game2=4, points1='AD', points2=15)

        response_body = render_template('match_score.html',
                                        player1=match_data.player1,
                                        player2=match_data.player2,
                                        set1=match_data.set1,
                                        set2=match_data.set2,
                                        games1=match_data.game1,
                                        games2=match_data.game2,
                                        points1=match_data.points1,
                                        points2=match_data.points2, match_id = uuid_match).encode('utf-8')
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

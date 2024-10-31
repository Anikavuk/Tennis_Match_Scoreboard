from src.errors import ErrorResponse, InvalidPlayernameError, IntegrityError
from src.dao.player_DAO import PlayerDAO
from src.controller.base_controller import BaseController

class StartGame(BaseController):

    def do_POST(self, form):
        try:
            # проверка на None, если False
            players_names = {key: form.get(key)[0] if form.get(key) else None for key in ['player1', 'player2']}
            if not all(players_names.values()):
                raise InvalidPlayernameError()

            # проверка на валидацию
            players_valid = {key: value for key, value in players_names.items() if PlayerDAO.is_valid_username(value)}
            if not players_valid or ('player1' not in players_valid or 'player2' not in players_valid):
                raise InvalidPlayernameError()

            players_save = {key: value for key, value in players_valid.items() if PlayerDAO.save_player(value)}
            response_body = f"Имена игроков успешно сохранились!".encode('utf-8')
            if not players_save:
                raise IntegrityError()
            return [response_body]
        except InvalidPlayernameError:
            return ErrorResponse.error_response(exception=InvalidPlayernameError)
        except IntegrityError:
            return ErrorResponse.error_response(exception=IntegrityError)
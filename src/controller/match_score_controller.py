from src.controller.base_controller import BaseController
from src.dao.player_DAO import PlayerDAO
from src.errors import ErrorResponse, InvalidPlayernameError, IntegrityError


class MatchRegistrationHandler(BaseController):

    def start_game_handler(self, form): #TODO УДАЛИ ЗДЕСЬ ВСЕ
        try:
            # Проверка на None
            players_names = {key: form.get(key)[0] if form.get(key) else None for key in ['player1', 'player2']}
            if not all(players_names.values()):
                raise InvalidPlayernameError

            # Проверка на валидацию
            players_valid = {key: True for key, value in players_names.items() if PlayerDAO.is_valid_username(value)}
            if not players_valid or ('player1' not in players_valid or 'player2' not in players_valid):
                raise InvalidPlayernameError

            # Проверка на дубликат в db
            players_save = {}
            for key, value in players_names.items():
                if PlayerDAO.save_player(value):
                    players_save[key] = True
                else:
                    raise IntegrityError

            response_body = "The names of the players have been successfully saved"
            return response_body
        except InvalidPlayernameError:
            return ErrorResponse.error_response(exception=InvalidPlayernameError())
        except IntegrityError:
            return ErrorResponse.error_response(exception=IntegrityError())
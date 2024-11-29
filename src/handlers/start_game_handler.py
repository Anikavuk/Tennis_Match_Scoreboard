from src.dao.player_DAO import PlayerDAO
from src.errors import BaseAPIException, InvalidPlayernameError, IntegrityError, SameNamesError
from src.handlers.base_handler import BaseController


class PlayerHandler(BaseController):
    """
    Контроллер-обработчик '/new-match'
    """

    def start_game_handler(self, form: dict):
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
                player_id = PlayerDAO.save_player(value)
                if type(player_id) == int:
                    players_save[player_id] = value
                else:
                    raise SameNamesError

            return players_save
        except InvalidPlayernameError:
            return BaseAPIException.error_response(exception=InvalidPlayernameError())
        except IntegrityError:
            return BaseAPIException.error_response(exception=IntegrityError())
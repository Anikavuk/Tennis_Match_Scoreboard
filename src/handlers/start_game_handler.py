from typing import List, Dict

from src.dao.player_DAO import PlayerDAO
from src.dto.player_DTO import PlayerDTO
from src.errors import BaseAPIException, InvalidPlayernameError, IntegrityError, SameNamesError
from src.handlers.base_handler import BaseController


class PlayerHandler(BaseController):
    """
    Контроллер-обработчик '/new-match'
    """

    def start_game_handler(self, form: Dict[str, List[str]]) -> List[PlayerDTO]:
        """Обрабатывает начало игры, проверяет корректность введенных данных и сохраняет новых игроков в базу данных.

            Аргументы:
            - form (Dict[str, List[str]]): Форма с данными об игроках, представленная в виде словаря.

            Возвращает:
            - List[PlayerDTO]: Список объектов PlayerDTO, представляющих игроков, участвующих в игре.

            Исключения:
            - InvalidPlayernameError: Возникает, если одно из имен игроков пустое или некорректное.
            - IntegrityError: Возникает, если происходит дублирование имени, которое уже есть в базе данных.
            """
        try:
            # Проверка на пустые имена игроков
            players_names = {key: form.get(key)[0] if form.get(key) else None for key in ['player1', 'player2']}
            if not all(players_names.values()):
                raise InvalidPlayernameError

            # Проверка валидности имен игроков
            if not all(PlayerDAO.is_valid_username(name) for name in players_names.values()):
                raise InvalidPlayernameError

            # Проверка на дубликат в db
            players_dto = []
            for key, name in players_names.items():
                player_id = PlayerDAO._save_player(name)
                if isinstance(player_id, int):
                    players_dto.append(PlayerDTO(player_id, name))
                else:
                    raise SameNamesError

            return players_dto
        except InvalidPlayernameError:
            return BaseAPIException.error_response(exception=InvalidPlayernameError())
        except IntegrityError:
            return BaseAPIException.error_response(exception=IntegrityError())

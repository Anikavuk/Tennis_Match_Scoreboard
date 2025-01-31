from typing import List

from src.dao.match_DAO import MatchDAO
from src.dto.match_DTO import MatchDTO
from src.dto.player_DTO import PlayerDTO
from src.errors import BaseAPIException, InvalidPlayernameError, IntegrityError
from src.handlers.base_handler import BaseController


class MatchRegistrationHandler(BaseController):
    """
    Контроллер-обработчик '/new-match'
    """

    def _get_match_uuid_by_player_ids(self, form: List[PlayerDTO]) -> str:
        """
        Получает UUID текущего матча по идентификаторам двух игроков.
            Эта функция извлекает ID игроков из переданного списка объектов PlayerDTO,
            сохраняет текущий матч в базе данных и возвращает UUID этого матча.

            @param: form (List[PlayerDTO]): Список объектов PlayerDTO, содержащих информацию об игроках.
            @return: UUID текущего матча: str
            @raise: InvalidPlayernameError: Возникает, если обнаружено неверное имя игрока.
                    IntegrityError: Возникает, если произошла ошибка целостности данных при работе с базой данных.
        """
        try:
            players_id_1 = getattr(form[0], 'id')
            players_id_2 = getattr(form[1], 'id')
            uuid = MatchDAO._save_current_match(players_id_1, players_id_2)
            result = MatchDTO(uuid, players_id_1, players_id_2)
            return result.uuid
        except InvalidPlayernameError:
            return BaseAPIException.error_response(exception=InvalidPlayernameError())
        except IntegrityError:
            return BaseAPIException.error_response(exception=IntegrityError())

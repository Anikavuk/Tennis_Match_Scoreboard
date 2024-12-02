from typing import List

from src.dao.match_DAO import MatchDAO
from src.dto.player_DTO import PlayerDTO
from src.errors import BaseAPIException, DatabaseErrorException
from src.handlers.base_handler import BaseController


class CurrentMatchHandler(BaseController):
    """
    Контроллер-обработчик '/match-score'
    """

    @staticmethod
    def get_current_match(uuid_match: str) -> List[PlayerDTO]:
        try:
            match_dao = MatchDAO()
            names_of_players = match_dao.get_match_by_uuid_with_names(uuid_match)
            players_DTO = [PlayerDTO(id, name) for id, name in
                           names_of_players.items()]
            return players_DTO
        except DatabaseErrorException:
            return BaseAPIException.error_response(exception=DatabaseErrorException())
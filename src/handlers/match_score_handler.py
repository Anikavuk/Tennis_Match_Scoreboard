from src.handlers.base_handler import BaseController
from src.dao.match_DAO import MatchDAO
from src.errors import BaseAPIException, DatabaseErrorException


class CurrentMatchHandler(BaseController):
    """
    Контроллер-обработчик '/match-score'
    """

    @staticmethod
    def curren_match(uuid_match: str):
        try:
            match_dao = MatchDAO()
            names_of_players = match_dao.get_match_by_uuid_with_names(uuid_match)

            return names_of_players
        except DatabaseErrorException:
            return BaseAPIException.error_response(exception=DatabaseErrorException())


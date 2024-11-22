from src.handlers.base_handler import BaseController
from src.dao.match_DAO import MatchDAO
from src.errors import BaseAPIException, DatabaseErrorException


class CurrentMatchHandler(BaseController):

    @staticmethod
    def curren_match(uuid_match):
        try:
            match_obj = MatchDAO()
            names_of_players = match_obj.get_match_by_uuid_with_names(uuid_match)

            return names_of_players
        except DatabaseErrorException:
            return BaseAPIException.error_response(exception=DatabaseErrorException())


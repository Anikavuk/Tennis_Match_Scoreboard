from src.dao.match_DAO import MatchDAO
from src.errors import BaseAPIException, InvalidPlayernameError, IntegrityError


class FinishedMatchesHandler:
    """
    Контроллер-обработчик '/matches'
    """
    def get_all_matсhes(self):
        try:
            match_dao = MatchDAO()
            all_matches_list = match_dao.get_all_matches()
            completed_matches = [match for match in all_matches_list if match['winner'] is not None]
            return completed_matches
        except InvalidPlayernameError:
            return BaseAPIException.error_response(exception=InvalidPlayernameError())
        except IntegrityError:
            return BaseAPIException.error_response(exception=IntegrityError())
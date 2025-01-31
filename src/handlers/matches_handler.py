from src.dao.match_DAO import MatchDAO
from src.errors import BaseAPIException, InvalidPlayernameError, IntegrityError
from src.dto.match_DTO import MatchDTO


class FinishedMatchesHandler:
    """
    Контроллер-обработчик '/matches'
    """

    def get_all_matches(self):
        try:
            match_dao = MatchDAO()
            all_matches_list = match_dao._get_all_matches()
            completed_matches = [match for match in all_matches_list if match['winner'] is not None]
            return completed_matches
        except InvalidPlayernameError:
            return BaseAPIException.error_response(exception=InvalidPlayernameError())
        except IntegrityError:
            return BaseAPIException.error_response(exception=IntegrityError())

    def find_matches_by_player_name(self, name:str):
        try:
            match_dao = MatchDAO()
            all_matches_list = match_dao._list_player_matches(name)
            completed_matches = [match for match in all_matches_list if match['winner'] is not None]
            return completed_matches
        except InvalidPlayernameError:
            return BaseAPIException.error_response(exception=InvalidPlayernameError())
        except IntegrityError:
            return BaseAPIException.error_response(exception=IntegrityError())

# ddd = FinishedMatchesHandler()
# print(ddd.get_all_matches())
# fff = ddd.find_matches_by_player_name('io')
# fff['filter_by_name'] = ["['io']"]
# print(fff) [{'filter_by_name': names_of_players}], 'player1': 'io', 'player2': 'rt', 'winner': 'io'},
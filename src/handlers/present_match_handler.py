from src.dao.match_DAO import MatchDAO
from src.errors import BaseAPIException, InvalidPlayernameError, IntegrityError
from src.handlers.base_handler import BaseController


class MatchRegistrationHandler(BaseController):
    """
    Контроллер-обработчик '/new-match'
    """
    def get_match_uuid_by_player_ids(self, form: dict):
        try:
            players_id_1 = [id_player for id_player in form.keys()][0]
            players_id_2 = [id_player for id_player in form.keys()][1]
            match_uuid = MatchDAO.save_current_match(players_id_1, players_id_2)
            return match_uuid
        except InvalidPlayernameError:
            return BaseAPIException.error_response(exception=InvalidPlayernameError())
        except IntegrityError:
            return BaseAPIException.error_response(exception=IntegrityError())

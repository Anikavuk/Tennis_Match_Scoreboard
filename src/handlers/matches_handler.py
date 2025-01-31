from src.dao.match_DAO import MatchDAO
from src.errors import BaseAPIException, InvalidPlayernameError, IntegrityError


class FinishedMatchesHandler:
    """
    Контроллер-обработчик '/matches'
    """

    def _get_all_matches(self):
        """
        Получает все завершенные матчи из базы данных.
            Этот метод получает список всех матчей из базы данных,
            фильтрует те, у которых указан победитель, и возвращает их.
            @return: list: Список завершенных матчей.
            @raise: InvalidPlayernameError: Возникает, если обнаружено неверное имя игрока.
                    IntegrityError: Возникает, если ввели имя, которое уже сохранено в базе данных.
        """
        try:
            match_dao = MatchDAO()
            all_matches_list = match_dao._get_all_matches()
            completed_matches = [match for match in all_matches_list if match['winner'] is not None]
            return completed_matches
        except InvalidPlayernameError:
            return BaseAPIException.error_response(exception=InvalidPlayernameError())
        except IntegrityError:
            return BaseAPIException.error_response(exception=IntegrityError())

    def _find_matches_by_player_name(self, name: str):
        """
        Находит завершенные матчи (с победителем) для указанного игрока по имени.
            @param: name (str): Имя игрока, для которого нужно найти матчи.
            @return:  List[Dict[str, Any]]: Список словарей, представляющих завершенные матчи.
                      Каждый словарь содержит информацию о матче, включая имена игроков, сеты, игры и очки.
            @raise: InvalidPlayernameError: Если имя игрока неверное или не существует.
                    IntegrityError: Если произошла ошибка целостности данных при выполнении запроса.
        """
        try:
            match_dao = MatchDAO()
            all_matches_list = match_dao._list_player_matches(name)
            completed_matches = [match for match in all_matches_list if match['winner'] is not None]
            return completed_matches
        except InvalidPlayernameError:
            return BaseAPIException.error_response(exception=InvalidPlayernameError())
        except IntegrityError:
            return BaseAPIException.error_response(exception=IntegrityError())

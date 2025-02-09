from typing import Dict, Union

from src.dao.match_DAO import MatchDAO
from src.dao.player_DAO import PlayerDAO
from src.dto.score_DTO import ScoreDTO
from src.errors import BaseAPIException, DatabaseErrorException, MatchNotFoundException, PlayerNotFoundException
from src.handlers.base_handler import BaseController
from src.service.service import Tennis_Score, ScoreCalculator, Tiebreaker


class CurrentMatchHandler(BaseController):
    """
    Контроллер-обработчик '/match-score'
    """

    @staticmethod
    def _get_match_score(uuid_match: str) -> Union[ScoreDTO, BaseAPIException]:
        """Выгружает информацию о матче по uuid
        :param uuid_match : str уникальный идентификатор матча.
        :return: ScoreDTO объект ScoreDTO
        Raises: DatabaseErrorException: Если произошла ошибка при подключении к базе данных или выполнении запроса.
        """
        try:
            match_dao = MatchDAO()
            match_info = match_dao._get_match_info_by_uuid(uuid_match)
            if len(match_info)==1:
                return MatchNotFoundException("Матча с таким UUID не существует в базе данных")
            if isinstance(match_info, dict):
                match_score_DTO = ScoreDTO(**match_info)
                return match_score_DTO
            return BaseAPIException.error_response(exception=MatchNotFoundException())
        except DatabaseErrorException:
            return BaseAPIException.error_response(exception=DatabaseErrorException())

    def _process_point_won(self, uuid_match: str, winner: str) -> Union[ScoreDTO, BaseAPIException]:
        """
            Обрабатывает ситуацию, когда игрок выигрывает очко. Обновляет счет в гейме, в сете.
            Проверяет счет на деус, если points у игроков равные 40, тогда побед должно быть 2 раза подряд
            Проверяет счет на тайбрейк, если game1 и game2 равны 6, тогда points изменяются от 0 до 7

            @param uuid_match: str уникальный идентификатор матча.
            @param winner: имя игрока победителя
            @return: объект ScoreDTO
        """
        # Преобразует score объекта ScoreDTO в словарь
        score_dto = self._get_match_score(uuid_match)
        if isinstance(score_dto, ScoreDTO):
            current_score_dict = self._convert_score_dto_to_dict(score_dto)
        else:
            return BaseAPIException.error_response(exception=MatchNotFoundException())
        match_logic = Tennis_Score()

        score_logic = ScoreCalculator(current_score_dict)
        # Проверка на деус
        if score_logic.is_deuce_condition_met():
            current_score_dict = score_logic.process_deuce_game(winner)
        # Проверка на AD в points
        elif score_logic.is_there_an_advantage():
            current_score_dict = score_logic.process_deuce_game(winner)
        # Проверка на тайбрейк
        elif score_logic.is_tiebreaker_condition_met():
            tiebreaker_logic = Tiebreaker()
            current_score_dict[winner]['points'] = tiebreaker_logic._counting_of_points(
                current_score_dict[winner]['points'])
            score_logic.update_games(current_score_dict, winner)
        # Если обычный счет
        else:
            current_score_dict[winner]['points'] = match_logic._counting_of_points(
                current_score_dict[winner]['points'])
            score_logic.update_games(current_score_dict, winner)

        score_logic.update_set(current_score_dict)  # Обновляет счет set

        updated_score = {'match_data': current_score_dict}  # Обновленный счет сохраняется в бд

        match_dao = MatchDAO()
        match_dao.update_match(uuid_match, updated_score)
        # Если победитель определен, сохраняем информацию о нем
        if score_logic.check_the_winner(current_score_dict):
            self._determine_and_save_winner(uuid_match)
        return self._get_match_score(uuid_match)

    def _convert_score_dto_to_dict(self, score_dto: ScoreDTO) -> Dict:
        """Преобразует объект ScoreDTO в словарь.

        Аргументы:
        - score_dto (ScoreDTO): Объект ScoreDTO, содержащий данные о счете матча.

        Возвращает:
        - dict: Словарь, представляющий счет матча в формате:
          {
              "player1": {"set": int, "game": int, "points": int},
              "player2": {"set": int, "game": int, "points": int}
          }

        Примечание:
        - Поле 'winner' из ScoreDTO не включается в результирующий словарь.
        """
        return {
            "player1": {
                "set": score_dto.set1,
                "game": score_dto.game1,
                "points": score_dto.points1,
            },
            "player2": {
                "set": score_dto.set2,
                "game": score_dto.game2,
                "points": score_dto.points2,
            }
        }

    def _determine_and_save_winner(self, uuid_match: str) -> Union[int, BaseAPIException]:
        """ Метод проверяет на победу игрока,
        сохраяет в матче по uuid в winner
        и возвращает id игрока победителя"""

        # Получаем объект ScoreDTO для указанного uuid матча
        score_dto_obj = self._get_match_score(uuid_match)
        if isinstance(score_dto_obj, BaseAPIException):
            return BaseAPIException.error_response(exception=MatchNotFoundException())
        if score_dto_obj.set1 == 3:
            score_dto_obj.winner = score_dto_obj.player1
        elif score_dto_obj.set2 == 3:
            score_dto_obj.winner = score_dto_obj.player2

        if isinstance(score_dto_obj.winner, str):
            obj_player_dao = PlayerDAO(score_dto_obj.winner)
            winner = obj_player_dao._save_player(score_dto_obj.winner)
            if isinstance(winner, int):
                match_dao = MatchDAO()
                match_dao.update_winner(uuid_match, winner)
        else:
            raise BaseAPIException.error_response(exception=PlayerNotFoundException())
        return winner

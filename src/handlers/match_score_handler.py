from typing import List

from src.dao.match_DAO import MatchDAO
from src.dto.score_DTO import ScoreDTO
from src.errors import BaseAPIException, DatabaseErrorException
from src.handlers.base_handler import BaseController
from src.service.service import Tennis_Score, ScoreCalculator, Tiebreaker


class CurrentMatchHandler(BaseController):
    """
    Контроллер-обработчик '/match-score'
    """

    @staticmethod
    def get_match_score(match_uuid: str) -> List[ScoreDTO]:
        """Метод возвращает информацию о матче без победителя"""
        try:
            match_dao = MatchDAO()
            match_info = match_dao.get_match_info_by_uuid(match_uuid) # {'game1': 0, 'game2': 1, 'player1': 'Леха', 'player2': 'Женя', 'points1': 30, 'points2': 15, 'set1': 2, 'set2': 1}
            match_score_DTO = ScoreDTO(**match_info) # ScoreDTO(player1='Леха', player2='Женя', winner=None, set1=2, set2=1, game1=0, game2=1, points1=30, points2=15)
            return match_score_DTO  # ScoreDTO(player1='ПА', player2='Ксюша', set1=0, set2=0, game1=0, game2=0, points1=0, points2=0)
        except DatabaseErrorException:
            return BaseAPIException.error_response(exception=DatabaseErrorException())

    def process_point_won(self, uuid_match: str, winner: str):
        """
            Обрабатывает ситуацию, когда игрок выигрывает очко. Обновляет счет в матче.
            Проверяет счет на тайбрейк, если game1 и game2 равны 6, тогда points изменяются от 0 до 7
            Возвращает объект ScoreDTO, представляющий обновленный счет матча.
        """
        current_score_dict = self._convert_score_dto_to_dict(self.get_match_score(uuid_match))
        score_logic = Tennis_Score()

        match_logic = ScoreCalculator(current_score_dict)
        if match_logic.check_deuce_condition():
            match_logic.process_deuce_game(winner)
        if match_logic.check_tiebreaker_condition():
            tiebreaker_logic  = Tiebreaker()
            current_score_dict[winner]['points'] = tiebreaker_logic.counting_of_points(
            current_score_dict[winner]['points'])
        else:
            current_score_dict[winner]['points'] = score_logic.counting_of_points(
            current_score_dict[winner]['points'])



        updated_score = {'match_data': current_score_dict}

        match_dao = MatchDAO()
        match_dao.update_match(uuid_match, updated_score)
        return self.get_match_score(uuid_match)

    def _convert_score_dto_to_dict(self, score_dto):
        """Преобразует из ScoreDTO(player1='ПА', player2='еее', set1=0, set2=0, game1=0, game2=0, points1=0, points2=0)
        в {'player1': {'set': 0, 'game': 0, 'points': 0}, 'player2': {'set': 0, 'game': 0, 'points': 0}}"""
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

    def process_match_score(self, uuid_match: str):
        """ Проверяет и обновляет счетчики геймов и сетов."""
        current_score = self._convert_score_dto_to_dict(self.get_match_score(
            uuid_match))  # {'player1': {'set': 0, 'game': 0, 'points': 40}, 'player2': {'set': 0, 'game': 0, 'points': 30}}
        score_calculator = ScoreCalculator(current_score)
        score_calculator.update_games(current_score) #  """Изменяет game у игроков и обнуляет points у всех игроков"""
        score_calculator.update_set(current_score)  # """Изменяет set у игроков и обнуляет game у всех игроков"""
        updated_score = {'match_data': current_score}

        match_dao = MatchDAO()
        match_dao.update_match(uuid_match, updated_score)
        return self.get_match_score(uuid_match)

# winner = 'player1'
# match_uuid = 'eb6969bd-a0f6-4609-a52f-8ae42a9a2f81'
# dddd = CurrentMatchHandler()
#
#
# print(dddd.process_point_won(match_uuid, winner))
#

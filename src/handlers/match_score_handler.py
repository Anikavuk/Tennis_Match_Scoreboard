from typing import List
from src.service.service import Tennis_Score, ScoreCalculator
from src.dao.match_DAO import MatchDAO
from src.dto.score_DTO import ScoreDTO
from src.errors import BaseAPIException, DatabaseErrorException
from src.handlers.base_handler import BaseController


class CurrentMatchHandler(BaseController):
    """
    Контроллер-обработчик '/match-score'
    """

    @staticmethod
    def get_current_match(uuid_match: str) -> List[ScoreDTO]:
        """Метод возвращает информацию о матче без победителя"""
        try:
            match_dao = MatchDAO()
            match_info = match_dao.get_match_info_by_uuid(uuid_match)
            match_score_DTO = ScoreDTO(**match_info)
            return match_score_DTO  # ScoreDTO(player1='ПА', player2='Ксюша', set1=0, set2=0, game1=0, game2=0, points1=0, points2=0)
        except DatabaseErrorException:
            return BaseAPIException.error_response(exception=DatabaseErrorException())

    def update_score_match(self, match_id: str, winner : str):
        current_play = self.convert_score_dto_to_dict(self.get_current_match(match_id))
        tennis_play = Tennis_Score()
        current_play[winner]['points'] = tennis_play.counting_of_points(current_play[winner]['points'])

        score_update = {'match_data': current_play}

        match_dao = MatchDAO()
        match_dao.update_match(match_id, score_update)
        return self.get_current_match(match_id)

    def convert_score_dto_to_dict(self, score_dto):
        """Преобразуем из ScoreDTO(player1='ПА', player2='еее', set1=0, set2=0, game1=0, game2=0, points1=0, points2=0)
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

    def checking_score(self, match_id: str):
        current_score = self.convert_score_dto_to_dict(self.get_current_match(match_id)) # {'player1': {'set': 0, 'game': 0, 'points': 40}, 'player2': {'set': 0, 'game': 0, 'points': 30}}
        current_match = ScoreCalculator(current_score)
        current_match.update_games(current_score)
        current_match.update_set(current_score)
        a = current_match.winner(current_score)

        current_score_match = {'match_data': current_score}
        tennis = MatchDAO()
        tennis.update_match(match_id, current_score_match)
        return self.get_current_match(match_id), a

dddd = CurrentMatchHandler()
sss = dddd.update_score_match('f472d446-8290-41fd-9382-6ed5ab300bc3', 'player2')
print(dddd.checking_score('f472d446-8290-41fd-9382-6ed5ab300bc3'))

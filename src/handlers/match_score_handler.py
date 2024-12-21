from typing import List

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
            return match_score_DTO # ScoreDTO(player1='ПА', player2='Ксюша', set1=0, set2=0, game1=0, game2=0, points1=0, points2=0)
        except DatabaseErrorException:
            return BaseAPIException.error_response(exception=DatabaseErrorException())



    def update_score(self, player, point):
        score = MatchDAO.update_match()


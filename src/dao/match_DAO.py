from typing import List, Dict, Any, Union, cast

from sqlalchemy.exc import OperationalError

from src.db.database import engine, Session
from src.db.models import Match
from src.errors import BaseAPIException, DatabaseErrorException, MatchNotFoundException


class MatchDAO:
    """Класс для работы с таблицей matches"""

    @staticmethod
    def _save_current_match(player1_id: int, player2_id: int) -> str:
        """Сохранение текущего матча.
        :param player1_id: int
        :param player2_id: int
        :return uuid: str"""
        with Session(autoflush=False, bind=engine) as db:
            match = Match(player1_id=player1_id,
                          player2_id=player2_id,
                          score={"match_data":
                                     {"player1": {"set": 0, "game": 0, "points": 0},
                                      "player2": {"set": 0, "game": 0, "points": 0}}})
            db.add(match)
            db.commit()
            return match.uuid

    def _get_and_update_match(self, uuid: str, field_name: str, new_value: Any) -> None:
        """
        Получает матч по UUID и обновляет указанное поле.
        :param uuid : str Уникальный идентификатор матча.
        :param    field_name: str Имя поля, которое нужно обновить. Может быть 'score' или 'winner_id'.
        :param    new_value: Any Новое значение для указанного поля.
        Raises: OperationalError Если произошла ошибка при подключении к базе данных.
        """
        try:
            with Session(autoflush=False, bind=engine) as db:
                match = db.query(Match).filter(Match.uuid == uuid).first()
                setattr(match, field_name, new_value)
                db.commit()
        except OperationalError:
            return BaseAPIException.error_response(exception=DatabaseErrorException())

    def update_match(self, uuid: str, score_update: Dict) -> None:
        """Изменяет счет матча.
        :param uuid : str Уникальный идентификатор матча.
        :param score_update: json Обновленный счет матча.
        """
        self._get_and_update_match(uuid, 'score', score_update)

    def update_winner(self, uuid: str, winner: int) -> None:
        """Добавление победителя в завершенный матч
        :param uuid : str Уникальный идентификатор матча.
        :param winner: int ID игрока победителя.
        """
        self._get_and_update_match(uuid, 'winner_id', winner)

    def _get_all_matches(self) -> List[Dict[str, Any]]:
        """Выгрузка всех матчей
        Returns: List[Dict[str, Any]]
           Список словарей, где каждый словарь содержит информацию о матче:
           - 'player1': имя первого игрока в матче.
           - 'player2': имя второго игрока в матче.
           - 'winner': имя победителя матча (если есть), иначе None.
        Raises: OperationalError Если произошла ошибка при подключении к базе данных.
        """
        try:
            with (Session(autoflush=False, bind=engine) as bd):
                matches_query = bd.query(Match)
                results = matches_query.all()

                matches = []
                for match in results:
                    matches.append({'player1': match.player1.name,
                                    'player2': match.player2.name,
                                    'winner': match.winner.name if match.winner else None
                                    })

                return matches
        except OperationalError:
            return BaseAPIException.error_response(exception=DatabaseErrorException())

    def _list_player_matches(self, player_name: str) -> List[Dict[str, Any]]:
        """
        Выгрузка всех матчей с определенным игроком.
        :param player_name : str    Имя игрока, матчи которого нужно получить.
        Returns: List[Dict[str, Any]]
           Список словарей, где каждый словарь содержит информацию о матче:
           - 'player1': имя первого игрока в матче.
           - 'player2': имя второго игрока в матче.
           - 'winner': имя победителя матча (если есть), иначе None.
        Raises: OperationalError Если произошла ошибка при подключении к базе данных.
        """
        try:
            with Session(autoflush=False, bind=engine) as db:
                matches = db.query(Match).filter(
                    (Match.player1.has(name=player_name)) | (Match.player2.has(name=player_name))).all()
                all_matches = [{'player1': match.player1.name,
                                'player2': match.player2.name,
                                'winner': match.winner.name if match.winner else None}
                               for match in matches]
                return all_matches
        except OperationalError:
            return BaseAPIException.error_response(exception=DatabaseErrorException())

    def _get_match_info_by_uuid(self, uuid: str) -> Union[Dict[str, Any], BaseAPIException]:
        """выгрузка матча по uuid
             :param uuid : str Уникальный идентификатор матча.
             :return: Union[Dict[str, Any], BaseAPIException]: Словарь с информацией о матче или
                                                    объект исключения, если произошла ошибка.
            Raises: OperationalError: Если произошла ошибка при подключении к базе данных или выполнении запроса.
        """
        try:
            with Session(autoflush=False, bind=engine) as db:
                match = db.query(Match).filter(Match.uuid == uuid).first()
                if match is None:
                    return BaseAPIException.error_response(
                        exception=MatchNotFoundException())

                # Явное приведение score к Dict[str, Any] с помощью cast
                score_dict: Dict[str, Any] = cast(Dict[str, Any], match.score)

                result_dict = {
                    'player1': match.player1.name,
                    'player2': match.player2.name,
                    'set1': score_dict['match_data']['player1']['set'],
                    'game1': score_dict['match_data']['player1']['game'],
                    'points1': score_dict['match_data']['player1']['points'],
                    'set2': score_dict['match_data']['player2']['set'],
                    'game2': score_dict['match_data']['player2']['game'],
                    'points2': score_dict['match_data']['player2']['points'],
                    'winner': match.winner_id
                }
                return result_dict
        except OperationalError:
            return BaseAPIException.error_response(exception=DatabaseErrorException())

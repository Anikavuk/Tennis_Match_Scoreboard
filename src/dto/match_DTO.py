from dataclasses import dataclass
from typing import Optional, TypedDict, Union, cast


class MatchScore(TypedDict):
    Player1: dict[str, Union[int, str]]
    Player2: dict[str, Union[int, str]]


@dataclass
class MatchDTO:
    uuid: str
    player1_id: int
    player2_id: int
    winner_id: Optional[int]
    score: Optional[MatchScore]

    def __init__(self, uuid: str,
                 player1_id: int,
                 player2_id: int,
                 winner_id: Optional[int] = None,
                 score: Optional[MatchScore] = None):
        """Класс шаблон DTO для выгрузки матча
        :@param player1_id: id игрока 1
        :@param player2_id: id игрока 2
        :@param winner_id: id игрока - победителя
        :@param score: счет игры
        """
        self.uuid = uuid
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.winner_id = winner_id
        self.score = cast(MatchScore, score or {"player1": {"set": 0, "game": 0, "points": 0},
                                                "player2": {"set": 0, "game": 0, "points": 0}})

    def to_dict(self) -> object:
        """Метод возвращает словарь с данными матча"""
        return self.__dict__

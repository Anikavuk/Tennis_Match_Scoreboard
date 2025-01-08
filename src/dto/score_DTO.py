from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class ScoreDTO:
    """Класс шаблон DTO для выгрузки счета"""

    player1: str
    player2: str
    winner: Optional[str]
    set1: int
    set2: int
    game1: int
    game2: int
    points1: Union[int, str]
    points2: Union[int, str]

    def __init__(self, player1: str, player2: str,
                 set1: int, set2: int,
                 game1: int, game2: int,
                 points1: Union[int, str],
                 points2: Union[int, str],
                 winner: Optional[str] = None,):
        """Класс шаблон DTO для выгрузки матча
        :@param player1 : имя игрока 1
        :@param player2 : имя игрока 2
        :@param winner : имя игрока - победителя
        :@param set1: set игрока 1
        :@param set2: set игрока 2
        :@param game1: game игрока 1
        :@param game2: game игрока 2
        :@param points1: points игрока 1
        :@param points2: points игрока 2
        """
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        self.set1 = set1
        self.set2 = set2
        self.game1 = game1
        self.game2 = game2
        self.points1 = points1
        self.points2 = points2


    def to_dict(self) -> object:
        """Метод возвращает словарь с данными счета"""
        return self.__dict__

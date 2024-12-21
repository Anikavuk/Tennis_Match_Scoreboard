from dataclasses import dataclass
from typing import Union


@dataclass
class ScoreDTO:
    """Класс шаблон DTO для выгрузки счета
    :@param player1 : имя игрока 1
    :@param player2 : имя игрока 2
    :@param set_1: set игрока 1
    :@param set_2: set игрока 2
    :@param game_1: game игрока 1
    :@param game_2: game игрока 2
    :@param points_1: points игрока 1
    :@param points_2: points игрока 2
    """
    player1: str
    player2: str
    set1: int
    set2: int
    game1: int
    game2: int
    points1: Union[int, str]
    points2: Union[int, str]

    def to_dict(self) -> object:
        """Метод возвращает словарь с данными счета"""
        return self.__dict__

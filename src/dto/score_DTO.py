from dataclasses import dataclass


@dataclass
class ScoreDTO:
    """Класс шаблон DTO для выгрузки счета
    :@param set_1: set игрока 1
    :@param set_2: set игрока 2
    :@param game_1: game игрока 1
    :@param game_2: game игрока 2
    :@param points_1: points игрока 1
    :@param points_2: points игрока 2
    """

    set_1: int
    set_2: int
    game_1: int
    game_2: int
    points_1: int
    points_2: int

    def to_dict(self) -> object:
        """Метод возвращает словарь с данными счета"""
        return self.__dict__

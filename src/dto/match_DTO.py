from dataclasses import dataclass


@dataclass
class MatchDTO:
    """Класс шаблон DTO для выгрузки матча
    :@param player1_id: id игрока 1
    :@param player2_id: id игрока 2
    :@param winner_id: id игрока - победителя
    :@param score: счет игры
    """
    player1_id: int
    player2_id: int
    winner_id: int
    score: dict

    def to_dict(self) -> object:
        """Метод возвращает словарь с данными матча"""
        return self.__dict__

from dataclasses import dataclass
from typing import Optional
import json


@dataclass
class MatchDTO:
    def __init__(self, uuid: str,  player1_id:int, player2_id:int, winner_id: Optional[int]=None,score: Optional[json]=None):
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
        self.score = score

    def to_dict(self) -> object:
        """Метод возвращает словарь с данными матча"""
        return self.__dict__

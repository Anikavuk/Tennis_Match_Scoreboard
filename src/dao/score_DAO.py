"""Написать методы работы с контроллером и со счетом игры"""
from src.service.service import Tennis_Score, Tiebreaker

class Score:
    def __init__(self, player1: int, player2: int):
        self.player1 =player1
        self.player2 = player2
        self.score_dict = {"Player1": {"set": 0, "game": 0, "points": 0}, "Player2": {"set": 0, "game": 0, "points": 0}}

    def current_score(self):
        """возращает счет"""
        return  self.score_dict

    def winner(self):
        """Возвращает победителя"""
        if self.score_dict['Player1']['set']==3:
            return list(self.score_dict.keys())[0]
        else:
            return list(self.score_dict.keys())[1]

    def check_and_update_set(self):
        """Метод проверяет разницу в 2 очка для game (а не set),
        и если разница составляет 2, увеличивало значение set у соответствующего игрока на 1
        либо если у игрока game достигает 6, тогда значение set у соответствующего игрока на 1"""
        if abs(self.score_dict['Player1']['game'] - self.score_dict['Player2']['game']) == 2:
            if self.score_dict['Player1']['game'] > self.score_dict['Player2']['game']:
                self.score_dict['Player1']['set'] += 1
            else:
                self.score_dict['Player2']['set'] += 1
        if self.score_dict['Player1']['game'] == 6 or self.score_dict['Player2']['game'] == 6:
            if self.score_dict['Player1']['game'] > self.score_dict['Player2']['game']:
                self.score_dict['Player1']['set'] += 1
            else:
                self.score_dict['Player2']['set'] += 1

    def check_tiebreaker_condition(self):
        """Если геймы у игроков равны 6, то Тай-брейк"""
        if self.score_dict['Player1']['game'] == 6 and self.score_dict['Player2']['game'] == 6:
            return Tiebreaker()


    def points(self):



p1 = Score(348, 349)
p1.score_dict = {"Player1": {"set": 3, "game": 0, "points": 0}, "Player2": {"set": 1, "game": 0, "points": 0}}



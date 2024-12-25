class Tennis_Score:
    def __init__(self, tie_break=False):
        self.tie_break = tie_break

    def counting_of_points(self, point=0):
        if self.tie_break:
            # Словарь для тай-брейка
            dict_points = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 0}
        else:
            # Обычный счет
            dict_points = {0: 15, 15: 30, 30: 40, 40: 'AD', 'AD': 0}

        return dict_points[point]


class Tiebreaker(Tennis_Score):
    def __init__(self):
        super().__init__(tie_break=True)

class ScoreCalculator:
    def __init__(self, player1: int, player2: int):
        self.player1 =player1
        self.player2 = player2
        self.score_dict = {"player1": {"set": 0, "game": 0, "points": 0}, "player2": {"set": 0, "game": 0, "points": 0}}

    # def current_score(self):
    #     """возращает счет"""
    #     return  self.score_dict

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


    def points(self, winner: str):
        '''игра продолжается до тех пор, пока один из игроков не получит два выигранных розыгрыша подряд после счета 40-40, чтобы выиграть гейм.'''
        if self.score_dict['Player1']['points'] == 40 and self.score_dict['Player2']['points'] == 40:
            player1_wins = 0
            player2_wins = 0

            while True:

                if winner == 'Player1':
                    player1_wins += 1
                    player2_wins = 0  # Сбросить счетчик выигрышей игрока 2
                elif winner == 'Player2':
                    player2_wins += 1
                    player1_wins = 0  # Сбросить счетчик выигрышей игрока 1

                # Проверка на выигрыш гейма
                if player1_wins == 2:
                    return self.update_games('Player1')
                elif player2_wins == 2:
                    return self.update_games('Player2')

    def update_games(self, player:str):
        if self.score_dict['player']['points'] == 'AD' or self.score_dict['player']['points'] == 7:
            self.score_dict['player']['game']+=1

        else: # это можно удалить
            other_player = 'Player1' if player == 'Player2' else 'Player2'# Если у игрока нет преимущества, то мы можем предположить, что другой игрок выигрывает гейм
            self.score_dict[other_player]['game'] += 1



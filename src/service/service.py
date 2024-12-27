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
    def __init__(self, score_dict):
        self.score_dict = score_dict
        # {"player1": {"set": 0, "game": 0, "points": 0}, "player2": {"set": 0, "game": 0, "points": 0}}

    def current_score(self):
        """возращает счет"""
        return  self.score_dict

    def winner(self, score_dict):
        """Возвращает победителя"""
        if score_dict['player1']['set']==3:
            return list(score_dict.keys())[0]
        elif score_dict['player2']['set'] == 3:
            return list(score_dict.keys())[1]

    def update_set(self, score_dict):
        player1_games = score_dict['player1']['game']
        player2_games = score_dict['player2']['game']

        if (player1_games >= 6 or player2_games >= 6) and abs(player1_games - player2_games) >= 2:
            if player1_games > player2_games:
                score_dict['player1']['set'] += 1
                score_dict['player1']['game'] = 0
                score_dict['player2']['game'] = 0
            else:
                score_dict['player2']['set'] += 1
                score_dict['player1']['game'] = 0
                score_dict['player2']['game'] = 0

    def check_tiebreaker_condition(self):
        """Если геймы у игроков равны 6, то Тай-брейк"""
        if self.score_dict['player1']['game'] == 6 and self.score_dict['player2']['game'] == 6:
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

    def update_games(self, score_dict):
        """Изменяет game у игроков"""
        player1_points = score_dict['player1']['points']
        player2_points = score_dict['player2']['points']
        if player1_points == 'AD' or player1_points == 7:
            score_dict['player1']['game'] += 1
            score_dict['player1']['points'] = 0
            score_dict['player2']['points'] = 0
        elif player2_points == 'AD' or player2_points == 7:
            score_dict['player2']['game'] += 1
            score_dict['player1']['points'] = 0
            score_dict['player2']['points'] = 0


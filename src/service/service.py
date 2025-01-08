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
        self.score_dict = score_dict  # {"player1": {"set": 0, "game": 0, "points": 0}, "player2": {"set": 0, "game": 0, "points": 0}}
        self.player1_wins = 0  # Счет выигранных очков player1
        self.player2_wins = 0  # Счет выигранных очков player2

    def current_score(self):
        """возращает счет"""
        return self.score_dict

    def check_the_winner(self, score_dict):
        """Возвращает победителя"""
        if score_dict['player1']['set'] == 3:
            return list(score_dict.keys())[0]
        elif score_dict['player2']['set'] == 3:
            return list(score_dict.keys())[1]

    def update_set(self, score_dict):
        """Изменяет set у игроков и обнуляет game у всех игроков"""
        player1_games = score_dict['player1']['game']
        player2_games = score_dict['player2']['game']

        if ((player1_games >= 6 or player2_games >= 6) and abs(player1_games - player2_games) >= 2) or (
                player1_games == 7 or player2_games == 7):
            if player1_games > player2_games:
                score_dict['player1']['set'] += 1
            else:
                score_dict['player2']['set'] += 1
            score_dict['player1']['game'] = 0
            score_dict['player2']['game'] = 0

    def check_tiebreaker_condition(self):
        """Функция возвращает True, если games у игроков равны 6,
            тогда наступает Тай-брейк"""
        return self.score_dict['player1']['game'] == 6 and self.score_dict['player2']['game'] == 6

    def update_games(self, score_dict):
        """Изменяет game у игроков и обнуляет points у всех игроков"""
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

    def check_deuce_condition(self):
        """Функция возвращает True, если points у игроков равны 40,
        тогда для победы игроку нужно взять два очка подряд """
        return self.score_dict['player1']['points'] == 40 and self.score_dict['player2']['points'] == 40

    def process_deuce_game(self, winner):
        """  """
        if winner == 'player1':
            self.player1_wins += 1
            self.player2_wins = 0  # Сброс счетчика для player2
        elif winner == 'player2':
            self.player2_wins += 1
            self.player1_wins = 0  # Сброс счетчика для player1

            # Проверка на выигрыш
        if self.player1_wins == 2:
            self.score_dict['player1']['game'] += 1
            self.score_dict['player1']['points'] = 0
            self.score_dict['player2']['points'] = 0
            self.player1_wins = 0  # Сброс счетчика
            self.player2_wins = 0  # Сброс счетчика
        elif self.player2_wins == 2:
            self.score_dict['player2']['game'] += 1
            self.score_dict['player1']['points'] = 0
            self.score_dict['player2']['points'] = 0
            self.player1_wins = 0  # Сброс счетчика
            self.player2_wins = 0  # Сброс счетчика

        return self.score_dict  # Возвращаем обновленный счет



#
winner = 'player2'
f = {"player1": {"set": 0, "game": 5, "points": 40}, "player2": {"set": 0, "game": 6, "points": 40}}
match = ScoreCalculator(f)
# Проверка условия дьюса и обработка выигрыша
if match.check_deuce_condition():
    f = match.process_deuce_game(winner)

print(f)
print(match.score_dict)
print('f = {"player1": {"set": 0, "game": 5, "points": 40}, "player2": {"set": 0, "game": 6, "points": 40}}')

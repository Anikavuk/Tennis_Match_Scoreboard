class Tennis_Score:
    def __init__(self, tie_break=False):
        self.tie_break = tie_break

    def counting_of_points(self, point=0):
        if self.tie_break:
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

    def check_the_winner(self, score_dict):
        """Возвращает победителя"""
        if score_dict['player1']['set'] == 3:
            return list(score_dict.keys())[0]
        elif score_dict['player2']['set'] == 3:
            return list(score_dict.keys())[1]

    def reset_the_games(self):
        self.score_dict['player1']['game'] = 0
        self.score_dict['player2']['game'] = 0

    def reset_the_points(self):
        self.score_dict['player1']['points'] = 0
        self.score_dict['player2']['points'] = 0

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
            self.reset_the_games()

    def check_tiebreaker_condition(self):
        """Функция возвращает True, если games у игроков равны 6,
            тогда наступает Тай-брейк"""
        return self.score_dict['player1']['game'] == 6 and self.score_dict['player2']['game'] == 6

    def update_games(self, score_dict, winner):
        """Изменяет game у игроков и обнуляет points у всех игроков"""
        # player1_points = score_dict['player1']['points']
        # player2_points = score_dict['player2']['points']
        # loser = 'player1' if winner == 'player2' else 'player2'
        if score_dict[winner]['points'] in ['AD', 7]:
            score_dict[winner]['game'] += 1
            self.reset_the_points()
        # if (player1_points == 'AD' and player2_points == 40) and winner == 'player1':
        #     score_dict['player1']['game'] += 1
        #     self.reset_the_points()
        # if (player1_points == 40 and player2_points == 'AD') and winner == 'player2':
        #     score_dict['player2']['game'] += 1
        #     self.reset_the_points()
        # elif score_dict[winner]['points'] == 40 and score_dict[loser]['points'] == 'AD':
        #     # Если противник был на AD, но проиграл, возвращаем счет к 40-40
        #     score_dict[winner]['points'] = 40
        #     score_dict[loser]['points'] = 40
        # elif score_dict[winner]['points'] == 40 and score_dict[loser]['points'] == 40:
        #     # Если оба на 40, то победитель получает AD
        #     score_dict[winner]['points'] = 'AD'
        #     score_dict[loser]['points'] = 40

    def check_deuce_condition(self):
        """Функция возвращает True, если points у игроков равны 40,
        тогда для победы игроку нужно взять два очка подряд """
        return self.score_dict['player1']['points'] == 40 and self.score_dict['player2']['points'] == 40

    def process_deuce_game(self, winner):
        player1_points = self.score_dict['player1']['points']
        player2_points = self.score_dict['player2']['points']
        if (player1_points == 'AD' and player2_points == 40) and winner == 'player2':
            self.score_dict['player1']['points'] = 40
            self.score_dict['player2']['points'] = 40
        elif (player1_points == 40 and player2_points == 'AD') and winner == 'player1':
            self.score_dict['player2']['points'] = 40
            self.score_dict['player1']['points'] = 40
        elif (player1_points == 40 and player2_points == 40) and winner == 'player1':
            self.score_dict['player1']['points'] = 'AD'
        elif (player1_points == 40 and player2_points == 40) and winner == 'player2':
            self.score_dict['player2']['points'] = 'AD'
        elif (player1_points == 40 and player2_points == 'AD') and winner == 'player2':
            self.update_games(self.score_dict, winner)
            self.reset_the_points()
        elif (player1_points == 'AD' and player2_points == 40 ) and winner == 'player1':
            self.update_games(self.score_dict, winner)
            self.reset_the_points()
        return self.score_dict

    def check_advantage_condition(self):
        # Проверка на Advantage (AD)
        return 'AD' in [self.score_dict['player1']['points'], self.score_dict['player2']['points']]

fff = ScoreCalculator({'player1': {'set': 3, 'game': 0, 'points': 40}, 'player2': {'set': 0, 'game': 0, 'points': 30}})
print(fff.check_the_winner({'player1': {'set': 3, 'game': 0, 'points': 40}, 'player2': {'set': 0, 'game': 0, 'points': 30}}))
# if fff.check_advantage_condition():
#     print(fff.check_advantage_condition())
#     print(fff.process_deuce_game(winner))
# fff.
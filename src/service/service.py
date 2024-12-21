
#     # def __init__(self, player1, player2, points1, points2, games1, games2, set1, set2):
#     #     self.score = {'match_data':
#     #                       {player1: {'set': set1, 'games': games1, 'points': points1},
#     #                        player2: {'set': set2, 'games': games2, 'points': points2}}
#     #                   }


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

    @staticmethod
    def increment_counter(value):
        value += 1
        return value



class Tiebreaker(Tennis_Score):
    def __init__(self):
        super().__init__(tie_break=True)

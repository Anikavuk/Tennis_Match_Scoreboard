from typing import Dict, Union


class Tennis_Score:
    def __init__(self, tie_break=False):
        self.tie_break = tie_break

    def _counting_of_points(self, point: Union[int, str] = 0) -> Union[int, str]:
        """Функция для подсчета очков в зависимости от режима игры.

            В случае тай-брейка используется специальный режим счета,
            где очки начисляются последовательно от 1 до 7, а затем возвращаются к 0.
            В обычном режиме используются стандартные значения теннисного счета:
            0, 15, 30, 40 и 'AD' (преимущество).

            :param `point: Union[int, str]`: Текущее количество очков игрока. По умолчанию равно 0.

            :return:  Union[int, str]: Новое значение очков после увеличения.
        """
        # Объявляем dict_points с общим типом Dict[Union[int, str], Union[int, str]]
        dict_points: Dict[Union[int, str], Union[int, str]]
        if self.tie_break:
            dict_points = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 0}
        else:
            # Обычный счет
            dict_points = {0: 15, 15: 30, 30: 40, 40: 'AD', 'AD': 0}

        return dict_points[point]


class Tiebreaker(Tennis_Score):
    def __init__(self):
        super().__init__(tie_break=True)


class Score_Calculator:
    """ Класс для расчета и отслеживания счета в спортивном матче.
        Класс хранит текущий счет двух игроков, включая количество сетов, геймов и очков.

        :param `score_dict`: Словарь, содержащий информацию о счете каждого игрока.
          Структура словаря следующая:
          {
              "player1": {"set": 0, "game": 0, "points": 0},
              "player2": {"set": 0, "game": 0, "points": 0}
          }
    """

    def __init__(self, score_dict: Dict) -> None:
        self.score_dict = score_dict

    def check_the_winner(self, score_dict: dict) -> Union[str, None]:
        """Проверяет счет и возвращает имя победителя.
        Функция проверяет количество выигранных сетов у каждого игрока.
        Если один из игроков выиграл три сета, он объявляется победителем.

        :param`score_dict`: Словарь, содержащий информацию о текущем счете.
              Структура словаря следующая:
              {
                  "player1": {"set": 0, "game": 0, "points": 0},
                  "player2": {"set": 0, "game": 0, "points": 0}
              }

        :return
            - str: Имя победителя ('player1' или 'player2') при наличии такового.
            - None: Если ни один игрок еще не выиграл три сета.
        """
        if score_dict['player1']['set'] == 3:
            return list(score_dict.keys())[0]
        elif score_dict['player2']['set'] == 3:
            return list(score_dict.keys())[1]
        return None

    def reset_the_games(self):
        """Этот метод обнуляет значение ключа 'game' для каждого игрока в словаре score_dict.
        После вызова этого метода оба игрока будут иметь счет игры равный нулю."""
        self.score_dict['player1']['game'] = 0
        self.score_dict['player2']['game'] = 0

    def reset_the_points(self) -> None:
        """Этот метод обнуляет значение ключа 'points' для каждого игрока в словаре score_dict.
        После вызова этого метода оба игрока будут иметь счет игры равный нулю."""
        self.score_dict['player1']['points'] = 0
        self.score_dict['player2']['points'] = 0

    def update_set(self, score_dict: Dict[str, Dict[str, int]]) -> None:
        """
        Обновляет счёт сетов у игроков и сбрасывает счёт геймов.
        Эта функция проверяет условия завершения сета
        и обновляет счёт сета у соответствующего игрока,
        а затем сбрасывает счёт геймов до нуля для обоих игроков.

        Параметры:
        :param score_dict (dict): Словарь, содержащий текущий счёт игры для двух игроков.
        :return: None
        Условия завершения сета:
        - Один из игроков выиграл минимум 6 геймов, и разница в счёте составляет не менее 2 гейма.
        - Один из игроков выиграл 7 геймов.
        """
        player1_games = score_dict['player1']['game']
        player2_games = score_dict['player2']['game']

        if ((player1_games >= 6 or player2_games >= 6) and
            abs(player1_games - player2_games) >= 2) or (
                player1_games == 7 or player2_games == 7) :
            if player1_games > player2_games:
                score_dict['player1']['set'] += 1
            else:
                score_dict['player2']['set'] += 1
            self.reset_the_games()

    def is_tiebreaker_condition_met(self) -> bool:
        """
        Проверяет, наступает ли тай-брейк в матче.
        Тай-брейк наступает, когда количество игр у обоих игроков равно 6.
        Returns: bool: True, если оба игрока имеют по 6 игр, иначе False.
        """
        return self.score_dict['player1']['game'] == 6 and self.score_dict['player2']['game'] == 6

    def update_games(self, score_dict: Dict[str, Dict[str, int]], winner: str) -> None:
        """
        Обновляет счёт геймов у победителя и сбрасывает очки у обоих игроков.

        Эта функция проверяет, достиг ли победитель определённого количества очков ('AD' или 7),
        и если да, то увеличивает счёт геймов у данного игрока и сбрасывает очки у обоих игроков.

        :param score_dict: Словарь, содержащий текущий счёт игры для двух игроков.
        :param winner: Имя победителя гейма (либо 'player1', либо 'player2').
        :return: None
        """
        if score_dict[winner]['points'] in ['AD', 7]:
            score_dict[winner]['game'] += 1
            self.reset_the_points()

    def is_deuce_condition_met(self):
        """
        Проверяет, наступило ли состояние деуса (deuce) в матче.
        Деус наступает, когда количество очков у обоих игроков равно 40.
        Returns:
            bool: True, если оба игрока имеют по 40 очков, иначе False.
        """
        return self.score_dict['player1']['points'] == 40 and self.score_dict['player2']['points'] == 40

    def process_deuce_game(self, winner: str) -> Dict[str, Dict[str, Union[int, str]]]:
        """
        Обрабатывает ситуацию при равенстве очков в points и возвращает обновлённый счёт.

        В зависимости от текущей ситуации (счёт 'AD' или 40), функция определяет дальнейшие действия:
        - Возвращение к состоянию 40-40, если проигравший получил очко.
        - Увеличение счёта геймов у победившего игрока, если он выигрывает гейм.

        :param winner: str Имя победителя розыгрыша очка (либо 'player1', либо 'player2').
        :return: Обновлённый словарь счёта игры.
        """
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
        elif (player1_points == 'AD' and player2_points == 40) and winner == 'player1':
            self.update_games(self.score_dict, winner)
            self.reset_the_points()
        return self.score_dict

    def is_there_an_advantage(self) -> bool:
        """
        Проверяет, есть ли у одного из игроков преимущество (Advantage).
        Функция проверяет, есть ли в текущем счёте у одного из игроков состояние 'AD' (Advantage).
        :return: True, если хотя бы у одного из игроков есть преимущество, иначе False.
        """
        return 'AD' in [self.score_dict['player1']['points'], self.score_dict['player2']['points']]

class MatchDTO:
    """Класс шаблон DTO для единного вида выгрузки матча
    :@param player1_id: id игрока 1
    :@param player2_id: id игрока 2
    :@param winner_id: id игрока - победителя
    :@param score: счет игры
   """

    def __init__(self, player1, player2, winner, score):
        self.player1_id = player1
        self.player2_id = player2
        self.winner_id = winner
        self.score = score

    def to_dict(self) -> object:
        """Метод возвращает словарь с данными матча"""
        return self.__dict__
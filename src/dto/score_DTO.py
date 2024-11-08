class ScoreDTO:
    """Класс шаблон DTO для единного вида выгрузки счета
        :@param set_1: set игрока 1
        :@param set_2: set игрока 2
        :@param game_1: game игрока 1
        :@param game_2: game игрока 2
        :@param points_1: points игрока 1
        :@param points_2: points игрока 2
        """

    def __init__(self, set_1, set_2, game_1, game_2 ,points_1, points_2):

        self.set_1 = set_1
        self.set_2 = set_2
        self.game_1 = game_1
        self.game_2 = game_2
        self.points_1 = points_1
        self.points_2 = points_2

    def to_dict(self) -> object:
        """Метод возвращает словарь с данными счета"""
        return self.__dict__

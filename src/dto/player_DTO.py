class PlayerDTO:
    """Класс шаблон DTO для единного вида выгрузки игрока"""

    def __init__(self,name, id=None):
        """ 
        :@param id: id игрока
        @param name: имя игрока
        """
        self.id = id
        self.name = name

    def to_dict(self) -> object:
        """Метод возвращает словарь с данными игрока"""
        return self.__dict__

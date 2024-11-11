from dataclasses import dataclass


@dataclass
class PlayerDTO:
    """Класс шаблон DTO для выгрузки игрока
    :@param id: id игрока
    :@param name: имя игрока
    """
    id: int
    name: str

    def to_dict(self) -> object:
        """Метод возвращает словарь с данными игрока"""
        return self.__dict__

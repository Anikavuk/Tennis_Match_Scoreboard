from typing import List, Tuple, Union, Optional

from sqlalchemy.exc import IntegrityError, OperationalError

from src.db.database import engine, Session
from src.db.models import Player
from src.errors import BaseAPIException, DatabaseErrorException, PlayerNotFoundException


class PlayerDAO:
    """Класс для работы с таблицей players"""

    def __init__(self, name):
        self.name = name

    @staticmethod
    def _save_player(players_name: str) -> Union[ int, BaseAPIException]:
        """Сохранение имени игрока в базе данных.
        :param players_name: str Имя игрока
        :return player1.id: int Уникальный идентификатор игрока
        Raises: IntegrityError Если произошла ошибка при сохранении к базе данных,
        значит что имя уже есть в бд и выдает id игрока."""
        try:
            with Session(autoflush=False, bind=engine) as db:
                new_player = Player(name=players_name)
                db.add(new_player)
                db.commit()
                return new_player.id
        except IntegrityError:
            with Session(autoflush=False, bind=engine) as db:
                existing_player: Optional[Player] = db.query(Player).filter(Player.name == players_name).first()
                if existing_player is None:
                    return BaseAPIException.error_response(
                        exception=PlayerNotFoundException())
                db.commit()
                return existing_player.id

    def _get_all_players(self) -> Union[List[Tuple[int, str]], BaseAPIException]:
        """Выгружает всех игроков из базы данных.

        Этот метод выполняет запрос к базе данных для получения
        списка всех игроков. Каждый игрок представляется кортежем,
        содержащим его идентификатор и имя.

        Returns:
            List[Tuple[int, str]]:
                Список кортежей, где каждый кортеж состоит из
                идентификатора игрока и его имени, если операция прошла успешно.

            BaseAPIException:
                Возвращается объект исключения, если возникает
                ошибка при выполнении запроса к базе данных.

        Raises:
            OperationalError:
                Если возникает ошибка при попытке доступа к
                базе данных, будет выброшено это исключение.
        """
        try:
            with Session(autoflush=False, bind=engine) as db:
                players = db.query(Player).all()
                all_players = [(player.id, player.name) for player in players]
                return all_players

        except OperationalError:
            return BaseAPIException.error_response(exception=DatabaseErrorException())

    @staticmethod
    def is_valid_username(name: str) -> bool:
        """Проверка на валидацию введенного имени.

        Этот метод проверяет, является ли введенное имя пользователя
        допустимым на основании заданных критериев.

        :param name: Имя пользователя, которое необходимо проверить.
        :type name: str
        :return: True, если имя пользователя соответствует критериям
                 валидации (латинские буквы верхнего и нижнего регистра,
                 кириллические буквы и пробелы), иначе False.
        :rtype: bool
        """
        for letter in name:
            if not ((65 <= ord(letter) <= 90) or
                    (97 <= ord(letter) <= 122) or
                    (1040 <= ord(letter) <= 1103) or (ord(letter) == 32)):
                return False
        return True

    @staticmethod
    def check_name_length(name):
        return len(name) <= 30
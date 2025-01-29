from sqlalchemy.exc import IntegrityError, OperationalError

from src.db_models.database import engine, Session
from src.db_models.models import Player
from src.errors import BaseAPIException, DatabaseErrorException


class PlayerDAO:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def save_player(players_name: str):
        """Сохранение имени игрока в базе данных"""
        try:
            with Session(autoflush=False, bind=engine) as db:
                player = Player(name=players_name)
                db.add(player)
                db.commit()
                return player.id
        except IntegrityError:
            with Session(autoflush=False, bind=engine) as db:
                player = db.query(Player).filter(Player.name == players_name).first()
                db.commit()
                return player.id

    def get_all_players(self):
        """ Выгрузка всех игроков"""
        try:
            with Session(autoflush=False, bind=engine) as db:
                players = db.query(Player).all()
                all_players = [(player.id, player.name) for player in players]
                return all_players

        except OperationalError:
            return BaseAPIException.error_response(exception=DatabaseErrorException())
    @staticmethod
    def is_valid_username(name: str):
        """Проверка на валидацию введенного имени"""
        for letter in name:
            if not ((65 <= ord(letter) <= 90) or
                    (97 <= ord(letter) <= 122) or
                    (1040 <= ord(letter) <= 1103) or (ord(letter) == 32)):
                return False
        return True

# dddd = PlayerDAO('ААА')
# print(dddd.save_player('ААА'))

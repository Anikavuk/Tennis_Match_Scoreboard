from sqlalchemy.exc import IntegrityError, OperationalError

from src.db_models.database import engine, Session
from src.db_models.models import Player
from src.errors import ErrorResponse, DatabaseErrorException


class PlayerDAO:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def save_player(players_name):
        try:
            with Session(autoflush=False, bind=engine) as db:
                player = Player(name=players_name)
                db.add(player)
                db.commit()
            return True
        except IntegrityError:
            db.rollback()
            return False

    def get_all_players(self):
        """ Выгрузка всех игроков"""
        try:
            with Session(autoflush=False, bind=engine) as db:
                players = db.query(Player).all()
                all_players = [(player.id, player.name) for player in players]
                return all_players

        except OperationalError:
            return ErrorResponse.error_response(exception=DatabaseErrorException())
    @staticmethod
    def is_valid_username(name):
        """Проверка на валидацию введенного имени"""
        for letter in name:
            if not ((65 <= ord(letter) <= 90) or
                    (97 <= ord(letter) <= 122) or
                    (1040 <= ord(letter) <= 1103)):
                return False
        return True
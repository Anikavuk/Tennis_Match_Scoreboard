from sqlalchemy.exc import IntegrityError, OperationalError

from src.db_models.database import engine, Session
from src.db_models.models import Player
from src.errors import ErrorResponse, DatabaseErrorException


class PlayerDAO:
    def __init__(self, name):
        self.name = name

    def save_player(self):
        try:
            with Session(autoflush=False, bind=engine) as db:
                player = Player(name=self.name)
                db.add(player)
                db.commit()
        except IntegrityError:
            # print('You need to enter a different, unique nameone')
            # db.rollback()
            # здесь нужна ошибка дубликата имени, если в базе данных есть имя , то не сохранять
            return ErrorResponse.error_response(exception=IntegrityError())

    def get_all_players(self):
        try:
            with Session(autoflush=False, bind=engine) as db:
                players = db.query(Player).all()
                all_players = [(player.id, player.name) for player in players]
                return all_players

        except OperationalError:
            # Алсу!Проверить ошибку недоступности базы данных в sqlalchemy!!!
            # то исключение OperationalError выбрала или не то
            return ErrorResponse.error_response(exception=DatabaseErrorException())

    def is_valid_username(self):
        for letter in self.name:
            if not ((65 <= ord(letter) <= 90) or
                    (97 <= ord(letter) <= 122) or
                    (1040 <= ord(letter) <= 1103)):
                return False
        return True

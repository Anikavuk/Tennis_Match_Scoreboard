from database import engine, Session
from errors import ErrorResponse, IntegrityError, DatabaseErrorException
from models import PlayersOrm, MatchesOrm
from sqlalchemy.exc import OperationalError


class PlayerManager:
    def __init__(self, name):
        self.name = name

    def save_player(self):
        try:
            with Session(autoflush=False, bind=engine) as db:
                player = PlayersOrm(name=self.name)
                db.add(player)
                db.commit()
        except IntegrityError:
            return ErrorResponse.error_response(exception=IntegrityError())

    def get_all_players(self):
        try:
            with Session(autoflush=False, bind=engine) as db:
                players = db.query(PlayersOrm).all()
                all_players = [(player.id, player.name) for player in players]
                return all_players

        except OperationalError:
            #Алсу!Проверить ошибку недоступности базы данных в sqlalchemy!!!
            # то исключение OperationalError выбрала или не то
            return ErrorResponse.error_response(exception=DatabaseErrorException())

    class MatchManager:
        def __init__(self, player1, player2, winner, score):
            self.player1 = player1
            self.player1 = player2
            self.winner = winner
            self.score = score

        def save_matches(self):
            try:
                with Session(autoflush=False, bind=engine) as db:
                    match = MatchesOrm()
                    db.add(match)
                    db.commit()
            except IntegrityError:
                return ErrorResponse.error_response(exception=IntegrityError())

        def get_all_matches(self):
            try:
                with Session(autoflush=False, bind=engine) as db:
                    matches = db.query(MatchesOrm).all()
                    all_matches = [(match.id,
                                    match.player1,
                                    match.player2,
                                    match.winner,
                                    match.score)
                                   for match in matches]
                    return all_matches

            except OperationalError:
                # Алсу!Проверить ошибку недоступности базы данных в sqlalchemy!!!
                # то исключение OperationalError выбрала или не то
                return ErrorResponse.error_response(exception=DatabaseErrorException())
    def is_player_name_in_database(self, player_name):
        """Проверка имени в базе данных, нужна эта функция или нет"""
        with Session(autoflush=False, bind=engine) as db:
            first = db.query(PlayersOrm).filter(PlayersOrm.name == player_name)
            pass
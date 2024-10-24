from sqlalchemy.exc import IntegrityError, OperationalError
from database import engine, Session
from errors import ErrorResponse, DatabaseErrorException
from models import Player, Match


class PlayerManager:
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


class MatchManager:
    def __init__(self, player1, player2, winner, score):
        self.player1_id = player1
        self.player2_id = player2
        self.winner_id = winner
        self.score = score

    def save_match(self):
        try:
            with Session(autoflush=False, bind=engine) as db:
                match = Match(player1_id = self.player1_id,
                              player2_id = self.player2_id,
                              winner_id = self.winner_id,
                              score = self.score)
                db.add(match)
                db.commit()
        except IntegrityError:
            return ErrorResponse.error_response(exception=IntegrityError())

    def get_all_matches(self):
        try:

            with (Session(autoflush=False, bind=engine) as bd):
                matches_query = bd.query(Match)
                results = matches_query.all()

                # Форматируем результаты для удобства
                matches = []
                for match in results:
                    matches.append({
                        'match_id': match.id,
                        'player1': match.player1.name,
                        'player2': match.player2.name,
                        'winner': match.winner.name,
                        'score': match.score
                    })

                return matches
        except OperationalError:
            # Алсу!Проверить ошибку недоступности базы данных в sqlalchemy!!!
            # то исключение OperationalError выбрала или не то
            return ErrorResponse.error_response(exception=DatabaseErrorException())

    def list_player_matches(self, player_name):
        try:
            with Session(autoflush=False, bind=engine) as db:
                matches = db.query(Match).filter((Match.player1.has(name=player_name)) | (Match.player2.has(name=player_name))).all()
                all_matches = [{'match_id': match.id,
                                'player1': match.player1.name,
                                'player2': match.player2.name,
                                'winner': match.winner.name,
                                'score': match.score}
                               for match in matches]
                return all_matches
        except OperationalError:
            # Алсу!Проверить ошибку недоступности базы данных в sqlalchemy!!!
            # то исключение OperationalError выбрала или не то
            return ErrorResponse.error_response(exception=DatabaseErrorException())

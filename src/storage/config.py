from sqlalchemy.orm import joinedload, aliased

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
        self.player2 = player2
        self.winner = winner
        self.score = score


    def save_matches(self):
        try:
            with Session(autoflush=False, bind=engine) as db:
                match = MatchesOrm(player1=self.player1,
                                   player2=self.player2,
                                   winner=self.winner,
                                   score=self.score)
                db.add(match)
                db.commit()
        except IntegrityError:
            return ErrorResponse.error_response(exception=IntegrityError())

    def get_all_matches(self):
        # try:

        with (Session(autoflush=False, bind=engine) as bd):
            matches_query = bd.query(MatchesOrm.id,
                                     MatchesOrm.score,
                                     PlayersOrm.name.label('player1'),
                                     PlayersOrm.name.label('player2'),
                                     PlayersOrm.name.label('winner')
                                     ).join(PlayersOrm, MatchesOrm.player1 == PlayersOrm.id
                                            ).join(PlayersOrm, MatchesOrm.player2 == PlayersOrm.id
                                                   ).join(PlayersOrm, MatchesOrm.winner == PlayersOrm.id)
            results = matches_query.all()

            # Форматируем результаты для удобства
            matches = []
            for match in results:
                matches.append({
                    'match_id': match.id,
                    'player1': match.player1_relation.name,
                    'player2': match.player2_relation.name,
                    'winner': match.winner_relation.name,
                    'score': match.score
                })

            return results
        # except OperationalError:
        #     # Алсу!Проверить ошибку недоступности базы данных в sqlalchemy!!!
        #     # то исключение OperationalError выбрала или не то
        #     return ErrorResponse.error_response(exception=DatabaseErrorException())

    def list_player_matches(self, player_name):
        try:
            with Session(autoflush=False, bind=engine) as db:
                matches = db.query(MatchesOrm).filter(self.name==player_name).all()
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


# def is_player_name_in_database(self, player_name):
#     """Проверка имени в базе данных, нужна эта функция или нет надо решить"""
#     with Session(autoflush=False, bind=engine) as db:
#         first = db.query(PlayersOrm).filter(PlayersOrm.name == player_name)
#         pass


ff = PlayerManager('Дэн') # [(5, 'Даша'), (1, 'Денис'), (7, 'Дима'), (8, 'Дэн'), (2, 'Женя'), (4, 'Максим'), (3, 'Оля'), (6, 'Юра')]
# print(ff.save_player())
# print(ff.get_all_players())
mm = MatchManager(7, 1, 7, 3)
# mm.save_matches()
print(mm.get_all_matches())
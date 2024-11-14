from sqlalchemy.exc import IntegrityError, OperationalError
from src.db_models.database import engine, Session
from src.db_models.models import Match
from src.errors import ErrorResponse, DatabaseErrorException


class MatchDAO:

    @staticmethod
    def save_match(player1_id, player2_id):
        try:
            # сохранение матча
            with Session(autoflush=False, bind=engine) as db:
                match = Match(player1_id=player1_id,
                              player2_id=player2_id, winner_id=None)
                db.add(match)
                db.commit()
            return True
        except IntegrityError:
            db.rollback()
            return False

    def get_all_matches(self):
        try:
            # выгружает все матчи
            with (Session(autoflush=False, bind=engine) as bd):
                matches_query = bd.query(Match)
                results = matches_query.all()

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
                matches = db.query(Match).filter(
                    (Match.player1.has(name=player_name)) | (Match.player2.has(name=player_name))).all()
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



fff = MatchDAO()
fff.save_match(164, 161)
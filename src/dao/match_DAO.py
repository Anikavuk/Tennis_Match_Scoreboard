from src.db_models.database import engine, Session
from src.db_models.models import Match


class MatchDAO:

    @staticmethod
    def save_current_match(player1_id, player2_id):
        """сохранение текущего матча"""
        with Session(autoflush=False, bind=engine) as db:
            match = Match(player1_id=player1_id, player2_id=player2_id)
            db.add(match)
            db.commit()
            return True

    @staticmethod
    def update_match(uuid, winner, score):
        """изменение сохраненного матча"""
        with Session(autoflush=False, bind=engine) as db:
            match =db.query(Match).filter(Match.uuid==uuid).first()
            match.winner_id=winner
            match.score = score
            db.commit()
            return True


    def get_all_matches(self):
        """выгрузка всех матчей"""
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

    def list_player_matches(self, player_name):
        """выгрузка всех матчей с определенным игроком"""
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


fff = MatchDAO()
fff.update_match('06b10163-c9ab-4cd4-9d1d-62b704a44b4b', 159, {2:2})
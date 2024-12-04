from pydantic import json

from src.db_models.database import engine, Session
from src.db_models.models import Match


class MatchDAO:

    @staticmethod
    def save_current_match(player1_id: int, player2_id: int):
        """Сохранение текущего матча"""
        with Session(autoflush=False, bind=engine) as db:
            match = Match(player1_id=player1_id, player2_id=player2_id)
            db.add(match)
            db.commit()
            return match.uuid

    @staticmethod
    def update_match(uuid: str, winner: int, score: json):
        """Изменение сохраненного матча"""
        with Session(autoflush=False, bind=engine) as db:
            match = db.query(Match).filter(Match.uuid == uuid).first()
            match.winner_id = winner
            match.score = score
            db.commit()
            return True

    def get_all_matches(self):
        """Выгрузка всех матчей"""
        with (Session(autoflush=False, bind=engine) as bd):
            matches_query = bd.query(Match)
            results = matches_query.all()

            matches = []
            for match in results:
                matches.append({'player1': match.player1.name,
                                'player2': match.player2.name,
                                'winner': match.winner.name if match.winner else None
                })

            return matches

    def list_player_matches(self, player_name: str):
        """выгрузка всех матчей с определенным игроком"""
        with Session(autoflush=False, bind=engine) as db:
            matches = db.query(Match).filter(
                (Match.player1.has(name=player_name)) | (Match.player2.has(name=player_name))).all()
            all_matches = [{'player1': match.player1.name,
                            'player2': match.player2.name,
                            'winner': match.winner.name if match.winner else None}
                           for match in matches]
            return all_matches

    def get_match_by_uuid_with_names(self, uuid: str):
        """выгрузка имен игроков по uuid матча"""
        with Session(autoflush=False, bind=engine) as db:
            matches = db.query(Match).filter(Match.uuid == uuid).first()
            list_of_players = {matches.player1.id:matches.player1.name, matches.player2.id:matches.player2.name}
            return list_of_players

from pydantic import json
import json
from src.db_models.database import engine, Session
from src.db_models.models import Match


class MatchDAO:

    @staticmethod
    def save_current_match(player1_id: int, player2_id: int):
        """Сохранение текущего матча"""
        with Session(autoflush=False, bind=engine) as db:
            match = Match(player1_id=player1_id,
                          player2_id=player2_id,
                          score={"match_data":
                                     {"player1": {"set": 0, "game": 0, "points": 0},
                                      "player2": {"set": 0, "game": 0, "points": 0}}})
            db.add(match)
            db.commit()
            return match.uuid

    def update_match(self, uuid: str, score_update: json):
        """Изменение сохраненного матча"""
        with Session(autoflush=False, bind=engine) as db:
            match = db.query(Match).filter(Match.uuid == uuid).first()
            match.score = score_update
            db.commit()
            return match
    def update_winner(self, uuid: str, winner: int):
        """Добавление победителя в бд"""
        with Session(autoflush=False, bind=engine) as db:
            match = db.query(Match).filter(Match.uuid == uuid).first()
            match.winner = winner
            db.commit()
            return match

    def get_all_matches(self):
        """Выгрузка всех матчей"""
        with (Session(autoflush=False, bind=engine) as bd):
            matches_query = bd.query(Match)
            results = matches_query.all()

            matches = []
            for match in results:
                matches.append({'player1': match.player1.name,
                                'player2': match.player2.name,
                                'winner': match.check_the_winner.name if match.check_the_winner else None
                })

            return matches

    def list_player_matches(self, player_name: str):
        """выгрузка всех матчей с определенным игроком"""
        with Session(autoflush=False, bind=engine) as db:
            matches = db.query(Match).filter(
                (Match.player1.has(name=player_name)) | (Match.player2.has(name=player_name))).all()
            all_matches = [{'player1': match.player1.name,
                            'player2': match.player2.name,
                            'winner': match.check_the_winner.name if match.check_the_winner else None}
                           for match in matches]
            return all_matches

    def get_match_info_by_uuid(self, uuid: str):
        """выгрузка текущего матча по uuid"""
        with Session(autoflush=False, bind=engine) as db:
            match = db.query(Match).filter(Match.uuid == uuid).first()
            result_dict = {
                'player1': match.player1.name,
                'player2': match.player2.name,
                'set1': match.score['match_data']['player1']['set'],
                'game1': match.score['match_data']['player1']['game'],
                'points1': match.score['match_data']['player1']['points'],
                'set2': match.score['match_data']['player2']['set'],
                'game2': match.score['match_data']['player2']['game'],
                'points2': match.score['match_data']['player2']['points']
            }
            return result_dict
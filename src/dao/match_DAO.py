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
                                     {"Player1": {"set": 0, "game": 0, "points": 0},
                                      "Player2": {"set": 0, "game": 0, "points": 0}}})
            db.add(match)
            db.commit()
            return match.uuid

    def update_match(self, uuid: str, score_update: json):
        """Изменение сохраненного матча"""
        with Session(autoflush=False, bind=engine) as db:
            match = db.query(Match).filter(Match.uuid == uuid).first()
            # if match:
            #     # Извлечь текущий score
            #     current_score = json.dumps(match.score)
            #
            #     # Обновить только указанные поля
            #     if 'Player1' in score_update and 'points' in score_update['Player1']:
            #         current_score['match_data']['Player1']['points'] = score_update['Player1']['points']
            #     # аналогично для других полей:  'Player1.set', 'Player1.game', 'Player2.points', и т.д.
            #
            #     match.score = json.loads(current_score)  # Преобразовать обратно в JSON строку
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

    def get_match_info_by_uuid(self, uuid: str):
        """выгрузка текущего матча по uuid"""
        with Session(autoflush=False, bind=engine) as db:
            match = db.query(Match).filter(Match.uuid == uuid).first()
            result_dict = {
                'player1': match.player1.name,
                'player2': match.player2.name,
                'set1': match.score['match_data']['Player1']['set'],
                'game1': match.score['match_data']['Player1']['game'],
                'points1': match.score['match_data']['Player1']['points'],
                'set2': match.score['match_data']['Player2']['set'],
                'game2': match.score['match_data']['Player2']['game'],
                'points2': match.score['match_data']['Player2']['points']
            }
            return result_dict

# ЗДЕСЬ НЕ ДОРАБОТАН МЕТОД АПДЕЙТ МАТЧА
# ddd = MatchDAO()
# print(ddd.update_match('2671e3d0-e998-4929-b3dc-a966c2fca1d0',  {'Player1': {'points': 15}} ))
# score_update = {'Player1': {'points': 15}}
# score_update2 = json.dumps(score_update)
# print(type(score_update2))
# print(score_update2)
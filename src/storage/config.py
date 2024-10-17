from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from database import engine, Session
from models import PlayersOrm, MatchesOrm
from sqlalchemy import text, select

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
            # return ErrorResponse.error_response(exception=DatabaseErrorException())
            pass
    def get_all_players(self):
        try:
            with Session(autoflush=False, bind=engine) as db:
                players = db.query(PlayersOrm).all()
                for player in players:
                    return f"{player.id} {player.name}"
        except:
            print('Придумать ошибку.. какую ошибку при выгрузке всех игроков придумать?')

    # def is_player_name_in_database(self, player_name):
    #     try:
    #         with Session(autoflush=False, bind=engine) as db:
    #             first = db.query(PlayersOrm).filter(PlayersOrm.name == player_name)

ff = PlayerManager('Максим')
ff.save_player()

#
# # здесь создать таблицы, методы внести новые данные , удалить, пр.
#
# def select_players_relationships():
#     with Session(autoflush=False, bind=engine) as db:
#         players = db.query(PlayersOrm).all()
#         for player in players:
#             print(f"{player.id} {player.name}")
# with Session(autoflush=False, bind=engine) as db:
#     tom = PlayersOrm(name="Оля")
#     db.add(tom)
#     db.commit()
# with Session(autoflush=False, bind=engine) as db:
#     tom = MatchesOrm(player1=5, player2=9, winner=9, score=3)
#     g = MatchesOrm(player1=8, player2=5, winner=5, score=3)
#     db.add(tom)
#     db.commit()

# with Session(autoflush=False, bind=engine) as db:
#     res = db.execute(text('SELECT VERSION()'))
#     print(f"{res.first()=}")
#
# select_players_relationships()
# def select_MatchesOrm_relationships():
#     with Session(autoflush=False, bind=engine) as db:
#         players = db.query(MatchesOrm).all()
#         for player in players:
#             print(f"{player.id} {player.uuid} {player.player1} {player.player2} {player.winner} {player.score}")
#
# select_MatchesOrm_relationships()
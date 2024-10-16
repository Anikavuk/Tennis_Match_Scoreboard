from sqlalchemy.orm import sessionmaker
from database import engine, Session
from models import PlayersOrm, MatchesOrm
from sqlalchemy import text, select

# здесь создать таблицы, методы внести новые данные , удалить, пр.

def select_players_relationships():
    with Session(autoflush=False, bind=engine) as db:
        players = db.query(PlayersOrm).all()
        for player in players:
            print(f"{player.id} {player.name}")

# with Session(autoflush=False, bind=engine) as db:
#     tom = MatchesOrm(player1=5, player2=4, winner=5, score=1)
#     db.add(tom)
#     db.commit()

# with Session(autoflush=False, bind=engine) as db:
#     res = db.execute(text('SELECT VERSION()'))
#     print(f"{res.first()=}")

select_players_relationships()
def select_MatchesOrm_relationships():
    with Session(autoflush=False, bind=engine) as db:
        players = db.query(MatchesOrm).all()
        for player in players:
            print(f"{player.id} {player.uuid} {player.player1} {player.player2} {player.winner} {player.score}")

select_MatchesOrm_relationships()
from sqlalchemy.orm import sessionmaker
from database import engine, Session
from models import PlayersOrm, MatchesOrm
from sqlalchemy import text

# здесь создать таблицы, методы внести новые данные , удалить, пр.

# with Session(autoflush=False, bind=engine) as db:
#     tom = PlayersOrm(name="Tom")
#     db.add(tom)
#     db.commit()

# with Session(autoflush=False, bind=engine) as db:
#     tom = MatchesOrm(player1=5, player2=4, winner=5, score=1)
#     db.add(tom)
#     db.commit()

with Session(autoflush=False, bind=engine) as db:
    res = db.execute(text('SELECT VERSION()'))
    print(f"{res.first()=}")
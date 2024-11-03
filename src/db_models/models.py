import uuid

from sqlalchemy import ForeignKey, VARCHAR, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import CHAR


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__: str = 'players'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(length=30), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Player(id={self.id}, name={self.name!r})"


class Match(Base):
    __tablename__: str = 'matches'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), primary_key=True, nullable=False, unique=True,
                                      default=lambda: str(uuid.uuid4()))
    player1_id: Mapped[int] = mapped_column(ForeignKey('players.id', ondelete='CASCADE'))
    player2_id: Mapped[int] = mapped_column(ForeignKey('players.id', ondelete='CASCADE'))
    winner_id: Mapped[int] = mapped_column(ForeignKey('players.id', ondelete='CASCADE'))
    score: Mapped[JSON] = mapped_column(JSON)

    player1 = relationship('Player', foreign_keys=[player1_id], lazy='joined')
    player2 = relationship('Player', foreign_keys=[player2_id], lazy='joined')
    winner = relationship('Player', foreign_keys=[winner_id], lazy='joined')

    def __repr__(self):
        return (f"Match(id={self.id}, uuid={self.uuid},"
                f"player1={self.player1_id}, player2={self.player2_id},"
                f"winner={self.winner_id},score={self.score}")

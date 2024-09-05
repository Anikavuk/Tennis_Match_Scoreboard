import uuid

from sqlalchemy import ForeignKey, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String


class Base(DeclarativeBase):
    pass


class PlayersOrm(Base):
    __tablename__: str = "players"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(length=255))

    def __repr__(self) -> str:
        return f"PlayerOrm(id={self.id}, name={self.name!r})"


class MatchesOrm(Base):
    __tablename__: str = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, nullable=False, unique=True,
                                      default=lambda: str(uuid.uuid4()))
    # mapped_column(unique=True, nullable=False)
    player1: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    player2: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    winner: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    score: Mapped[str] = mapped_column(VARCHAR(length=255))

    def __repr__(self):
        return (f"MatchesOrm(id={self.id}, uuid={self.uuid}, "
                f"player1={self.player1}, player2={self.player2},"
                f"winner={self.winner},score={self.score}")

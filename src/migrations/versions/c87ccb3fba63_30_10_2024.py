"""30.10.2024

Revision ID: c87ccb3fba63
Revises: b8268736af7b
Create Date: 2024-10-30 21:05:43.077221

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "c87ccb3fba63"
down_revision: Union[str, None] = "b8268736af7b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "players", sa.Column("delete", sa.VARCHAR(length=255), nullable=False)
    )
    op.alter_column(
        "players",
        "name",
        existing_type=mysql.VARCHAR(length=255),
        type_=sa.VARCHAR(length=30),
        existing_nullable=False,
    )
    op.create_unique_constraint(None, "players", ["delete"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "players", type_="unique")
    op.alter_column(
        "players",
        "name",
        existing_type=sa.VARCHAR(length=30),
        type_=mysql.VARCHAR(length=255),
        existing_nullable=False,
    )
    op.drop_column("players", "delete")
    # ### end Alembic commands ###

"""31.10.2024

Revision ID: 3f2cef8ca312
Revises: c87ccb3fba63
Create Date: 2024-10-30 21:07:39.222741

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "3f2cef8ca312"
down_revision: Union[str, None] = "c87ccb3fba63"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("delete", table_name="players")
    op.drop_column("players", "delete")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "players",
        sa.Column("delete", mysql.VARCHAR(length=255), nullable=False),
    )
    op.create_index("delete", "players", ["delete"], unique=True)
    # ### end Alembic commands ###

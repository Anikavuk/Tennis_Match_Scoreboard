import os

import sqlalchemy.orm
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.db.models import Base

# Загрузка переменных окружения из файла .env
load_dotenv()

database = os.environ['DATABASE_URL']
# database = os.getenv('DATABASE_URL')

engine = create_engine(database, echo=True, future=True)

SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=True, autoflush=True, bind=engine)

Base.metadata.create_all(bind=engine)  # при создании новой миграции удали эту строчку и бд полностью
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()
# alembic revision --autogenerate -m "30.10.2024"
# alembic upgrade head

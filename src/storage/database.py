import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
import sqlalchemy.orm

from models import Base

load_dotenv()

database_url = os.getenv('DATABASE_URL')

engine = create_engine(database_url, echo=True, future=True)

SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=True, autoflush=True, bind=engine)

Base.metadata.create_all(bind=engine)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

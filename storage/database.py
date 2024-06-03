from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from models import Base

SQLALCHEMY_DATABASE_URL = URL.create(
    "mysql",
    username="root",
    password='050402',
    host="localhost",
    port=3306,
    database="bd_tennis",
)


engine = create_engine(SQLALCHEMY_DATABASE_URL,
                        echo=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
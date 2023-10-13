import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from database.models import Base

connect_args = {"options": "-c statement_timeout=2000", "connect_timeout": 5}

DATABASE_URL = URL.create(
    drivername="postgresql",
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    port=5432,
)

engine = create_engine(DATABASE_URL, connect_args=connect_args)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

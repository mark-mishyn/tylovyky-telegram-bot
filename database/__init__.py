import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from database.models import Base

connect_args = {"options": "-c statement_timeout=2000", "connect_timeout": 5}

if os.getenv('USER') == 'ubuntu':
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")

    if not all([host, database, username, password]):
        raise Exception('NO DB CONNECTION ENV VARIABLES')

    # connect
    db_url = URL.create(
        drivername="postgresql",
        host=host,
        database=database,
        username=username,
        password=password,
        port=5432,
    )
else:
    db_url = "sqlite:///./actors.db"

print('DB URL: ', db_url)

engine = create_engine(db_url, connect_args=connect_args)
Session = sessionmaker(bind=engine)

# create tables
Base.metadata.create_all(bind=engine)

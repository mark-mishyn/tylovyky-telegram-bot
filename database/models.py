from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Our class model for db


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    phone = Column(String)
    email = Column(String)
    social_media_link = Column(String)
    sizes = Column(String)
    hair_colour = Column(String)
    eyes_colour = Column(String)
    type = Column(String)
    actors_skills = Column(String)
    language = Column(String)
    driver_license = Column(String)
    photo_1 = Column(String)
    photo_2 = Column(String)
    photo_3 = Column(String)

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

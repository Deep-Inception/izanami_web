from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.schema import UniqueConstraint
from config.database import Base
from datetime import datetime


class Race(Base):
    __tablename__ = 'race'
    id = Column(Integer, primary_key=True)
    place = Column(String(32), unique=False)
    race_number = Column(String(32), unique=False)
    deadline = Column(DateTime, unique=False)
    distance = Column(Integer, unique=False)
    title_name = Column(String(256), unique=False)
    created_at = Column(DateTime, unique=False, default=datetime.now())
    __table_args__ = (UniqueConstraint("place", "race_number", "deadline", name="unique_race"),)

    def __init__(self, url=None, place=None, race_number=None, deadline=None):
        self.url = url
        self.place = place
        self.race_number = race_number
        self.deadline = deadline

    def __repr__(self):
        return self.url

    def set_params_from_dto(self, dto):
        self.place = dto.place
        self.race_number = dto.race_number
        self.deadline = dto.deadline
        self.distance = dto.distance
        self.title_name = dto.title_name
        return self
from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime


class Race(Base):
    __tablename__ = 'race'
    id = Column(Integer, primary_key=True)
    url = Column(String(128), unique=True)
    deadline = Column(String(128), unique=False)

    def __init__(self, race_dto=None):
        if race_dto:
            self.url = race_dto.url
            self.deadline = race_dto.deadline

    def __repr__(self):
        return self.url
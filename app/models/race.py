from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from config.database import Base
from datetime import datetime
import enum
from .model_mixin import ModelMixin

@enum.unique
class RaceStatusEnum(enum.Enum):
    BEFORE = "BEFORE" # レース前
    IMMEDIATELY_BEFORE = "IMMEDIATELY_BEFORE" # 直前情報入手済
    FINISHED = "FINISHED" # レース結果取得済

class Race(Base, ModelMixin):
    __tablename__ = "race"
    id = Column(Integer, primary_key=True)
    place = Column(String(32), unique=False)
    race_number = Column(String(32), unique=False)
    deadline = Column(DateTime, unique=False)
    distance = Column(Integer, unique=False)
    title_name = Column(String(256), unique=False)
    created_at = Column(DateTime, unique=False, default=datetime.now())
    __table_args__ = (UniqueConstraint("place", "race_number", "deadline", name="unique_race"),)
    timetable_racers = relationship("TimetableRacer", backref="race", lazy=True, order_by="TimetableRacer.couse")
    status = Column(Enum(RaceStatusEnum), nullable=False, default=RaceStatusEnum.BEFORE)

    def __init__(self, url=None, place=None, race_number=None, deadline=None):
        self.url = url
        self.place = place
        self.race_number = race_number
        self.deadline = deadline

    def info(self):
        return "place %s, race_number %s" % (self.place, self.race_number)

    def set_params_from_dto(self, dto):
        self.place = dto.place
        self.race_number = dto.race_number
        self.deadline = dto.deadline
        self.distance = dto.distance
        self.title_name = dto.title_name
        return self

    def before_info_url(self):
        rno = self.race_number
        jcd = self.place
        date_str = self.deadline.strftime("%Y%m%d")
        return "http://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=%s&jcd=%s&hd=%s" % (rno, jcd, date_str)

    def race_result_url(self):
        rno = self.race_number
        jcd = self.place
        date_str = self.deadline.strftime("%Y%m%d")
        return "http://www.boatrace.jp/owpc/pc/race/raceresult?rno=%s&jcd=%s&hd=%s" % (rno, jcd, date_str)
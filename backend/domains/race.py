from datetime import datetime
import enum
from backend import db
from backend.domains.model_mixin import ModelMixin

@enum.unique
class RaceStatusEnum(enum.Enum):
    BEFORE = "BEFORE" # レース前
    IMMEDIATELY_BEFORE = "IMMEDIATELY_BEFORE" # 直前情報入手済
    FINISHED = "FINISHED" # レース結果取得済
    STOPPED = "STOPPED" # レース中止(レース結果データなし)

class Race(db.Model, ModelMixin):
    __tablename__ = "race"
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(32), unique=False)
    race_number = db.Column(db.String(32), unique=False)
    deadline = db.Column(db.DateTime, unique=False)
    distance = db.Column(db.Integer, unique=False)
    title_name = db.Column(db.String(256), unique=False)
    status = db.Column(db.Enum(RaceStatusEnum), nullable=False, default=RaceStatusEnum.BEFORE)
    created_at = db.Column(db.DateTime, unique=False, default=datetime.now())
    __table_args__ = (db.UniqueConstraint("place", "race_number", "deadline", name="unique_race"),)
    timetable_racers = db.relationship("TimetableRacer", backref="race", lazy=True, order_by="TimetableRacer.couse")
    

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
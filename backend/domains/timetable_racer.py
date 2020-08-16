from datetime import datetime
from backend import db
from backend.domains.model_mixin import ModelMixin


class TimetableRacer(db.Model, ModelMixin):
    __tablename__ = "timetable_racer"
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey("race.id"), nullable=False)
    couse = db.Column(db.Integer, unique=False)
    racer_id = db.Column(db.String(32), unique=False)
    name = db.Column(db.String(64), unique=False)
    age = db.Column(db.Integer, unique=False)
    weight = db.Column(db.Integer, unique=False)
    rank = db.Column(db.String(32), unique=False)
    win_rate = db.Column(db.Float, unique=False)
    exacta_rate = db.Column(db.Float, unique=False)
    win_rate_place = db.Column(db.Float, unique=False)
    exacta_rate_place = db.Column(db.Float, unique=False)
    moter_id = db.Column(db.String(32), unique=False)
    exacta_rate_motor = db.Column(db.Float, unique=False)
    boat_id = db.Column(db.String(32), unique=False)
    exacta_rate_boat = db.Column(db.Float, unique=False)
    result_1 = db.Column(db.String(32), unique=False)
    result_2 = db.Column(db.String(32), unique=False)
    result_3 = db.Column(db.String(32), unique=False)
    result_4 = db.Column(db.String(32), unique=False)
    result_5 = db.Column(db.String(32), unique=False)
    result_6 = db.Column(db.String(32), unique=False)
    exhibition_time = db.Column(db.Float, unique=False)
    tilt = db.Column(db.Float, unique=False)
    created_at = db.Column(db.DateTime, unique=False, default=datetime.now())
    racer_result = db.relationship("RacerResult", backref="timetable_racer", lazy=True, uselist=False)
    racer_prediction_dl = db.relationship("RacerPredictionDL", backref="timetable_racer", lazy=True, uselist=False)
    __table_args__ = (db.UniqueConstraint("race_id", "racer_id", name="unique_racer"),)


    def __init__(self):
        self

    def info(self):
        return "race_id %s, racer_id %s" % (self.race_id, self.racer_id)

    def set_params_from_dto(self, dto):
        self.race_id = dto.race_id
        self.couse = dto.couse
        self.racer_id = dto.racer_id
        self.name = dto.name
        self.age = dto.age
        self.weight = dto.weight
        self.rank = dto.rank
        self.win_rate = dto.win_rate
        self.exacta_rate = dto.exacta_rate
        self.win_rate_place = dto.win_rate_place
        self.exacta_rate_place = dto.exacta_rate_place
        self.moter_id = dto.moter_id
        self.exacta_rate_motor = dto.exacta_rate_motor
        self.boat_id = dto.boat_id
        self.exacta_rate_boat = dto.exacta_rate_boat
        self.result_1 = dto.result_1
        self.result_2 = dto.result_2
        self.result_3 = dto.result_3
        self.result_4 = dto.result_4
        self.result_5 = dto.result_5
        self.result_6 = dto.result_6
        return self

    def has_before_info(self):
        return self.exhibition_time is not None or self.tilt is not None

    def set_before_info(self, dto):
        self.exhibition_time = dto.exhibition
        self.tilt = dto.tilt
        return self

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from backend import db
from datetime import datetime

class RacerPredictionDL(db.Model):
    __tablename__ = "racer_pred_dl"
    id = db.Column(Integer, primary_key=True)
    timetable_racer_id = db.Column(Integer, ForeignKey("timetable_racer.id"), nullable=False, unique=True)
    version = db.Column(Integer, unique=False, nullable=False)
    time = db.Column(Float, unique=False)
    created_at = db.Column(DateTime, unique=False, default=datetime.now())

    def __init__(self, timetable_racer_id=None, version=None, time=None):
        self.timetable_racer_id = timetable_racer_id
        self.version = version
        self.time = time

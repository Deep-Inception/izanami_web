from datetime import datetime
from backend import db

class RacerPredictionDL(db.Model):
    __tablename__ = "racer_pred_dl"
    id = db.Column(db.Integer, primary_key=True)
    timetable_racer_id = db.Column(db.Integer, db.ForeignKey("timetable_racer.id"), nullable=False, unique=True)
    version = db.Column(db.Integer, unique=False, nullable=False)
    time = db.Column(db.Float, unique=False)
    created_at = db.Column(db.DateTime, unique=False, default=datetime.now())

    def __init__(self, timetable_racer_id=None, version=None, time=None):
        self.timetable_racer_id = timetable_racer_id
        self.version = version
        self.time = time

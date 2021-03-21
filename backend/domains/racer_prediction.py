from datetime import datetime
from backend import db

class RacerPrediction(db.Model):
    __tablename__ = "racer_prediction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timetable_racer_id = db.Column(db.Integer, db.ForeignKey("timetable_racer.id"), nullable=False)
    model = db.Column(db.String, unique=False, nullable=False)
    version = db.Column(db.Integer, unique=False, nullable=False)
    value = db.Column(db.Float, unique=False)
    created_at = db.Column(db.DateTime, unique=False, default=datetime.now())
    __table_args__ = (db.UniqueConstraint("timetable_racer_id", "model", "version", name="unique_prediction"),)

    def __init__(self, timetable_racer_id=None, model=None, version=None, value=None):
        self.timetable_racer_id = timetable_racer_id
        self.model = model
        self.version = version
        self.value = value

    def set_params(self, timetable_racer_id=None, model=None, version=None, value=None):
        self.timetable_racer_id = timetable_racer_id
        self.model = model
        self.version = version
        self.value = value
        return self

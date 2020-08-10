from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from backend.domains.database import Base
from datetime import datetime

class RacerPredictionDL(Base):
    __tablename__ = "racer_pred_dl"
    id = Column(Integer, primary_key=True)
    timetable_racer_id = Column(Integer, ForeignKey("timetable_racer.id"), nullable=False, unique=True)
    version = Column(Integer, unique=False, nullable=False)
    time = Column(Float, unique=False)
    created_at = Column(DateTime, unique=False, default=datetime.now())

    def __init__(self, timetable_racer_id=None, version=None, time=None):
        self.timetable_racer_id = timetable_racer_id
        self.version = version
        self.time = time

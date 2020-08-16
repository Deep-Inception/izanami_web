from sqlalchemy import Column, Integer, DateTime, ForeignKey
from backend import db
from datetime import datetime

class Result(db.Model):
    __tablename__ = "result"
    id = db.Column(Integer, primary_key=True)
    race_id = db.Column(Integer, ForeignKey("race.id"), nullable=False, unique=True)
    win = db.Column(Integer, nullable=True, unique=False) # 単勝
    exacta = db.Column(Integer, nullable=True, unique=False) # 二連単
    quinella = db.Column(Integer, nullable=True, unique=False) # 二連複
    trifecta = db.Column(Integer, nullable=True, unique=False) # 三連単
    trio = db.Column(Integer, nullable=True, unique=False) # 三連複
    show1 = db.Column(Integer, nullable=True, unique=False) # 複勝1位
    show2 = db.Column(Integer, nullable=True, unique=False) # 複勝2位
    created_at = db.Column(DateTime, unique=False, default=datetime.now())

    def __init__(self):
        self.win = None
        self.exacta = None
        self.quinella = None
        self.trifecta = None
        self.trio = None
        self.show1 = None
        self.show2 = None

    def info(self):
        return "win %s, exacta %s" % (self.win, self.exacta)

    def set_params_from_dto(self, dto):
        self.race_id = dto.race_id
        self.win = dto.win
        self.exacta = dto.exacta
        self.quinella = dto.quinella
        self.trifecta = dto.trifecta
        self.trio = dto.trio
        self.show1 = dto.show1
        self.show2 = dto.show2
        return self

from datetime import datetime
import enum, re
from backend import db
from backend.domains.model_mixin import ModelMixin

class QisqualificationEnum(enum.Enum):
    L0 = "L0" # 選手責任外の出遅れ
    L1 = "L1" # 選手責任の出遅れ
    K0 = "K0" # 選手責任外の事前欠場
    K1 = "K1" # 選手責任の事前欠場
    S0 = "S0" # 選手責任外の失格
    S1 = "S1" # 選手責任の失格
    S2 = "S2" # 他艇を妨害・失格
    F = "Ｆ" # フライング
    K = "欠" # 欠場
    T = "転" # 転覆
    R = "落" # 落水
    L = "Ｌ" # 出遅れ
    B = "妨" # 妨害失格
    E = "エ" # エンスト失格
    C = "沈" # 沈没失格
    H = "不" # 不完走失格
    S = "失" # 前記以外の失格

    @classmethod
    def value_of(cls, target_value):
        for e in QisqualificationEnum:
            if e.value == target_value:
                return e

def parse_prize_zen_to_han(str):
    prize_dict = {"１": 1, "２": 2, "３": 3, "４": 4, "５":5, "６": 6}
    if re.match(r"[1-6]", str):
        return str
    else:
        return prize_dict[str]


class RacerResult(db.Model, ModelMixin):
    __tablename__ = "racer_result"
    id = db.Column(db.Integer, primary_key=True)
    timetable_racer_id = db.Column(db.Integer, db.ForeignKey("timetable_racer.id"), nullable=False, unique=True)
    time = db.Column(db.Float, unique=False)
    prize = db.Column(db.Integer, unique=False)
    disqualification = db.Column(db.Enum(QisqualificationEnum), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, unique=False, default=datetime.now())

    def __init__(self, timetable_racer_id=None, prize=None, time=None, disqualification=None):
        self.timetable_racer_id = timetable_racer_id
        self.prize = prize
        self.time = time
        self.disqualification = disqualification

    def info(self):
        return "time %s, prize %s" % (self.time, self.prize)

    def set_params_from_dto(self, dto):
        self.time = dto.time
        self.timetable_racer_id = dto.timetable_racer_id
        if re.match(r"[1-6,１-６]", dto.prize):
            self.prize = parse_prize_zen_to_han(dto.prize)
        else:
            self.disqualification = QisqualificationEnum.value_of(dto.prize)
        return self

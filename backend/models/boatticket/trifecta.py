import numpy as np
from .boat_ticket_base import BoatTicketBase

# 3連単クラス
class Trifecta(BoatTicketBase):

    def __init__(self, pred):
        self.pred = np.reshape(pred, (6))

    # 第1予想までを返す
    # TODO 第3予想まで計算して返せるようにする
    # （計算方法の候補：1位の確率*1位が以外の5艇の中での1位の確率*1,2位が以外の4艇の中での1位の確率）
    def predict(self):
        first = super().first_prize_index()
        second = super().second_prize_index()
        third = super().third_prize_index()
        pred = [first, second, third]
        return (pred,)

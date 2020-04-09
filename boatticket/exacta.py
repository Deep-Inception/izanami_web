import numpy as np
from boatticket.boat_ticket_base import BoatTicketBase

# 2連単クラス
class Exacta(BoatTicketBase):

    def __init__(self, pred):
        self.pred = np.reshape(pred, (6))

    # 第3予想までを返す
    def predict(self):
        first = super().first_prize_index()
        second = super().second_prize_index()
        third = super().third_prize_index()
        pred1_2 = [first, second]
        pred2_1 = [second, first]
        pred1_3 = [first, third]
        if self.is_second(first, second, third):
            return pred1_2, pred2_1, pred1_3
        else:
            return pred1_2, pred1_3, pred2_1

    def is_second(self, first_idx, second_idx, third_idx):
        first_val = self.pred[first_idx]
        second_val = self.pred[second_idx]
        third_val = self.pred[third_idx]
        sum_val = self.pred.sum()
        # 2-1 の確率（1−３との差の部分のみ）
        second_first_val = second_val / ( sum_val - second_val )
        # 1-3 の確率（2−1との差の部分のみ）
        first_third_val = third_val / ( sum_val - first_val )
        return second_first_val >= first_third_val
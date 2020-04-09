import numpy as np
from boatticket.boat_ticket_base import BoatTicketBase

# 複式舟券のabstractクラス
class CombinationBoatTicket(BoatTicketBase):
    def __init__(self, pred):
        super().__init__(pred)
        self.create_all_rate_list()

    def predict(self):
        first_idx = self.rate_idx[0]
        second_idx = self.rate_idx[1]
        third_idx = self.rate_idx[2]
        return self.all_list[first_idx], self.all_list[second_idx], self.all_list[third_idx]

    # [レーンの組み合わせ, 確率]のNumpyリスト
    def create_all_rate_list(self):
        all_list = self.create_all_combination()
        all_rate_list = np.array([self.win_rate(i) for i in all_list])
        self.all_list = all_list
        rate_idx_sorted = all_rate_list.argsort()[::-1]
        self.rate_idx = rate_idx_sorted

    def create_all_combination(self):
        raise NotImplementedError()

    def win_rate(self, combination):
        raise NotImplementedError()
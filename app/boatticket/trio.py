import numpy as np
from boatticket.boat_ticket_base import CombinationBoatTicket

# 3連複クラス
class Trio(CombinationBoatTicket):
    def __init__(self, pred):
        super().__init__(pred)
        self.create_all_rate_list()

    def create_all_combination(self):
        pred = self.pred
        length = len(pred)
        all_list = []
        for i in range(length):
            for j in range(i):
                for k in range(j):
                    all_list.append([k, j, i])
        return all_list

    def win_rate(self, combination):
        if len(combination) != 3:
            return None
        first = self.pred[combination[0]]
        second = self.pred[combination[1]]
        third = self.pred[combination[2]]
        return first * second * third

import numpy as np
from boatticket.boat_ticket_base import CombinationBoatTicket

# 2連複
class Quinella(CombinationBoatTicket):
    def __init__(self, pred):
        super().__init__(pred)

    def create_all_combination(self):
        pred = self.pred
        length = len(pred)
        all_list = []
        for i in range(length):
            for j in range(i):
                all_list.append([j, i])
        return all_list

    def win_rate(self, combination):
        if len(combination) != 2:
            return None
        first = self.pred[combination[0]]
        second = self.pred[combination[1]]
        return first * second
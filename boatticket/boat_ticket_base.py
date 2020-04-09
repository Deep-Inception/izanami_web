import numpy as np

# 舟券の親クラス　予想結果（一位確率）を引数にしてインスタンスを作る
class BoatTicketBase:
    def __init__(self, pred):
        self.pred = np.reshape(pred, (6))
    
    # 同確率ならインデックスが若い方を返す    
    def first_prize_index(self):
        pred = self.pred
        first = pred.argmax(axis = 0)
        return first
    
    # 同確率ならインデックスが若い方を返す
    def second_prize_index(self):
        first = self.first_prize_index()
        del_f = np.delete(self.pred, first)
        second = del_f.argmax(axis = 0)
        return second if first > second else second + 1
    
    def third_prize_index(self):
        first = self.first_prize_index()
        second = self.second_prize_index()
        del_f = np.delete(self.pred, [first, second])
        third_val = np.max(del_f)
        third = np.where(self.pred == third_val)
        return third[-1][0]
        
    
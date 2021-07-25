# レース結果の予想を返すクラス
from . import math_util
from sklearn.preprocessing import StandardScaler

def win_rate(pred):
    recip = math_util.reciprocal(pred)
    scaler = StandardScaler()
    recip = recip.reshape(-1, 1)
    recip_scaler = scaler.fit_transform(recip)
    return math_util.softmax(recip_scaler)
# レース結果の予想を返すクラス
from izanamiutils import math_util
from sklearn.preprocessing import StandardScaler

def win_rate(pred):
    recip = math_util.reciprocal(pred)
    scaler = StandardScaler()
    recip_scaler = scaler.fit_transform(recip)
    return math_util.softmax(recip_scaler)
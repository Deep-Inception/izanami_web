# レース結果の予想を返すクラス
import numpy as np
from izanamiutils import math_util
from sklearn.preprocessing import StandardScaler
print("Run race.py")

def win_rate(pred):
    recip = math_util.reciprocal(pred)
    scaler = StandardScaler()
    recip_scaler = scaler.fit_transform(recip)
    return math_util.softmax(recip_scaler)
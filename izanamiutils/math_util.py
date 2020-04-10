# レース結果予測に使う数値計算用のクラス
import numpy as np

def softmax(ndarray):
    ndarray_e = np.exp(ndarray)
    total = ndarray_e.sum()
    return ndarray_e / total

def reciprocal(pred):
    return np.reciprocal(pred)
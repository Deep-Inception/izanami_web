# レース結果予測に使う数値計算用のクラス
import numpy as np

def softmax(ndarray):
    ndarray_e = np.exp(ndarray)
    total = ndarray_e.sum()
    return ndarray_e / total

def reciprocal(pred):
    return np.reciprocal(pred)

# スクレイピングのときに入る余分な文字の削除
def trim_text(text):
    if text.find(u'\xa0') >= 0:
        text = text.replace(u'\xa0', u'')
    return text

def cast_to_float(text):
    text = trim_text(text)
    if text == None or len(text) == 0:
        return None
    else:
        return float(text)
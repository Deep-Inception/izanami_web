import sys

from backend.controllers import batch, prediction
import datetime
from datetime import timedelta

# バッチの叩き方
# 2020/01/01から2020/01/07までのレース予定情報をインポートする
# python batch_by_date.py race_data 2020-02-01 2020-02-04

# レース直前情報をインポートする
# python batch_by_date.py before_info

# レース結果をインポートする
# python batch_by_date.py race_result

# 予想モデルに学習させる
# python batch_by_date.py models_fit

def daterange(_start, _end):
    for n in range((_end - _start).days + 1):
        yield _start + timedelta(n)

arg = sys.argv

if arg[1] == "race_data":
    from_date = datetime.datetime.strptime(f"{arg[2]} 00:00", '%Y-%m-%d 00:00')
    to_date = datetime.datetime.strptime(f"{arg[3]} 00:00", '%Y-%m-%d 00:00')
    
    for i in daterange(from_date, to_date):
        batch.import_race_data(i)
elif arg[1] == "before_info":
    batch.before_info_batch()
elif arg[1] == "race_result":
    batch.race_result_batch()
elif arg[1] == "models_fit":
    prediction.fix()

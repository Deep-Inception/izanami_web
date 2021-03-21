import schedule
import time, date
from backend.controllers import batch, prediction

def race_index_job():
    batch.index()

def before_info_job():
    batch.before_info_batch()

def race_result_job():
    batch.race_result_batch()

def prediction_fix_job():
    if date.today().day != 1:
        return
    prediction.fix()

schedule.every().day.at("04:00").do(prediction_fix_job)
schedule.every().day.at("02:00").do(race_index_job)
schedule.every(5).minutes.do(before_info_job)
schedule.every(5).minutes.do(race_result_job)

while True:
    schedule.run_pending()
    time.sleep(1)
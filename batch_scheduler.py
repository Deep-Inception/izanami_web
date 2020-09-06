import schedule
import time
from backend.controllers import batch

def race_index_job():
    batch.index()

def before_info_job():
    batch.before_info_batch()

def race_result_job():
    batch.race_result_batch()

schedule.every().day.at("02:00").do(race_index_job)
schedule.every(5).minutes.do(before_info_job)
schedule.every(5).minutes.do(race_result_job)

while True:
    schedule.run_pending()
    time.sleep(1)
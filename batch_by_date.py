from backend.controllers import batch
import datetime
from datetime import timedelta

from_date = datetime.datetime(2020, 9, 1)
to_date = datetime.datetime(2021, 1, 1)

def daterange(_start, _end):
    for n in range((_end - _start).days):
        yield _start + timedelta(n)

# for i in daterange(from_date, to_date):
#     batch.import_race_data(i)

# batch.before_info_batch()
batch.race_result_batch()

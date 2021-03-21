from backend.controllers import batch, prediction
import datetime
from datetime import timedelta

from_date = datetime.datetime(2021, 1, 2)
to_date = datetime.datetime(2021, 1, 3)

# def daterange(_start, _end):
#     for n in range((_end - _start).days):
#         yield _start + timedelta(n)

# for i in daterange(from_date, to_date):
#     batch.import_race_data(i)
# prediction.fix()
# batch.before_info_batch()
# batch.race_result_batch()


from backend import db
# db.drop_all(bind=None)
db.create_all()
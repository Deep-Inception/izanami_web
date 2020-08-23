# 過去3ヶ月分のレースデータを格納する
from backend.controllers import batch
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

end_date = datetime.date.today()
end_date_str = end_date.strftime("%Y-%m-%d")
start_date = end_date - relativedelta(months=3)
start_date_str = start_date.strftime("%Y-%m-%d")
period = pd.date_range(start_date_str, end_date_str)

for date in period:
    batch.import_race_data(date)
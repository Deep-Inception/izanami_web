import pandas as pd
import pickle
import datetime
from flask import logging
from sklearn.model_selection import train_test_split
from backend.domains.racer_prediction import RacerPrediction
from backend.models.machinelearning import ml_racer_prize_lgb, preprocessing_racer_prize_lgb
from backend import db_session
from backend.domains.timetable_racer import TimetableRacer
from backend.domains.race import Race, RaceStatusEnum
from backend.domains.racer_result import RacerResult
from backend.utils.izanamiutils import file_util

logger = logging.logging
PP_PICKLE_PATH = './backend/tmp/preprocessors/racer_prize_lgb_preprocessor.pickle'
ML_PICKLE_PATH = './backend/tmp/models/ml_racer_prize_lgb.txt'


def fix():
    raw_data_df = get_all_train_data()
    train_data , valid_data = train_test_split(raw_data_df, random_state=0, test_size=0.2)
    preprocessor = preprocessing_racer_prize_lgb.RacerPrizeLgbPreprocessor()

    preprocessor.fix(train_data)
    train_data = preprocessor.transform(train_data)
    valid_data = preprocessor.transform(valid_data)
    
    file_util.pickle_dump(preprocessor, PP_PICKLE_PATH)
    ml_racer_prize_lgb.fit(train_data, valid_data, model_file=ML_PICKLE_PATH)

# モデルの学習に利用するデータを取得する 戻り値：dataframe
def get_all_train_data():
    # レースは直近一年のものに限定する
    race_df = Race.values_as_dataframe_by_query(db_session.query(Race).filter(Race.status == RaceStatusEnum.FINISHED).all())
    race_df.deadline = pd.to_datetime(race_df.deadline)
    last_date = race_df.deadline.max()
    race_df = race_df.loc[race_df.deadline >= (last_date - datetime.timedelta(days=365))]
    timetable_racer_df = TimetableRacer.values_as_dataframe_by_query(db_session.query(TimetableRacer).filter(TimetableRacer.exhibition_time != None).all())
    # レースが行われたが無効の場合があるので、順位がある人のデータだけ使って予測する
    racer_result_df = RacerResult.values_as_dataframe_by_query(RacerResult.query.filter(RacerResult.time != None).all())
    merged_df = merge_train_data(race_df, timetable_racer_df, racer_result_df)
    return merged_df

# モデル学習用のデータをJOINする
def merge_train_data(race_df, timetable_racer_df, racer_result_df):
    merged_df = pd.merge(race_df, timetable_racer_df)
    merged_df = pd.merge(merged_df, racer_result_df)
    merged_df.sort_values(["race_id", "prize"], inplace=True)
    return merged_df

def predict(df_data):
    with open(PP_PICKLE_PATH, 'rb') as f:
        preprocessor = pickle.load(f)

    pred_data = preprocessor.transform(df_data)
    y_pred = ml_racer_prize_lgb.predict(pred_data[ml_racer_prize_lgb.cols], model_file=ML_PICKLE_PATH)
    
    for ttr_id , prize in zip(list(df_data["timetable_racer_id"]), y_pred):
        result = RacerPrediction(timetable_racer_id=ttr_id, value=prize, model=ml_racer_prize_lgb.MODEL_NAME, version=ml_racer_prize_lgb.VERSION)
        db_session.add(result)
        db_session.commit()
        db_session.expunge(result)

import pandas as pd
import pickle
import datetime
from flask import logging
from backend import db_session
from backend.domains.racer_prediction import RacerPrediction
from backend.models.machinelearning import ml_racer_time_dl, preprocessing_racer_time_dl
from backend.domains.timetable_racer import TimetableRacer
from backend.domains.race import Race, RaceStatusEnum
from backend.domains.racer_result import RacerResult
from backend.utils.izanamiutils import file_util

logger = logging.logging
PP_PICKLE_PATH = './backend/tmp/preprocessors/racer_time_dl_preprocessor.pickle'
ML_PICKLE_PATH = './backend/tmp/models/ml_racer_time_dl.pickle'

def fix():
    raw_data_df = train_data()
    preprocessor = preprocessing_racer_time_dl.RacerPredDlPreprocessor()
    preprocessor.data_prepare(raw_data_df, 1)
    X, y = preprocessor.get_prepared_data()
    
    if not pd.isnull(y).any():
        file_util.pickle_dump(preprocessor, PP_PICKLE_PATH)
        ml_racer_time_dl.fit_and_save(X, y, file_path=ML_PICKLE_PATH)

# モデルの学習に利用するデータを取得する 戻り値：dataframe
def train_data():
    # レースは直近二ヶ月のものに限定する
    race_df = Race.values_as_dataframe_by_query(db_session.query(Race).filter(Race.status == RaceStatusEnum.FINISHED).all())
    race_df.deadline = pd.to_datetime(race_df.deadline)
    last_date = race_df.deadline.max()
    race_df = race_df.loc[race_df.deadline >= (last_date - datetime.timedelta(days=60))]
    timetable_racer_df = TimetableRacer.values_as_dataframe_by_query(db_session.query(TimetableRacer).filter(TimetableRacer.exhibition_time != None).all())
    # レース全員timeがない場合があるので、タイムがある人のデータだけ使って予測する
    racer_result_df = RacerResult.values_as_dataframe_by_query(RacerResult.query.filter(RacerResult.time != None).all())
    merged_df = merge_train_data(race_df, timetable_racer_df, racer_result_df)
    raw_data_df = raw_data(merged_df)
    return raw_data_df

# モデル学習用のデータをJOINする
def merge_train_data(race_df, timetable_racer_df, racer_result_df):
    merged_df = pd.merge(race_df, timetable_racer_df)
    merged_df = pd.merge(merged_df, racer_result_df)
    merged_df.sort_values(["race_id", "prize"], inplace=True)
    return merged_df

# 学習に必要な行、列のみを取得し、適宜カラム名、変更する
def raw_data(merged_df):
    raw_data_df = merged_df.loc[:, ["time", "place", "deadline", "distance", "couse", "racer_id", "exhibition_time"]]
    raw_data_df.dropna(how='any',subset=["place", "deadline", "distance", "couse", "racer_id", "exhibition_time"], inplace=True)
    raw_data_df.rename(columns={"time": "RACE_TIME", "place": "PLACE","deadline": "RACE_DATE", "distance": "DISTANCE", "couse": "COUSE", "racer_id": "RACER_ID", "exhibition_time": "EXHIBITION_TIME"}, inplace=True)
    return raw_data_df

def predict(df_data):
    with open(PP_PICKLE_PATH, 'rb') as f:
        preprocessor = pickle.load(f)

    raw_data_df = df_data[["place", "deadline", "distance", "couse", "racer_id", "exhibition_time"]]
    raw_data_df.rename(columns={"place": "PLACE","deadline": "RACE_DATE", "distance": "DISTANCE", "couse": "COUSE", "racer_id": "RACER_ID", "exhibition_time": "EXHIBITION_TIME"}, inplace=True)
    preprocessor.data_prepare(raw_data_df, 0)
    X, y = preprocessor.get_prepared_data()
    y_pred = ml_racer_time_dl.predict(X, file_path=ML_PICKLE_PATH)
    for ttr_id , time in zip(list(df_data["timetable_racer_id"]), y_pred):
        result = RacerPrediction().set_params(timetable_racer_id=ttr_id, value=time[0],  model=ml_racer_time_dl.MODEL_NAME, version=ml_racer_time_dl.VERSION)
        db_session.add(result)
        db_session.commit()
        db_session.expunge(result)

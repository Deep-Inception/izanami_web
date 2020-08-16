from flask import Blueprint
from flask import logging
import pandas as pd
import pickle
from backend.domains.database import db_session
from backend.domains.timetable_racer import TimetableRacer
from backend.domains.race import Race, RaceStatusEnum
from backend.domains.racer_result import RacerResult
from backend.domains.racer_pred_dl import RacerPredictionDL
from backend.models.machinelearning import ml_racer_pred_dl, preprocessing_racer_pred_dl

prediction = Blueprint('preditction', __name__)
logger = logging.logging

PP_PICKLE_PATH = './backend/tmp/preprocessors/racer_pred_dl_preprocessor.pickle'
ML_PICKLE_PATH = './backend/tmp/models/ml_racer_pred_dl.pickle'

@prediction.route("/fit/")
def fix():
    raw_data_df = train_data()
    preprocessor = preprocessing_racer_pred_dl.RacerPredDlPreprocessor()
    preprocessor.data_prepare(raw_data_df, 1)
    X, y = preprocessor.get_prepared_data()
    if not pd.isnull(y).any():
        with open(PP_PICKLE_PATH, 'wb') as f:
            pickle.dump(preprocessor, f)
        ml_racer_pred_dl.fit_and_save(X, y, file_path=ML_PICKLE_PATH)
    return "ok"

# モデルの学習に利用するデータを取得する　戻り値：dataframe
def train_data():
    race_ids = [ r[0] for r in db_session.query(Race.id).filter(Race.status == RaceStatusEnum.FINISHED).all() ]
    race_df = Race.values_as_dataframe_by_ids(race_ids)
    timetable_racer_query = db_session.query(TimetableRacer.id).filter(TimetableRacer.race_id.in_(race_ids), TimetableRacer.exhibition_time != None).all()
    timetable_racer_ids = [ r[0] for r in timetable_racer_query ]
    timetable_racer_df = TimetableRacer.values_as_dataframe_by_ids(timetable_racer_ids)
    racer_result_df = RacerResult.values_as_dataframe_by_query(RacerResult.query.filter(RacerResult.timetable_racer_id.in_(timetable_racer_ids)))
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
    raw_data_df = merged_df[["time", "place", "deadline", "distance", "couse", "racer_id", "exhibition_time"]]
    raw_data_df.dropna(how='any',subset=["place", "deadline", "distance", "couse", "racer_id", "exhibition_time"], inplace=True)
    raw_data_df.rename(columns={"time": "RACE_TIME", "place": "PLACE","deadline": "RACE_DATE", "distance": "DISTANCE", "couse": "COUSE", "racer_id": "RACER_ID", "exhibition_time": "EXHIBITION_TIME"}, inplace=True)
    return raw_data_df

@prediction.route("/predict/")
def predict():
    with open(PP_PICKLE_PATH, 'rb') as f:
        preprocessor = pickle.load(f)
    # 予想するレーサーのデータフレームを作成する
    race_ids = [ r[0] for r in db_session.query(Race.id).filter(Race.status == RaceStatusEnum.IMMEDIATELY_BEFORE).all() ]
    race_df = Race.values_as_dataframe_by_ids(race_ids)
    predicted_timetable_racer_id_list = set([ r[0] for r in db_session.query(RacerPredictionDL.timetable_racer_id).all()])
    timetable_racers = db_session.query(TimetableRacer.id).filter(TimetableRacer.race_id.in_(race_ids), TimetableRacer.exhibition_time != None).all()
    timetable_racer_ids = set([ r[0] for r in timetable_racers ])
    # 一度も予想されていないレーサーだけに絞る
    prepredict_timetable_racer_ids = timetable_racer_ids - predicted_timetable_racer_id_list
    timetable_racer_df = TimetableRacer.values_as_dataframe_by_ids(prepredict_timetable_racer_ids)

    # 新たに予想するレーサーがいなかったら終了
    if timetable_racer_df.empty:
        return "ok"

    merged_df = pd.merge(race_df, timetable_racer_df)
    raw_data_df = merged_df[["place", "deadline", "distance", "couse", "racer_id", "exhibition_time"]]
    raw_data_df.rename(columns={"place": "PLACE","deadline": "RACE_DATE", "distance": "DISTANCE", "couse": "COUSE", "racer_id": "RACER_ID", "exhibition_time": "EXHIBITION_TIME"}, inplace=True)
    preprocessor.data_prepare(raw_data_df, 0)
    X, y = preprocessor.get_prepared_data()
    y_pred = ml_racer_pred_dl.predict(X, file_path=ML_PICKLE_PATH)
    for ttr_id , time in zip(list(merged_df["timetable_racer_id"]), y_pred):
        result = RacerPredictionDL(timetable_racer_id=ttr_id, time=time[0], version=ml_racer_pred_dl.VERSION)
        logger.DEBUG("timetable_racer_id: %i, version: %i" % (result.ttr_id, ml_racer_pred_dl.VERSION))
        db_session.add(result)
        db_session.commit()
        db_session.expunge(result)
    return "ok %i" % len(y_pred)
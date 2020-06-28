# vim:fileencoding=utf8
from flask import Blueprint
from flask import logging
import pandas as pd
import datetime
import pickle
import numpy as np

from config.database import db_session
from models.timetable_racer import TimetableRacer
from models.race import Race, RaceStatusEnum
from models.racer_result import RacerResult
from models.racer_pred_dl import RacerPredictionDL
from machinelearning import ml_racer_pred_dl, preprocessing_racer_pred_dl

predict_app = Blueprint("predict", __name__, template_folder="./templates", static_folder="./static")
logger = logging.logging

@predict_app.route("/test/")
def fix():
    race_ids = [ r[0] for r in db_session.query(Race.id).filter(Race.status == RaceStatusEnum.FINISHED).all() ]
    race_df = Race.values_as_dataframe_by_ids(race_ids)
    timetable_racer_query = db_session.query(TimetableRacer.id).filter(TimetableRacer.race_id.in_(race_ids), TimetableRacer.exhibition_time != None).all()
    timetable_racer_ids = [ r[0] for r in timetable_racer_query ]
    timetable_racer_df = TimetableRacer.values_as_dataframe_by_ids(timetable_racer_ids)
    racer_result_df = RacerResult.values_as_dataframe_by_query(RacerResult.query.filter(RacerResult.timetable_racer_id.in_(timetable_racer_ids)))
    merged_df = pd.merge(race_df, timetable_racer_df)
    merged_df = pd.merge(merged_df, racer_result_df)
    merged_df.sort_values(["race_id", "prize"], inplace=True)
    raw_data_df = merged_df[["time", "place", "deadline", "distance", "couse", "racer_id", "exhibition_time"]]
    raw_data_df.dropna(how='any', inplace=True)
    raw_data_df.rename(columns={"time": "RACE_TIME", "place": "PLACE","deadline": "RACE_DATE", "distance": "DISTANCE", "couse": "COUSE", "racer_id": "RACER_ID", "exhibition_time": "EXHIBITION_TIME"}, inplace=True)
    preprocessor = preprocessing_racer_pred_dl.RacerPredDlPreprocessor()
    preprocessor.data_prepare(raw_data_df, 1)
    X, y = preprocessor.get_prepared_data()
    with open('machinelearning/racer_pred_dl_preprocessor.pickle', 'wb') as f:
        pickle.dump(preprocessor, f)
    ml_racer_pred_dl.fit(X, y)
    return "ok"

@predict_app.route("/predict/")
def predict():
    with open('machinelearning/racer_pred_dl_preprocessor.pickle', 'rb') as f:
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
    y_pred = ml_racer_pred_dl.predict(X)
    for ttr_id , time in zip(list(merged_df["timetable_racer_id"]), y_pred):
        result = RacerPredictionDL(timetable_racer_id=ttr_id, time=time[0], version=ml_racer_pred_dl.VERSION)
        db_session.add(result)
        db_session.commit()
        db_session.expunge(result)
    return "ok %i" % len(y_pred)
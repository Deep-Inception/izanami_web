from flask import Blueprint
from flask import logging
import pandas as pd
import pickle
from backend.domains.timetable_racer import TimetableRacer
from backend.domains.race import Race, RaceStatusEnum
from backend.domains.racer_result import RacerResult
from backend.domains.racer_pred_dl import RacerPredictionDL
from backend.models.machinelearning import ml_racer_pred_dl, preprocessing_racer_pred_dl
from backend.controllers import prediction_racer_pred_dl, prediction_racer_prize_lgb
from backend import db_session

prediction = Blueprint('prediction', __name__)
logger = logging.logging

@prediction.route("/fit/")
def fix():
    prediction_racer_pred_dl.fix()
    prediction_racer_prize_lgb.fix()
    return "ok"

@prediction.route("/predict/")
def predict():
    prediction_df = predict_data()
    # 新たに予想するレーサーがいなかったら終了
    if prediction_df.empty:
        return "ok"
    
    try:
        race_ids = set(prediction_df.race_id)
        races = Race.query.filter(Race.id.in_(race_ids)).all()
        prediction_racer_pred_dl.predict(prediction_df)
        prediction_racer_prize_lgb.predict(prediction_df)
        logger.debug("%i 件の予想完了" % len(races))
        for race in races:
            race.has_prediction = True
        db_session.commit()
    except :
        logger.error("%i 件の予想失敗" % len(races))
    finally:
        db_session.expunge_all()
    return "ok"

def predict_data():
    # 予想するレーサーのデータフレームを作成する
    race_df = Race.values_as_dataframe_by_query(db_session.query(Race).filter(Race.status == RaceStatusEnum.IMMEDIATELY_BEFORE, Race.has_prediction == False).all())
    race_ids = set(race_df.race_id)
    timetable_racer_df = TimetableRacer.values_as_dataframe_by_query(db_session.query(TimetableRacer).filter(TimetableRacer.race_id.in_(race_ids)).all())
    merged_df = pd.merge(race_df, timetable_racer_df)
    merged_df.sort_values(["couse"], inplace=True)
    return merged_df